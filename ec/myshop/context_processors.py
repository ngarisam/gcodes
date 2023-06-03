from .models import Cart, Wishlist
from django.db.models import Sum
def total_quantity_count(request):
    if(request.user.is_authenticated):
        cart_count=Cart.objects.filter(user=request.user).aggregate(total_quantity=Sum('quantity'))
        iswishlist=Wishlist.objects.filter(user=request.user).count()
        return {'cart_count':cart_count, 'iswishlist':iswishlist,}
    else:
         return {}