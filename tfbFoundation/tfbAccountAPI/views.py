#necessary module,file,code import
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializers, ProfileSerializers
from libs.email_verification import send_verification_code
from django.contrib.auth.models import User
from libs.time_calculate import time_calculate
from libs.email_verification import send_verification_code
from django.utils import timezone
from django.contrib.auth import authenticate,login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

#----------user creation view use APIView for more controlling start----------
class AccountCreateView(APIView):
    user_serializer_class = UserSerializers
    profile_serializer_class = ProfileSerializers
    
    def post(self, request, *args, **kwargs):
        #user creation handling
        user_data = {}
        user_data['username'] = request.data.get('username')
        user_data['first_name'] = request.data.get('first_name')
        user_data['last_name'] = request.data.get('last_name')
        user_data['email'] = request.data.get('email')
        user_data['password'] = request.data.get('password')
        user_data['confirm_password'] = request.data.get('confirm_password')
        user_serializer = self.user_serializer_class(data=user_data)

        #profile creation handling
        profile_data = {}
        profile_data['user'] = 'test'
        profile_data['profession'] = request.data.get('profession')
        profile_data['phone_no'] = request.data.get('phone_no')
        profile_data['address'] = request.data.get('address')
        profile_data['current_address'] = request.data.get('current_address')
        profile_data['district'] = request.data.get('district')
        profile_data['sub_district'] = request.data.get('sub_district')
        profile_data['account_type'] = request.data.get('account_type')
       
        #check validation and save
        if user_serializer.is_valid():
            print("user valid")
            try:
                user = user_serializer.save(commit=True)
                profile_data['user'] = user.id
                profile_serializer = self.profile_serializer_class(data=profile_data)
                if profile_serializer.is_valid():
                    print("profile valid")
                    try:
                        profile_serializer.save()
                        send_verification_code(user)
                        return Response({'success': 'Account created successfully.Please verify your email for confirmation.'}, status=status.HTTP_201_CREATED)
                    except Exception as e:
                        print(e)
                        user.delete()
                        return Response({"error":"Profile Data saving error occured on database"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    user.delete()
                    return Response(profile_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except:
                return Response({"error":"User Data saving error occured on database"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
           return Response(user_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#----------user creation view use APIView for more controlling end----------

#----------user account verify start ----------
class AccountVerifyView(APIView):
    
    def put(self,request):
        email = request.data.get('email')
        verification_code = request.data.get('verification_code')
        try:
            user = User.objects.get(email=email, profile__verification_code=verification_code)
            time_left = time_calculate(user.profile.created_at)
            if time_left > 10000:
                return Response({'error':'OOPs!Your Verification code timeout.please resend'}, status=status.HTTP_504_GATEWAY_TIMEOUT)
            else:
                user.is_active = True
                user.save()
                return Response({'success':'Account verified successfully.'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': 'Your Verification code does not match'}, status=status.HTTP_404_NOT_FOUND)
           


#----------user account verify end ----------


#---------- user verification code resend start ----------
class ResendVerificationCodeView(APIView):
    def put(self,request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            verification_code = send_verification_code(user)
            user.profile.verification_code = verification_code
            user.profile.created_at = timezone.now()
            user.profile.save()
            return Response({'success':'Verification code successfully send to your email.please check your email.'},status=status.HTTP_202_ACCEPTED)
        except:
            return Response({'error':'User not found'}, status=status.HTTP_404_NOT_FOUND)


#---------- user verification code resend end ----------



#---------- user login view start ----------
class AccountLoginView(APIView):
    def post(self,request):
        user_email = request.data.get('user_email')
        password = request.data.get('password')
        try:
            user = authenticate(username=user_email,password=password)
            if not user:
                user2 = User.objects.filter(email=user_email).first()
                user = authenticate(username=user2.username, password=password)
            if user:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)
            else:
                return Response({'error':'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'error':'Invalid credential'}, status=status.HTTP_401_UNAUTHORIZED)
#---------- user login view end ----------



#---------- user logout view start ----------
class AccountLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            # logout(request) its used for session based authentication
            request.user.auth_token.delete() #it's used for token based authentication
            return Response({'success':'User logged out successfully'}, status=status.HTTP_200_OK)
        except:
            return Response({'error':'User not found'}, status=status.HTTP_404_NOT_FOUND)
#---------- user logout view end ----------



#---------- user account get view start ----------
class AccountGetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        print("hhelo", self.request.user)
        try:
            user = User.objects.get(id=id)
            if request.user != user:
                return Response({'detail': 'Not authorized to access this user information.'}, status=status.HTTP_403_FORBIDDEN)

            # Serialize the user data
            serializer = UserSerializers(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print("get error: ", e)
            return Response({'Error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
#---------- user account get view end ----------


class NewsSaved(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        user = request.user.profile
        new_favorite_id = request.data.get('news_id')  # ID to be added to favorites

        if not new_favorite_id:
            return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Assume `favorites` is a JSONField on the user model
            # Initialize the JSON field as an empty list if it's None
            if user.favourites is None:
                user.favourites = []

            # Ensure `favourites` is a list
            if not isinstance(user.favourites, list):
                return Response({"error": "favourites must be a list"}, status=status.HTTP_400_BAD_REQUEST)

            # Add the new ID if it's not already in the list
            if new_favorite_id not in user.favourites:
                user.favourites.append(new_favorite_id)
                user.save()

            return Response({"message": "Favorite added successfully", "favourites": user.favourites}, status=status.HTTP_200_OK)

        except Exception as e:
            print("hello")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
