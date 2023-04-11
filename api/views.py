""" Views for the api app  """
import datetime

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

from django.utils import timezone
from django.contrib.auth import get_user_model, authenticate
from django.db.models import Q, Sum
from django.http import Http404

from kinohall.models import Movie, Hall, Session
from kinohall.serializers import MovieSerializer, HallSerializer, SessionSerializer

from order.models import Purchase
from order.serializers import PurchaseSerializer

from user.models import UserModel
from user.serializers import UserModelSerializer

from api.permissions import IsOwnerOrAdmin, SessionPermission

User = get_user_model()


class UsersViewSet(ModelViewSet):
    """A ViewSet that allows viewing, creating, updating, and deleting `UserModel` objects."""

    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [IsAdminUser]


class RegisterView(APIView):
    """API View that allows registration of new users.

    Accepts a POST request with user data and attempts to create a new user
    in the database using the 'UserModelSerializer' serializer. If the data
    is valid, the user is saved and a response with the user's username and email
    is returned. If the data is invalid, a response with the serializer's
    errors is returned.

    This view does not require authentication or permission to access."""

    def post(self, request):
        """Handle POST requests for user registration.

        :param request: HTTP request object containing user registration data.
        :return: HTTP response object with the user's username and email if
        registration is successful, or the serializer's errors and a 'Bad Request'
        status code if registration fails. """

        serializer = UserModelSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'username': user.username, 'email': user.email})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    authentication_classes = []  # remove TokenAuthentication
    permission_classes = []  # remove IsAuthenticated


class LoginView(APIView):
    """API view for user login. Accepts a POST request with username
    and password in the request data. If the credentials are valid,
    generates and returns a token for the user. If the credentials are
    invalid, returns an error message with a status of 400.

    This view does not require authentication or permission to access."""

    def post(self, request):
        """Authenticates a user and generates a token if the credentials are valid.

            :param request: The HTTP request object.
            :return: HTTP response object with the token and user info if credentials are valid.
                 Otherwise, returns an error message with a status of 400."""

        user = authenticate(username=request.data.get('username'),
                            password=request.data.get('password'))
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'username': user.username, 'email': user.email})
        return Response({'error': 'Invalid credentials'}, status=400)

    authentication_classes = []  # remove TokenAuthentication
    permission_classes = []  # remove IsAuthenticated


class LogoutView(APIView):
    """API view that logs out a user by deleting their authentication
        token from the database.

        Accepts a POST request with a valid authentication token in the
        header, which is used to identify the user to log out. If the token
        is valid and corresponds to an existing user, the token is deleted
        from the database, effectively logging out the user. If the token
        is invalid or does not correspond to an existing user, a response
        with an error message is returned.

        This view requires authentication using TokenAuthentication and
        optionally, permission to access the endpoint using IsAuthenticated.
        If permission_classes is commented out, the endpoint is
        accessible to all users, authenticated or not."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """POST request to logout the authenticated user.

               :param request: HTTP request object.
               :return: HTTP response object indicating if the user was
                successfully logged out."""

        token = request.auth
        token.delete()
        return Response({'message': 'Successfully logged out'})


class MovieViewSet(ModelViewSet):
    """API endpoint that allows movies to be viewed or edited."""

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    permission_classes = [IsAdminUser]


class HallViewSet(ModelViewSet):
    """API endpoint that allows halls to be viewed or edited."""

    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        """Create a new hall instance."""

        name = request.data.get('name')
        if not name:
            return Response({'detail': 'Name is required.'},
                            status=status.HTTP_400_BAD_REQUEST)
        if Hall.objects.filter(name=name).exists():
            return Response({'detail': 'This name already exists.'},
                            status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Update a hall instance."""

        instance = self.get_object()
        hall_id = instance.pk

        purchases_with_hall = Purchase.objects.filter(session__hall__id=hall_id, paid=True)
        if purchases_with_hall.exists():
            return Response({'error': 'You cannot update this hall because some '
                                      'tickets have already been sold.'},
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
        return Response({'error': 'You cannot delete this hall because '
                                  'some tickets have been sold'}, status=status.HTTP_400_BAD_REQUEST)


class SessionViewSet(viewsets.ModelViewSet):
    """API endpoint that allows sessions to be viewed or edited."""

    serializer_class = SessionSerializer
    queryset = Session.objects.all()
    permission_classes = [SessionPermission]

    def create(self, request, *args, **kwargs):
        """Called when creating a new session"""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.validate_session(serializer.validated_data)
        serializer.save()

    def update(self, request, *args, **kwargs):
        """Called when updating an existing session"""

        session_id = kwargs['pk']
        purchases_with_session = Purchase.objects.filter(session_id=session_id, paid=True)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.validate_session(serializer.validated_data, session_id=session_id)

        if not request.user.is_staff or purchases_with_session.exists():
            return Response({'error': 'You cannot update this session because some tickets '
                                      'have been sold'},
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

        if start_date < datetime.date.today():
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

        instance = self.get_object()
        session_id = instance.pk
        purchases_with_session = Purchase.objects.filter(session_id=session_id, paid=True)

        if self.request.user.is_staff and not purchases_with_session.exists():
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'You cannot delete this session '
                                  'because some tickets have been sold'}, status=status.HTTP_400_BAD_REQUEST)


class SessionTodayListAPIView(ListAPIView):
    """API endpoint that returns a list of sessions happening today.

        Only authenticated users can access this endpoint.
        The endpoint returns a paginated list of sessions happening today, sorted by start time.
        Each session is represented as a SessionSerializer object."""

    serializer_class = SessionSerializer
    queryset = Session.objects.filter(start_date__lte=timezone.now().date(),
                                      end_date__gte=timezone.now().date())
    paginate_by = 9
    permission_classes = [IsAuthenticatedOrReadOnly]


class SessionTomorrowListAPIView(ListAPIView):
    """API View that retrieves a paginated list of all sessions that are scheduled for tomorrow."""

    serializer_class = SessionSerializer
    queryset = Session.objects.filter(start_date__lte=timezone.now().date() +
                                                      timezone.timedelta(days=1),
                                      end_date__gte=timezone.now().date() +
                                                    timezone.timedelta(days=1))
    paginate_by = 9
    permission_classes = [IsAuthenticatedOrReadOnly]


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def purchase_session_api(request, pk):
    """API endpoint for purchasing tickets for a movie session.

        :param request: The HTTP request object.
        :type request: rest_framework.request.Request

        :param pk: The primary key of the movie session to purchase tickets for.
        :type pk: int

        :return: The HTTP response object indicating whether the purchase was successful or not.
        :rtype: rest_framework.response.Response"""

    session = get_object_or_404(Session, pk=pk)
    hall_capacity = session.hall.seats
    remaining_capacity = 0

    quantity = int(request.data.get('quantity'))
    showdata = timezone.datetime.strptime(request.data.get('showdata'), '%Y-%m-%d').date()
    tickets_sold = Purchase.objects.filter(showdata=showdata,
                                           session=session).aggregate(Sum('quantity'))[
                                           'quantity__sum'] or 0
    remaining_capacity = hall_capacity - tickets_sold
    current_time = timezone.localtime(timezone.now()).time()

    if showdata < timezone.now().date():
        return Response({'error': 'Show date cannot be less than today'},
                        status=status.HTTP_400_BAD_REQUEST)

    if showdata == timezone.now().date() and current_time > session.start_time:
        return Response({'error': 'The session has already started. '
                                  'Please choose another session or day'},
                        status=status.HTTP_400_BAD_REQUEST)

    if showdata > session.end_date:
        return Response({'error': 'You can only select the dates within which films are shown'},
                        status=status.HTTP_400_BAD_REQUEST)

    if remaining_capacity < quantity:
        return Response({'error': f"Only {remaining_capacity} tickets available for purchase"},
                        status=status.HTTP_400_BAD_REQUEST)

    if request.user.wallet < session.price * quantity:
        return Response({'error': "You don't have enough money in your account to buy. "
                                  "Please, check your balance"},
                        status=status.HTTP_400_BAD_REQUEST)

    if quantity <= remaining_capacity:
        purchase = Purchase.objects.create(user=request.user, session=session,
                                           quantity=quantity, showdata=showdata)
        request.user.wallet -= session.price * quantity
        request.user.save()
        return Response({'success': True, 'url': purchase.get_absolute_url()},
                        status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_400_BAD_REQUEST)


class PurchaseSessionAPIView(APIView):
    """API endpoint for retrieving a single Purchase object.

        Only authenticated users who own the purchase or are admins
        can access this view."""

    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get(self, request, user_id, purchase_id):
        """Retrieve a Purchase object.

            :param request: HTTP request object.
            :param user_id: ID of the user who made the purchase.
            :param purchase_id: ID of the purchase object to retrieve.
            :raises: Http404: If the Purchase object with given `purchase_id`
             and `user_id` does not exist.
            :return: HTTP response object containing serialized Purchase data.
            :rtype: Response"""

        purchase = get_object_or_404(Purchase, pk=purchase_id, user_id=user_id)
        serializer = PurchaseSerializer(purchase)
        return Response(serializer.data)


class PurchaseListAPIView(ListAPIView):
    """API endpoint for retrieving a list of all Purchase objects.
        Only authenticated users who own the purchases or are admins
        can access this view."""

    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()
    paginate_by = 9
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]


class TodaySessionsListView(generics.ListAPIView):
    """API endpoint that returns a list of sessions that are available for the current day,
    filtered by hall and start/end time if provided.

    Only authenticated users can access this view."""
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Returns the queryset for the view, filtered by hall and start/end time if provided.
            Raises a 404 exception if no sessions are found for the specified criteria."""

        start_time_api = self.request.query_params.get('start_time')
        end_time_api = self.request.query_params.get('end_time')
        hall_id = self.request.query_params.get('hall')
        queryset = Session.objects.filter(start_date__lte=timezone.now().date(),
                                          end_date__gte=timezone.now().date())

        if hall_id:
            queryset = queryset.filter(hall_id=hall_id)

        if start_time_api and end_time_api:
            queryset = queryset.filter(start_time__gte=start_time_api, start_time__lte=end_time_api)
        elif start_time_api:
            queryset = queryset.filter(start_time__gte=start_time_api)
        elif end_time_api:
            queryset = queryset.filter(start_time__lte=end_time_api)
        else:
            queryset.filter(start_time__gte=datetime.time.min, start_time__lte=datetime.time.max)

        if not queryset.exists():
            raise Http404("No sessions available for the specified criteria.")

        return queryset
