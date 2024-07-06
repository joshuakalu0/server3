
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from authDbs.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# Serializers
from authDbs.serializer import MyTokenObtainPairSerializer,UserSerializer,RegisterSerializer

from organisation.models  import Organisation



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        # token =  super().post(request, *args, **kwargs)
        token= {}
        print(token,'hello')
        return token


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


    def post(self, request, *args, **kwargs):
        statu =  self.create(request, *args, **kwargs)
        if statu.status_code == 201:
            user = User.objects.get(email = request.data['email'])
            token = TokenObtainPairSerializer.get_token(user)
            # org = Organisation.objects.create(name=f'{self.firstName}`s organisation')
            # user.organisation.add(org)

            return Response({
                "status": "success",
                "message": "Registration successful",
                "data": {
                      "accessToken":str(token),
                    "user": {
                         "userId": user.userId,
                         "firstName": user.firstName,
                         "lastName": user.lastName,
                         "email": user.email,
                         "phone": user.phone,
                         }
                    }
                },status=status.HTTP_201_CREATED)


        return Response({
            "status": "Bad request",
            "message": "Registration unsuccessful",
            "statusCode": 400
            },status=status.HTTP_400_BAD_REQUEST)



