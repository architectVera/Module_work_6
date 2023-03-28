from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from datetime import date

from django.contrib.auth import get_user_model, authenticate
from django.db.models import Q

from api.permissions import UserPermission
from kinohall.models import Movie, Hall, Session
from kinohall.serializers import MovieSerializer, HallSerializer, SessionSerializer

from user.models import UserModel
from user.serializers import UserModelSerializer


User = get_user_model()

"""AUTHENTICATION"""


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


"""MOVIE"""


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    permission_classes = [IsAuthenticatedOrReadOnly]


class HallViewSet(ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        if Hall.objects.filter(name=name).exists():
            return Response({'detail': 'This name already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)


"""SESSION"""


class SessionViewSet(viewsets.ModelViewSet):
    serializer_class = SessionSerializer
    queryset = Session.objects.all()

    def perform_create(self, serializer):
        """Called when creating a new session"""

        serializer.is_valid(raise_exception=True)
        self.validate_session(serializer.validated_data)
        serializer.save()

    def perform_update(self, serializer):
        """Called when updating an existing session"""

        session_id = self.kwargs['pk']
        serializer.is_valid(raise_exception=True)
        self.validate_session(serializer.validated_data, session_id=session_id)
        serializer.save()

    def validate_session(self, data, session_id=None):
        """Validate session data"""

        hall = data['hall']
        start_time = data['start_time']
        end_time = data['end_time']
        start_date = data['start_date']
        end_date = data['end_date']

        if start_date < date.today():
            raise ValidationError('Start date cannot be less than today.')

        if end_date < start_date:
            raise ValidationError('End date should be greater than or equal to start date.')

        existing_sessions = Session.objects.exclude(id=session_id).filter(
            Q(hall=hall),
            Q(start_date__lte=start_date, end_date__gte=start_date) | Q(start_date__lte=end_date,
                                                                        end_date__gte=end_date) | Q(
                start_date__gte=start_date, end_date__lte=end_date),
            Q(start_time__lte=start_time, end_time__gte=start_time) | Q(start_time__lte=end_time,
                                                                        end_time__gte=end_time) | Q(
                start_time__gte=start_time, end_time__lte=end_time),
        )

        if existing_sessions.exists():
            raise ValidationError('This hall is already reserved at this time or date.')

