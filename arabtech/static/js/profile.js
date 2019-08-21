
$(document).ready(function(){
    $('#invoice').on('submit','.invoice-update', function(){
        $.ajax({
            url:'invoice/',
            type:'get',
            dataType:'json',
            beforeSend : function(){
                $('#cart').modal('show')
            },
            success : function(data){
                $('#cart .modal-content').html(data.cart)
            }
        })
    })

})

