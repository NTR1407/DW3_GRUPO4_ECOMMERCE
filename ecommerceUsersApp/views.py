from django.conf import settings
from django.contrib.auth.models import User
# from django.views.generic.base import View
from .serializers import ecommerceUserSerializer
from .models import ecommerceUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# Create your views here.

class VerifyTokenView(TokenVerifyView):

    def post(self, request, *args, **kwargs):
        token = request.data['token']
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            valid_data = tokenBackend.decode(token,verify=False)
            serializer.validated_data['UserId'] = valid_data['user_id']

        except TokenError as e:
            raise InvalidToken(e.args[0])
            
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

        # put y post llevan body
        # get y delet parametros por url
        # pip freezer > requirements.txt

# Usando decoradores y funciones
@api_view(['GET','POST'])
def user_information_view(request):

    if request.method == 'GET':
        users = ecommerceUser.objects.all()
        users_serializer = ecommerceUserSerializer(users, many = True)
        return Response(users_serializer.data, status = status.HTTP_200_OK)

    elif request.method == 'POST':
        user_serializer = ecommerceUserSerializer(data = request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'message': 'Usuario creado correctamente!'}, status = status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def user_detail_view(request, pk=None):
    user = User.objects.filter(id = pk).first()

    if user:

        if request.method == 'GET':
            user_serializer = ecommerceUserSerializer(user)
            return Response(user_serializer.data, status = status.HTTP_200_OK)

        elif request.method == 'PUT':
            user_serializer = ecommerceUserSerializer(user, data = request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status = status.HTTP_200_OK)
            return Response(user_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            user.delete()
            return Response( {'message': 'Usuario eliminado correctamente!'}, status = status.HTTP_200_OK )
    
    return Response( {'message': 'No se ha encontrado un usuario con estos datos'}, status = status.HTTP_400_BAD_REQUEST )
# Usando una clase
# class UserInformationView(APIView):

#     def get(self, request):
#         users = ecommerceUser.objects.all()
#         users_serializer = ecommerceUserSerializer(users, many = True)
#         return Response(users_serializer.data, status=status.HTTP_100_CONTINUE)

    

    # def get(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     print(serializer)

    #     if serializer.is_valid():
    #         # telephone = serializer.validated_data.get('telephone')
    #         return Response(serializer.validated_data, status=status.HTTP_200_OK)

    #     else:
    #         return Response(
    #             serializer.errors,
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    # def post(self, request, *args, **kwargs):
    #     # serializer = self.get_serializer(data=request.data)
    #     data = request.data
    #     print(data)

    #     return Response(data, status=status.HTTP_200_OK)
        
            