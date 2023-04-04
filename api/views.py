import datetime
from datetime import datetime
import time

from django.http import Http404
from rest_framework import viewsets, generics
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from datetime import date

from django.utils import timezone
from django.contrib.auth import get_user_model, authenticate
from django.db.models import Q, Sum

from kinohall.models import Movie, Hall, Session
from kinohall.serializers import MovieSerializer, HallSerializer, SessionSerializer

from order.models import Purchase
from order.serializers import PurchaseSerializer

from user.models import UserModel
from user.serializers import UserModelSerializer

from api.permissions import IsOwnerOrAdmin


User = get_user_model()

"""AUTHENTICATION"""


class UsersViewSet(ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [IsAdminUser]


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
    permission_classes = [IsAdminUser]


class HallViewSet(ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        if Hall.objects.filter(name=name).exists():
            return Response({'detail': 'This name already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        hall_id = instance.pk

        purchases_with_hall = Purchase.objects.filter(session__hall__id=hall_id, paid=True)
        if purchases_with_hall.exists():
            return Response({'error': 'You cannot update this hall because some tickets have already been sold.'},
                            status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Called when deleting an existing hall"""

        instance = self.get_object()
        hall_id = instance.pk
        purchases_with_hall = Purchase.objects.filter(session__hall__id=hall_id, paid=True)

        if self.request.user.is_staff and not purchases_with_hall.exists():
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'You cannot delete this hall because some tickets have been sold'},
                            status=status.HTTP_400_BAD_REQUEST)


"""SESSION"""


class SessionViewSet(viewsets.ModelViewSet):
    serializer_class = SessionSerializer
    queryset = Session.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Called when creating a new session"""
        permission_classes = [IsAdminUser]

        serializer.is_valid(raise_exception=True)
        self.validate_session(serializer.validated_data)
        serializer.save()

    def update(self, request, *args, **kwargs):
        """Called when updating an existing session"""

        permission_classes = [IsAdminUser]

        session_id = kwargs['pk']
        purchases_with_session = Purchase.objects.filter(session_id=session_id, paid=True)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.validate_session(serializer.validated_data, session_id=session_id)

        if not request.user.is_staff or purchases_with_session.exists():
            return Response({'error': 'You cannot update this session because some tickets have been sold'},
                            status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)

        return Response(serializer.data)

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

    def destroy(self, request, *args, **kwargs):
        """Called when deleting an existing session"""

        permission_classes = [IsAdminUser]

        instance = self.get_object()
        session_id = instance.pk
        purchases_with_session = Purchase.objects.filter(session_id=session_id, paid=True)

        if self.request.user.is_staff and not purchases_with_session.exists():
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'You cannot delete this session because some tickets have been sold'},
                            status=status.HTTP_400_BAD_REQUEST)


class SessionTodayListAPIView(ListAPIView):

    serializer_class = SessionSerializer
    queryset = Session.objects.filter(start_date__lte=timezone.now().date(), end_date__gte=timezone.now().date())
    paginate_by = 9
    permission_classes = [IsAuthenticatedOrReadOnly]


class SessionTomorrowListAPIView(ListAPIView):

    serializer_class = SessionSerializer
    queryset = Session.objects.filter(start_date__lte=timezone.now().date() + timezone.timedelta(days=1),
                                      end_date__gte=timezone.now().date() + timezone.timedelta(days=1))
    paginate_by = 9
    permission_classes = [IsAuthenticatedOrReadOnly]




"""PURCHASE"""


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def purchase_session_api(request, pk):
    session = get_object_or_404(Session, pk=pk)
    hall_capacity = session.hall.seats
    remaining_capacity = 0

    quantity = int(request.data.get('quantity'))
    showdata = timezone.datetime.strptime(request.data.get('showdata'), '%Y-%m-%d').date()
    tickets_sold = Purchase.objects.filter(showdata=showdata, session=session).aggregate(Sum('quantity'))['quantity__sum'] or 0
    remaining_capacity = hall_capacity - tickets_sold
    current_time = timezone.localtime(timezone.now()).time()

    if showdata < timezone.now().date():
        return Response({'error': 'Show date cannot be less than today'}, status=status.HTTP_400_BAD_REQUEST)

    if showdata == timezone.now().date() and current_time > session.start_time:
        return Response({'error': 'The session has already started. Please choose another session or day'}, status=status.HTTP_400_BAD_REQUEST)

    if showdata > session.end_date:
        return Response({'error': 'You can only select the dates within which films are shown'}, status=status.HTTP_400_BAD_REQUEST)

    if remaining_capacity < quantity:
        return Response({'error': f"Only {remaining_capacity} tickets available for purchase"}, status=status.HTTP_400_BAD_REQUEST)

    if request.user.wallet < session.price * quantity:
        return Response({'error': "You don't have enough money in your account to buy. Please, check your balance"}, status=status.HTTP_400_BAD_REQUEST)

    if quantity <= remaining_capacity:
        purchase = Purchase.objects.create(user=request.user, session=session, quantity=quantity, showdata=showdata)
        request.user.wallet -= session.price * quantity
        request.user.save()
        return Response({'success': True, 'url': purchase.get_absolute_url()}, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_400_BAD_REQUEST)


class PurchaseSessionAPIView(APIView):
    """ This view describes purchase session """

    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get(self, request, user_id, purchase_id):
        """ This method retrieves a Purchase object """

        purchase = get_object_or_404(Purchase, pk=purchase_id, user_id=user_id)
        serializer = PurchaseSerializer(purchase)
        return Response(serializer.data)


class PurchaseListAPIView(ListAPIView):

    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()
    paginate_by = 9
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]


""" TODAY SESSION API VIEW"""


class TodaySessionsListView(generics.ListAPIView):
    serializer_class = SessionSerializer

    def get_queryset(self):
        start_time_api = self.request.query_params.get('start_time')
        end_time_api = self.request.query_params.get('end_time')
        hall_id = self.request.query_params.get('hall')
        queryset = Session.objects.filter(start_date__lte=timezone.now().date(), end_date__gte=timezone.now().date())

        if hall_id:
            queryset = queryset.filter(hall_id=hall_id)

        if start_time_api and end_time_api:
            queryset = queryset.filter(start_time__gte=start_time_api, start_time__lte=end_time_api)
        elif start_time_api:
            queryset = queryset.filter(start_time__gte=start_time_api)
        elif end_time_api:
            queryset = queryset.filter(start_time__lte=end_time_api)
        else:
            queryset.filter(start_time__gte=time.min, start_time__lte=time.max)

        if not queryset.exists():
            raise Http404("No sessions available for the specified criteria.")

        return queryset



