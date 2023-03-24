from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.contrib.auth import get_user_model, authenticate

from user.models import UserModel
from user.serializers import UserModelSerializer

from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response

User = get_user_model()


class UsersViewSet(ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly, UserPermission]


class RegisterView(APIView):
    def post(self, request):
        serializer = UserModelSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'username': user.username, 'email': user.email})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    authentication_classes = []  # remove TokenAuthentication
    permission_classes = [] # remove IsAuthenticated


class LoginView(APIView):
    def post(self, request):
        print("post login invoked")

        user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'username': user.username, 'email': user.email})
        return Response({'error': 'Invalid credentials'}, status=400)

    authentication_classes = []  # remove TokenAuthentication
    permission_classes = []  # remove IsAuthenticated


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        print("post logout invoked")
        token = request.auth
        token.delete()
        return Response({'message': 'Successfully logged out'})
