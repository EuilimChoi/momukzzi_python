
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class ShopView (APIView):
    def get (self, request):
        print(request.shopid)
        return Response("This is shop API!!!!")