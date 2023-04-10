from store.models import Product
from decimal import Decimal


class Basket():
    """
    A base Basket class, providing some default behaviors that 
    can be inherited or overrided, as necessary.
    """

    def __init__(self, request) -> None:
        self.session = request.session
        basket = self.session.get('skey')

        if 'skey' not in request.session:
            basket = self.session['skey'] = {}

        self.basket = basket  # by doing this we give access to this variable from outer functions
        # print(self.basket)

    def save(self):
        self.session.modified = True

    def add(self, product, qty):
        """
        Adding and updating the users basket session data
        """
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'price': str(product.price), 'qty': int(qty)}
        # print("BASKET: ", self.basket)

        self.save()

    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        return sum(item['qty'] for item in self.basket.values())
    
    def __iter__(self):
        """
        Collect the product_id in the session data to query the database
        and return products
        """
        product_ids = self.basket.keys()
        # print("PRODUCT ID: ", product_ids)
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def get_total_price(self):
        """
        Get the basket data and count the total price of items
        """
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())
    
    def update(self, product, qty):
        """
        Update item from session data
        """
        product_id = str(product)

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty

        self.save()

    def delete(self, product):
        """
        Delete values from session data
        """
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            self.save()




