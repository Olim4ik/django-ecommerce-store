from store_basket.basket import Basket


def basket(request):
    # print("DATA:", Basket(request))
    return {'basket': Basket(request)}