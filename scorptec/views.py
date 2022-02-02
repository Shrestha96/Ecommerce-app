from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
#importing forms from application
from scorptec.forms import UserForm, UserDetailForm,CustomRegisterForm
# importing user model
from django.contrib.auth.models import User
from scorptec.models import Product, Category, Order, OrderProduct,Favourite,UserDetail
from django.contrib import messages


from django.http import JsonResponse

import json
# importing uuid for transaction id
import uuid
#importing login required decorator
from django.contrib.auth.decorators import login_required

#importing send email package
from django.core.mail import send_mail
# Create your views here.
#view for home page
def index(request):
    return render(request,'scorptec/index.html')

#view for product Page
def product(request):
    return render(request,'scorptec/products.html')

#view for about page
def about(request):
    return render(request,'scorptec/about.html')

#view for contact page
def contact(request):
    if request.method == "POST":
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message_subject = request.POST['message-subject']
        message = request.POST['message']

        send_mail(
            message_subject,#Subject
            message,#message
            message_email,#from Email
            ['grouplearning7@gmail.com'],#to email
        )
        messages.success(request,"Thank you for Contacting us!")
        return render(request,'scorptec/contact.html')
    else:
        return render(request,'scorptec/contact.html')





#View for privacy policy
def policy(request):
    return render(request,'scorptec/policy.html')

#View for Terms and conditions
def terms(request):
    return render(request,'scorptec/terms.html')

#view for login or signup Page
def register(request):
    register_form = CustomRegisterForm()

    if request.method == "POST":
        register_form = CustomRegisterForm(data=request.POST)

        if register_form.is_valid():
            register_form.save()

            messages.success(request, 'Your Account Has been registered')
            return redirect('scorptec:login')

    return render(
        request,
        'scorptec/register.html',
        {'register_form': register_form}
    )


"""
def register(request):

    registered = False
    form = UserForm()
    user_detail_form = UserDetailForm()

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        detail_form = UserDetailForm(data = request.POST)

        if user_form.is_valid() and detail_form.is_valid():
            user =user_form.save()
            user.set_password(user.password)
            user.save()

            detail = detail_form.save(commit = False)
            detail.user = user
            detail.save()

            messages.success(request,'Your Account Has been registered')

            registered = True
        else:
            print(user_form.errors, detail_form.errors)


    return render(request, 'scorptec/register.html',{'form':form,'user_detail_form': user_detail_form})
"""
#login views
def loginPage(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"Username Doesn't exist!!!")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            messages.success(request,'Your Account Has been logged in.')
            return redirect('scorptec:userhome')
        else:
            messages.error(request,'Username or password incorrect!!!')

    return render(request,'scorptec/login.html')


#creating logout views
def logoutUserProfile(request):
    logout(request) #logs out the user
    return redirect('scorptec:login') #returns to login page

#view for user home Page
@login_required()
def userhome(request):
    #getting all products from database
    products = Product.objects.all()
    #starting of codes for showing no_of0-favaourites and no_of cart_items
    #retreiveing no of items in cart and favourite
    user = request.user
    order, created = Order.objects.get_or_create(user = user, order_finalised =False)
    cart_items = order.cart_items
    #retreiveing no_of items in favorite
    no_of_favourites = Favourite.objects.filter(user = user).count()
    #end of the query
    context = {'products':products,'order':order, "cart_items":cart_items, "no_of_favourites":no_of_favourites}
    return render(request,'scorptec/userhome.html',context)



#creating a view to update item
def updateItem(request):
    #loading the json data passsed through fetch api
    data = json.loads(request.body)
    productId =data['productId']
    action = data['action']

    #getting logged in customer
    cust = request.user
    #getting product data from the button
    product =Product.objects.get(id = productId)

    #reference from
    #https://www.kite.com/python/docs/django.db.models.QuerySet.get_or_create
    #creaing order of the user if it doesn't exist
    #getting order if exist with order_finalised is false
    order, created = Order.objects.get_or_create(user = cust, order_finalised = False)
    orderProduct, created = OrderProduct.objects.get_or_create(order = order,product= product)

    #adding product and increasing the number of items by 1
    if action == "add":
        orderProduct.no_of_items = (orderProduct.no_of_items +1)
        messages.success(request,'Successfully added the item ' + orderProduct.product.product_name + ' to cart')
    #deleting the product or decreasing the no of product by 1
    elif action== "remove":
        orderProduct.no_of_items = (orderProduct.no_of_items -1)
        messages.error(request,'Removed 1 quantity of ' + orderProduct.product.product_name + ' from cart', extra_tags='alert alert-danger')
    #saving the data in database
    orderProduct.save()
    #deleting the product from orderproduct model if no _of items is 0
    if orderProduct.no_of_items <= 0:
        orderProduct.delete()


    return JsonResponse("Item was added", safe =False)


#cart view rendering
@login_required()
def myCart(request):
    user = request.user
    order, created = Order.objects.get_or_create(user = user, order_finalised =False)
    products = order.orderproduct_set.all()
    #cart_items
    cart_items = order.cart_items
    #favourite Items
    no_of_favourites = Favourite.objects.filter(user = user).count()
    return render(request,'scorptec/my_cart.html', {'user':user, 'products':products, 'order':order,"cart_items":cart_items,"no_of_favourites":no_of_favourites})


#creating checkout view
@login_required()
def checkout(request):
    user = request.user
    order, created = Order.objects.get_or_create(user = user, order_finalised =False)
    products = order.orderproduct_set.all()
    #cart_items
    cart_items = order.cart_items
    #favourite Items
    no_of_favourites = Favourite.objects.filter(user = user).count()
    return render(request,'scorptec/checkout.html', {'user':user, 'products':products, 'order':order, "cart_items":cart_items, "no_of_favourites":no_of_favourites})

#view to finalise the order and process it
def orderProcess(request):
    #loading the json data passsed through fetch api
    data = json.loads(request.body)
    transaction_id = uuid.uuid4() #creating a unique transaction id using UUID
    #getting the logged in user
    user = request.user
    #getting the order created by usern with order_finalised false
    order, created = Order.objects.get_or_create(user = user, order_finalised =False)
    #getting total from the json response from fetch API
    total = float(data['total'])
    order.transaction_id = transaction_id

    #to confirm the total from fornt end equals to backend

    if total == float(order.cart_total):
        order.order_finalised =True
        messages.success(request,'Thanks for Purchasing from our store.')
    order.save() #saving the order
    return JsonResponse('Payment Complete', safe =False)



def updateFavourite(request):
    #loading the json data passsed through fetch api
    data = json.loads(request.body)
    productId =data['productId']
    action = data['action']
    #getting the logged in user
    cust = request.user
    #getting product id and details of from the button clicked
    product =Product.objects.get(id = productId)
    #reference from
    #https://www.kite.com/python/docs/django.db.models.QuerySet.get_or_create
    #creaing order of the user if it doesn't exist
    #getting order if exist with order_finalised is false
    favourite, created = Favourite.objects.get_or_create(user = cust,product= product)

    if action=="add":
        messages.success(request,'Added ' + product.product_name + ' to your favorite list')
    if action=="remove":
        favourite.delete()
        messages.error(request,'Removed ' + product.product_name + ' from your favorite list!')
    return JsonResponse("Items Added in Favourties", safe =False)

@login_required()
def favourite(request):
    #getting the logged in user
    user =request.user
    #getting products in favouritye of particular user
    products = user.favourite_set.all()

    #retreiveing no of items in cart and favourite
    order, created = Order.objects.get_or_create(user = user, order_finalised =False)
    cart_items = order.cart_items
    #favourite Items
    no_of_favourites = Favourite.objects.filter(user = user).count()
    return render(request,'scorptec/favourite.html', {'products':products,"cart_items":cart_items,"no_of_favourites":no_of_favourites})


@login_required()
def userProfile(request):
    user = request.user
    #retreiveing no of items in cart and favourite
    order, created = Order.objects.get_or_create(user = user, order_finalised =False)
    cart_items = order.cart_items
    #favourite Items
    no_of_favourites = Favourite.objects.filter(user = user).count()
    #getting order history for user
    user_orders = Order.objects.filter(user = user, order_finalised =True)
    if user.is_superuser:
        userdetail =UserDetail.objects.get(user = user)
        return render(request, "scorptec/my_account.html",{'user':user,
        'user_orders':user_orders,"cart_items":cart_items,"no_of_favourites":no_of_favourites,'userdetail':userdetail})

    else:
        userdetail =UserDetail.objects.get(user = user)
        return render(request, "scorptec/my_account.html",{'user':user, 'userdetail':userdetail,'user_orders':user_orders,"cart_items":cart_items,"no_of_favourites":no_of_favourites})

@login_required()
def updateUser(request):
    #getting logged in user
    user = request.user
    #retreiveing no of items in cart and favourite
    order, created = Order.objects.get_or_create(user = user, order_finalised =False)
    cart_items = order.cart_items
    #favourite Items
    no_of_favourites = Favourite.objects.filter(user = user).count()
    # checking the instance of userdetail in userdetail model
    userdetail =UserDetail.objects.get(user = user)
    #getting the data from userdetail form
    user_detail_form = UserDetailForm(instance = userdetail)
    #when user detaiil form is updated
    if request.method == "POST":
        detail_form = UserDetailForm(data = request.POST, instance = userdetail)
        #checking if the passed values are valid
        if detail_form.is_valid():
            #saving data
            detail = detail_form.save(commit = False)
            #defining the relationship
            detail.user = user
            detail.save()

            messages.success(request,'Your Account Has been updated')

            return redirect('scorptec:user_profile')
        else:
            print(detail_form.errors)
            message.error(request,'Your Account cannot be updated.')



    return render(request, 'scorptec/update_user.html',{'user_detail_form': user_detail_form,'user':user,"cart_items":cart_items,"no_of_favourites":no_of_favourites})

@login_required()
def search(request):
    #getting all products from database
    products = Product.objects.all()
    #retreiveing no of items in cart and favourite
    user = request.user
    order, created = Order.objects.get_or_create(user = user, order_finalised =False)
    cart_items = order.cart_items
    #favourite Items
    no_of_favourites = Favourite.objects.filter(user = user).count()
    results = None
    #getting the input from search field
    q = request.GET.get('q')
    #getting any data using filter that contains speicific given value
    if request.method == 'GET' and q:
        results = Product.objects.filter(product_name__icontains=q)
    context = {
        'results': results,
        'q': q,
        "cart_items":cart_items,
        "no_of_favourites":no_of_favourites

    }
    return render(request, 'scorptec/search.html', context)
