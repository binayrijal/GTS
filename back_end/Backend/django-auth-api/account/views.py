from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegisterationSerializer, UserLoginSerializer, UserProfileSerializer, UserChangePasswordSerializer, UserSendPasswordResetEmailSerializer, UserPasswordResetSerializer,UserMessageSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
<<<<<<< HEAD
from rest_framework import serializers
from account.utils import Util

=======
from rest_framework.permissions import AllowAny
>>>>>>> 100e2a8bb02581432211bf3d7c052188edbe8318



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view

# for events,date from calendar
from rest_framework import viewsets
from .models import Event
from .serializers import EventSerializer
from .permissions import IsAdminOrReadOnly

# Generate Token Manually

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegisterationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegisterationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token=get_tokens_for_user(user)
        return Response({'token':token,'message': 'Registeration Success'},
                            status=status.HTTP_201_CREATED
                            )
        # return Response(serializer.errors,
        #                 status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        
        if user is not None:
            token=get_tokens_for_user(user)
            response = JsonResponse({'message': 'Login Success', 'refresh_token':token['refresh'], 'access_token': token['access']})
            response.set_cookie('access_token', token['access'], httponly=True)
            response.set_cookie('refresh_token', token['refresh'], httponly=True)
            
            return response
        else:
            return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}},
                            status=status.HTTP_400_BAD_REQUEST
                            )

        # return Response(serializer.errors,
        #                 status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    renderer_classes= [UserRenderer]
    # permission_classes = [permissions.IsAuthenticated]
    def get(self,request,format=None):
        serializer =UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
class UserChangePasswordView(APIView):
    renderer_classes= [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request,format=None):
        serializer=UserChangePasswordSerializer(data=request.data,context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'Password Changed Successfully'},
                                status=status.HTTP_200_OK)
        # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)    
    
class SendPasswordResetEmailView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserSendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'Password Reset Link Sent Successfully, Please Check Your Email'},
                                status=status.HTTP_200_OK)
        # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)   
     
class UserPasswordResetView(APIView):
    renderer_classes=[UserRenderer] 
    def post(self, request, uid, token, format=None):
        serializers=UserPasswordResetSerializer(data=request.data,
                                                context={'uid':uid,'token':token})   
        serializers.is_valid(raise_exception=True)
        return Response({'message':'Password Reset Successfully'},
                            status=status.HTTP_200_OK)
        # return Response(serializers.errors,
        #                     status=status.HTTP_400_BAD_REQUEST)  
        
class UserLogoutView(APIView):
    def post(self, request, format=None):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token is not None:
            # Delete the refresh token from the database or cache
            # Alternatively, you can mark the token as expired in the database or cache
            # Here, we assume you have a User model with a refresh_token field
            user = request.user
            user.refresh_token = None
            user.save()

            # Clear the access and refresh token cookies
            response = Response({'message': 'Logout Successful'})
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response
        else:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)


# Apply the CSRF exemption to the logout view
@method_decorator(csrf_exempt, name='dispatch')
class UserLogoutViewCSRFExempt(UserLogoutView):
    pass



<<<<<<< HEAD
@api_view(['POST'])
def send_message(request):
    email = request.data.get('email')
    address = request.data.get('address')

    if not email and not address:
        return Response({'error': 'email and address are required'})

    user_data = {'email': email, 'address': address}
    user_serializer = UserMessageSerializer(data=user_data)
    body="we send this mail.The vehicle is near to you"
    data={
        'email_subject':'Mail from Garbage Tracking system',
                'body':body,
               'to_email':email
            }
    
    if user_serializer.is_valid():
        user_serializer.save()
        Util.send_mail(data)
        return Response({'message': 'User data saved successfully'})
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

=======


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminOrReadOnly]
>>>>>>> 100e2a8bb02581432211bf3d7c052188edbe8318
