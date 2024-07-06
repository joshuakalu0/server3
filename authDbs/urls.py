from django.urls import path
from authDbs.views import RegisterView,TokenObtainPairView

urlpatterns = [
    path('register',RegisterView.as_view()),
    path('login',TokenObtainPairView.as_view()),

]
