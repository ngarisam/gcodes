from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from . models import Product, Customer, Cart,Wishlist
from . forms import CustomerRegistrationForm,CustomerProfileForm
from django.db.models import Count,Q
from django.contrib import messages
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from fuzzywuzzy import fuzz

def home(request):
    return render(request,"myshop/home.html",locals())
def about(request):
    return render(request,"myshop/about.html")
def contact(request):
    return render(request,"myshop/contact.html")
def Category(request):
    return render(request,"myshop/category.html")

class CategoryView(View):
    def get(self,request,val):
        product=Product.objects.filter(category=val)
        title=Product.objects.filter(category=product[0].category).values('title')
        return render(request,"myshop/category.html",locals())
class ProductDetail(View):
    def get(self, request, pk):
        product=Product.objects.get(pk=pk)
        try:
            isWishlist=Wishlist.objects.get(product=product)
        except ObjectDoesNotExist:
            isWishlist=None
        return render(request, "myshop/product-detail.html", locals())
        
class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,"myshop/customerregistration.html", locals())
    def post(self, request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, "Your registration was susccessful")
        else:
            messages.warning(request, "An error occured during registration")

        return render(request,"myshop/customerregistration.html", locals())
class ProfileView(View):
    def get(self,request):
        if(request.user.is_authenticated):
            form=CustomerProfileForm
            return render(request, 'myshop/profile.html',locals())
        else:
            return redirect('login')
        
    def post(self, request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            mobile=form.cleaned_data['mobile']
            county=form.cleaned_data['county']
            reg=Customer(user=user,locality=locality,mobile=mobile,county=county)
            reg.save()  
            messages.success(request, "Successfully saved the data")
        else:
            messages.warning(request, "Unsuccessful, Kindly fill all the fields")
            
        return render(request, 'myshop/profile.html',locals())
def address(request):
    if(request.user.is_authenticated):
        add=Customer.objects.filter(user=request.user)
        return render(request,'myshop/address.html',locals())
    else:
        return redirect('login')
class UpdateAddress(View):
    def get(self, request,pk):
        if(request.user.is_authenticated):
            add=Customer.objects.get(pk=pk)
            form=CustomerProfileForm(instance=add)
            return render(request, 'myshop/updateAddress.html',locals())
        else:
            return redirect('login') 
    def post(self, request,pk):
        if(request.user.is_authenticated):
            form=CustomerProfileForm(request.POST)
            add=Customer.objects.get(pk=pk)
            if form.is_valid():
                add.user=request.user
                add.name=form.cleaned_data['name']
                add.locality=form.cleaned_data['locality']
                add.mobile=form.cleaned_data['mobile']
                add.county=form.cleaned_data['county']
                
                add.save()  
                messages.success(request, "Successfully saved the data")
            else:
                messages.warning(request, "Unsuccessful, Kindly fill all the fields")
                
            return redirect('address')
        else:
            return redirect('login') 
def add_to_cart(request):
    if(request.user.is_authenticated):
        user=request.user
        prod_id=request.GET.get('prod_id')
        product=Product.objects.get(id=prod_id)
        #checking whether product already exists
        cartcheck=Cart.objects.filter(product=product)

        if len(cartcheck)==0:
            Cart(user=user,product=product).save()
        return redirect('/cart')
    else:
        return redirect('login')
def show_cart(request): 
    if(request.user.is_authenticated):
        user=request.user
        prod_id=request.GET.get('prod_id')
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount=amount+value
            totalamount=amount+70
    
    #also check wishlist
        return render(request,"myshop/addtocart.html", locals())
    else:
        return redirect('login')
def plus_cart(request):
 if(request.method=='GET'):
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0
        cart=Cart.objects.filter(user=request.user)
        for p in cart:
            amount+=p.quantity*p.product.discounted_price
        totalamount=amount+70
        data={
            'amount':amount,
            'totalamount':totalamount,
            'quantity':c.quantity   
            }
        return JsonResponse(data)
def minus_cart(request):
    if(request.method=='GET'):
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        if(c.quantity<1):
            c.quantity=1
        c.save()
        amount=0
        cart=Cart.objects.filter(user=request.user)
        for p in cart:
            amount+=p.quantity*p.product.discounted_price
        totalamount=amount+70
        data={
            'amount':amount,
            'totalamount':totalamount,
            'quantity':c.quantity   
            }
        return JsonResponse(data)
def remove_cart(request):
    data={}
    if(request.user.is_authenticated):
        if(request.method=='GET'):
            prod_id=request.GET['prod_id']
            c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            c.delete()
            
            user=request.user
            prod_id=request.GET.get('prod_id')
            cart=Cart.objects.filter(user=user)
            amount=0
        for p in cart:
            amount+=p.quantity*p.product.discounted_price
            totalamount=amount+70
            cart_count=len(cart)
            data={
                'amount':amount,
                'totalamount':totalamount,
                'quantity':p.quantity,
                'cart_count':cart_count
                }
    
        return JsonResponse(data)
        
    else:
        return redirect('login')
    
class Checkout(View):
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        totalamount=0
        for p in cart_items:
            totalamount+=p.quantity*p.product.discounted_price
        return render(request, "myshop/checkout.html", locals())
def wishlist(request):
    
    if(request.user.is_authenticated):
        user=request.user
        prod_id=request.GET.get('prod_id')
        wishlist=Wishlist.objects.filter(user=user)
        amount=0
        for p in wishlist:
            value=p.product.discounted_price
            amount=amount+value
            totalamount=amount+70
        return render(request,"myshop/wishlist.html", locals())
    else:
        return redirect('login')
def updatewishlist(request):
    if(request.user.is_authenticated):
        prod_id=request.GET.get('prod_id')
        product=Product.objects.get(id=prod_id)
        try:
            wishlist=Wishlist.objects.get(Q(user=request.user) & Q(product=prod_id))
        except ObjectDoesNotExist:
            wishlist=None
        if(wishlist is None):
            wishlist= Wishlist(user=request.user, product=product, wishlist_count=True)
            wishlist.save()
        else:
            wishlist.delete()
        data={}
        return JsonResponse(data)
    else:
        return redirect('login')
def removeWishlist(request):
    if(request.user.is_authenticated):
        prod_id=request.GET.get('prod_id')
        product=Product.objects.get(id=prod_id)
       
        try:
            wishlist=Wishlist.objects.filter(Q(user=request.user) & Q(product=product))
        except ObjectDoesNotExist:
            wishlist=None
        if(wishlist is not None):
            wishlist.delete()
        #check the remaining count
        wishlist=Wishlist.objects.filter(user=request.user)
        wishlist_count=len(wishlist)
        data={'wishlist_count':wishlist_count}
        return JsonResponse(data)   
    else:
        return redirect('/login')

def search(request):
    if(request.method=='GET'):
        query=request.GET['searchInput']
        allproducts=Product.objects.all()

        product=[]
        for prod in allproducts:
            title_similarity_ratio=fuzz.ratio(query, prod.title)
            category_similarity_ratio=fuzz.ratio(query, prod.category)
            average_similarity_ration=(title_similarity_ratio+category_similarity_ratio)/2

            if(average_similarity_ration>=15):
                product.append(prod)
        return render(request,"myshop/search.html",locals())