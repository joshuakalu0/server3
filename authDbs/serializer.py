from authDbs.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from organisation.models  import Organisation


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims to the token
        token['first_name'] = user.firstName
        token['first_name'] = user.lastName
        token['email'] = user.email
        token['phone'] = user.phone

        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User

        fields = ('firstName', 'lastName', 'email', 'phone', 'password')

    # def validate(self, attrs):
    #     if attrs['password'] != attrs['password2']:
    #         raise serializers.ValidationError({"password": "Password fields didn't match."})

    #     return attrs

    def create(self, validated_data):
        user = User.objects.create(
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName'],
            email=validated_data['email'],
            phone=validated_data['phone']
        )

        user.username = validated_data['email']
        user.set_password(validated_data['password'])
        user.save()
        org = Organisation.objects.create(name=f'{self.firstName}`s organisation')
        org.save()
        user.organisation.add(org)




        # Return the created user
        return user





class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


# return Response({
#                 "status": "success",
#     "message": "Registration successful",
#     "data": {
#       "accessToken":token,
#       "user": {
# 	      "userId": user.userId,
# 	      "firstName": user.firstName,
# 				"lastName": user.lastName,
# 				"email": user.email,
# 				"phone": user.phone,
#       }
#     }
#             })