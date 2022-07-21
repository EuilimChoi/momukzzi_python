from django.urls import path
from .views import CrawlingView

urlpatterns =[
    path('',CrawlingView.as_view()),
]

