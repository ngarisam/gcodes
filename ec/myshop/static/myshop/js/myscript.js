$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 2,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 4,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 6,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})
$('.plus-cart').click(function(){
    
    var id=$(this).attr("pid").toString();
    var quantityid=document.getElementById("quantity"+id)

    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
        'prod_id':id
        },
        success:function(data){
            quantityid.innerText=data.quantity
            document.getElementById("amount").innerHTML=data.amount
            document.getElementById("totalplusvat").innerHTML=data.totalamount
    }
})
})



$('.minus-cart').click(function(){
 
    var id=$(this).attr("pid").toString();
    var quantityid=document.getElementById("quantity"+id)
    var eml=this.parentNode.children[2]

    
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id:id
        },
        success:function(data){
            quantityid.innerText=data.quantity
            document.getElementById("amount").innerHTML=data.amount
            document.getElementById("totalplusvat").innerHTML=data.totalamount



        }
    })
})


$('.remove-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var itemClass=".quantity"+id;
    var parentRow= $(itemClass).closest('.row')
    
    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id:id
        },
        success:function(data){
            location.reload()

        }
    })
})

$('.wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/updatewishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            location.reload()
           
        }
    })
})
$('.removewishlist').click(function(){
    var id=$(this).attr("pid").toString();
    var itemClass=".wishlist"+id;
   var parentRow= $(itemClass).closest('.row')

   parentRow.remove()
   $.ajax({
    type:"GET",
    url:"/removewishlist",
    data:{
        prod_id:id
    },
    success:function(data){
        location.reload()


    }
})
})

function validateForm() {
  var input = document.getElementById('searchInput');
  if (input.value.length < 2) {
    alert('Please enter at least two characters.');
    return false;
  }
  else{
    return true;
  }
}


