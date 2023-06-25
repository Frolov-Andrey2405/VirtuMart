from products.models import Basket


def baskets(request):
    """
    The baskets function is a context processor that adds the user's baskets to
    the template context. It does this by checking if the user is authenticated, and
    if so, it returns all of their baskets. If not, it returns an empty list.
    """
    user = request.user
    return {'baskets': Basket.objects.filter(user=user) if user.is_authenticated else []}
