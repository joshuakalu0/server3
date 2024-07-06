
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
from django.db.models import Q


# Serializers
from authDbs.serializer import MyTokenObtainPairSerializer,UserSerializer,RegisterSerializer
from organisation.serializer import OrgSerializer
from organisation.models  import Organisation



class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'userId'

    def get(self, request, *args, **kwargs):
        userId = kwargs['userId']

        user = User.objects.filter(
            Q(userId=userId)|
            Q(pk=userId)
        )
        if user:
            print(user)
            return Response({
                "status": "success",
                "message": "<message>",
                "data": {

                         "userId": user[0].userId,
                         "firstName": user[0].firstName,
                         "lastName": user[0].lastName,
                         "email": user[0].email,
                         "phone": user[0].phone,

                    }
                },status=status.HTTP_200_OK)


        # return super().get(request, *args, **kwargs)

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




class Orglistview(generics.ListCreateAPIView):
    queryset = Organisation.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes =(JWTAuthentication,)
    serializer_class = OrgSerializer

    def get(self, request, *args, **kwargs):
        orgs = Organisation.objects.filter(user__in=[request.user,]).values()


        if orgs:
            print(orgs)
            return Response({
                "status": "success",
                "message": "<message>",
                "data": {"organisations": orgs

                    }
                },status=status.HTTP_200_OK)


        return super().get(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        org = Organisation.objects.create(
            name=request.data['name'],
            description=request.data['description'],
        )
        org.save()
        request.user.organisation.add(org)

        return Response({
            "status": "success",
            "message": "<message>",
            "data": {
                "orgId": org.orgId,
                "name": org.name,
                "description": org.description,
                }
            })








class OrgDetailView(generics.RetrieveAPIView):
    serializer_class = OrgSerializer
    queryset = Organisation.objects.all()


    def get(self, request, *args, **kwargs):
        orgId = kwargs['orgId']

        user = Organisation.objects.filter(
            Q(orgId=orgId)|
            Q(pk=orgId)
        )
        if user:
            print(user)
            return Response({
                "status": "success",
                "message": "<message>",
                "data": {

                         user.values()

                    }
                },status=status.HTTP_200_OK)


        # return super().get(request, *args, **kwargs)


class addOrgDetailView(generics.RetrieveAPIView):
    serializer_class = OrgSerializer
    queryset = Organisation.objects.all()


    def get(self, request, *args, **kwargs):
        orgId = kwargs['orgId']

        orgs = Organisation.objects.filter(
            Q(orgId=orgId)|
            Q(pk=orgId)
        )
        request.user.organisation.add(orgs[0])
        if orgs:
            print(orgs)
            return Response({
                "status": "success",
                "message": "<message>",
                "data": {

                         orgs.values()

                    }
                },status=status.HTTP_200_OK)