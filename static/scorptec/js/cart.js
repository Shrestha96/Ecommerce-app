var updateCartButtons = document.getElementsByClassName('update-btn')
//looping Through each update buttons in our user home page
for(var i = 0; i < updateCartButtons.length; i++){
  updateCartButtons[i].addEventListener('click',function(){
    var productId = this.dataset.product
    var action = this.dataset.action
    console.log('productId:', productId,'action:', action)
    console.log(user)
    updateUserOrder(productId,action)
  })
}


function updateUserOrder(productId,action){
  var url = '/update_item/'
  //https://www.brennantymrak.com/articles/fetching-data-with-ajax-and-django.html
  //fetch api to send data using POST method
  fetch(url, {
    method:'POST',
    headers:{
      'Content-Type': 'application/json',
      'X-CSRFToken':csrftoken,
    },
    body: JSON.stringify({'productId':productId,'action':action})
  })
  .then((response)=>{
    return response.json()
  })
  .then((data)=>{
    console.log('data:',data)
    location.reload()
  })
}
