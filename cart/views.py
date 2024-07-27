from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.

def cart_summary(request):
    
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_totals()
     
    
    
    return render(request, "cart_summary.html", {"products" : cart_products, "quantity" : quantities, "totals" : totals})

def cart_add(request):
    cart = Cart(request)
    # Test for POST
    if request.method == 'POST':
        # Get details
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty"))
        # Check if product is in DB
        product = get_object_or_404(Product, id=product_id)
        # Save the product to session storage
        cart.add(product=product, quantity=product_qty)   
        messages.success(request, "Item Added Successfully")  
        # get cart quantity
        cart_quantity = cart.__len__()
        
        
        
           
        # Return the response
        response = JsonResponse({ "qty" : cart_quantity})
        return response
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

def cart_delete(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        # Get details
        product_id = int(request.POST.get("product_id"))
        
        cart.delete(product=product_id)
        messages.success(request, "Item Deleted Successfully")
        
        # Return the response
        response = JsonResponse({"deleted-product": product_id})
        return response
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
    

def cart_update(request):
    cart = Cart(request) 
    
    if request.method == 'POST':
        # Get details
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty"))
        
        cart.update(product=product_id, quantity=product_qty)
        messages.success(request, "Updated Successfully")
        
        # Return the response
        response = JsonResponse({"qty": product_qty})
        return response
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
