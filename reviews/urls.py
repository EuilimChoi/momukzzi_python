from django.urls import path
from .views import RivewView

urlpatterns =[
    path('',RivewView.as_view()),
]

