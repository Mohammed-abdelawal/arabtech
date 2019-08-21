$(document).ready(function(){
    check_Nums("hello")
    setInterval(function(){ check_Nums("Hello"); }, 10000);
})

function check_Nums(){
    
}


function delete_all() {
    $.ajax({
        url: '/cart/delete',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            $('#cart').modal('hide')
        }
    })

}



function add_item(product_name,pk){
    $.ajax({
        url:'/cart/additem/'+pk,
        type:'post',
        dataType:'json',
        success : function(data){
            if (data.respond == 0){
                alert('The '+product_name+' already in your cart')
            }
        }
    })
    
}


function cart_order(){
    $.ajax({
        url:'/cart/order/',
        type:'get',
        dataType:'json',
        success : function(data){
            if (data.respond == 0){
                alert('What about add some products to the cart')
            }else{
                window.location.pathname = 'user/orders/'
            }
        }
    })
}





function add_wish_item(pk,product_name){
    $.ajax({
        url:'/wishlist/additem/'+pk,
        type:'get',
        dataType:'json',
        success : function(data){
            if (data.respond == 0){
                alert('The '+product_name+' already in your Wishlist');
            }
        }
    })
    
}
