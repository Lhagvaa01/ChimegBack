from django.utils.timezone import now

from invoice.models import InfoProduct


class DiscountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check all products and reset expired discounts
        InfoProduct.objects.filter(
            TCDiscountEndDate__lt=now()
        ).update(TCDiscountPrice=0, TCDiscountEndDate=None)

        response = self.get_response(request)
        return response