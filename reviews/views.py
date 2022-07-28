from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import User
import jwt
from rest_framework import status
from .serializers import ReviewSerializer

# Create your views here.
class RivewView (APIView):
    def post (self, request):
        #로그인한 사람의 토큰이 맞는지를 보고, 그에 맞는 상점에 알맞는 리뷰를 작성합니다.
        #토큰이 문제가 있으면 벤때립니다.

            try:
                token = jwt.decode(request.META['HTTP_AUTHORIZATION'][7:],"1234", algorithm="HS256")
                userId = int(User.objects.filter(userId = token['userId']).values()[0]["id"])
                print(userId)
            except:
                print("err!")
                return Response({"status" : "Token Err!"}, status=status.HTTP_400_BAD_REQUEST)

            reviewSerializer = ReviewSerializer(data = {"shopId_id":request.data["shopId"],"userId_id":userId,"comment":request.data["comment"], "star":request.data["star"]})
            if reviewSerializer.is_valid():
                reviewSerializer.save()
                return Response({"status" : "Posting!", "data" : request.data}, status=status.HTTP_201_CREATED)
            return Response("Not Posted!!!")


    def get(self, request):
        return Response("This is review API!!!!")