from .cart import Cart

# creating context processors so that cart work on all site

def cart(request):
    # return the default data from our cart
    return {'cart':Cart(request)}