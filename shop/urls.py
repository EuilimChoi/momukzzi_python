from django.urls import path
from .views import ShopView

urlpatterns =[
    path('<int:shopid>',ShopView.as_view()),
]

