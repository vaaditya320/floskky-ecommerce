from store.models import *



class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("session_key")
        if "session_key" not in request.session:
            cart = self.session["session_key"] = {}
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = int(quantity)
        if product_id in self.cart:
            self.cart[product_id] += product_qty  # Increment the quantity
        else:
            self.cart[product_id] = product_qty  # Set the quantity
        self.session.modified = True


    def __len__(self):
        return sum(1 for _ in self.cart)


    def get_prods(self):
        # get id from cart
        product_ids = self.cart.keys()
        # use id to look up products in db
        products = Product.objects.filter(id__in=product_ids)
        
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        
        self.cart[product_id] = product_qty  # Update the quantity
        self.session.modified = True
        
        return self.cart
        
        
    def delete(self, product):
        product_id = str(product)
        
        # delete from dict {"2":4} => this is cookie
        if product_id in self.cart:
            # self.cart.popitem()
            del self.cart[product_id]
            
        self.session.modified = True
        
    def cart_totals(self):
        # get product ids
        product_ids = self.cart.keys()
        # look up those keys in db models
        products = Product.objects.filter(id__in=product_ids)
        
        quantities = self.cart
        total = 0
        
        for key, value in quantities.items():
            # typecast str(key) into int coz its math now
            key = int(key)
            
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += product.sale_price * value
                    else:
                        total += product.price * value
                    
        return total
            
            