from django.shortcuts import render
from  rest_framework import generics,status,views
from authentication import serializers as api_serializer
from authentication import models as api_models
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from .utils import Util
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .renderers import UserRenderer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,force_bytes,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util

# Create your views here.


class RegisterView(generics.CreateAPIView):
       permission_classes = [AllowAny]
       serializer_class = api_serializer.RegisterSerializer
       queryset =  api_models.User.objects.all()
       renderer_classes = (UserRenderer,)
       
       def post(self, request, *args, **kwargs):
              serializer = self.serializer_class(data=request.data)
              serializer.is_valid(raise_exception=True)
              user = serializer.save()
              token = RefreshToken.for_user(user).access_token
              current_site = get_current_site(request).domain
              relativeLink = reverse('email-verify')
              absurl = 'http://'+ current_site + relativeLink + "?token=" + str(token)
              email_body = 'Hi' + " " +  user.username + " " +'Use Link below to verify your email \n' + absurl
              data = {'email_body':email_body,'email_subject':'Verify your email','to_email':user.email}
              Util.send_email(data)
              
              return Response(serializer.data,status=status.HTTP_201_CREATED)
              
class VerifyEmail(views.APIView):
    
    serializer_class = api_serializer.EmailVerificationSerializer  
    token_param_config = openapi.Parameter('token',in_=openapi.IN_QUERY,description='Description',type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config])
    
    def get(self,request):
        token = request.GET.get('token')
        try:
           payload =  AccessToken(token)
           user = api_models.User.objects.get(id=payload['user_id'])
           if not user.is_verified:
             user.is_verified = True
             user.save()
           return Response({"message":"Account successfully verified"},status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError :
            return Response({'error':"Activation Expired"},status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
              return Response({'error':"Invalid token"},status=status.HTTP_400_BAD_REQUEST)
        
        
class LoginAPIView(generics.GenericAPIView):
      serializer_class = api_serializer.LoginSerializer
    
      def post(self,request):
          serializer = self.serializer_class(data=request.data)
          serializer.is_valid(raise_exception=True)
          
          return Response(serializer.data,status=status.HTTP_200_OK)
            
            
            
class RequestPasswordResetEmail(generics.GenericAPIView):
       serializer_class = api_serializer.ResetPasswordEmailRequestSerializer
       
       def post(self,request):
             serializer = self.serializer_class(data=request.data)
             email = request.data['email']         
             if api_models.User.objects.filter(email=email).exists():
                    user = api_models.User.objects.get(email=email)
                    uidb64 = urlsafe_base64_encode(force_bytes(user.id))
                    token = PasswordResetTokenGenerator().make_token(user)
                    current_site = get_current_site(request=request).domain
                    relativeLink = reverse('password-reset-confirm',kwargs={'uidb64':uidb64,'token':token})
                    absurl = 'http://' + current_site +  relativeLink
                    email_body = 'Hello, \n Use link below to reset your password \n ' + absurl
                    data = {
                        'email_body':email_body,'to_email':user.email,
                        'email_subject': 'Reset your Password'
                    }
                    Util.send_email(data)           
             return Response({'success':'We have sent you a link to reset your password'},status=status.HTTP_200_OK)

class PasswordTokenCheckApi(generics.GenericAPIView):
    
       serializer_class = api_serializer.SetNewPasswordSerializer
       
       def get(self,request,uidb64,token):
           try:
             id = smart_str(urlsafe_base64_decode(uidb64))
             user = api_models.User.objects.get(id=id)
             
             if not PasswordResetTokenGenerator().check_token(user,token):
                 return Response({"error":"Token is not valid,please request a new one"})
             
             return Response({'success':True,'message':'Credentials Valid',
                              'uidb6':uidb64,'token':token})
           except DjangoUnicodeDecodeError as e:
               return Response({"error":"Token is not valid,please request a new one"})
               

class SetNewPasswordAPIView(generics.GenericAPIView):
     serializer_class = api_serializer.SetNewPasswordSerializer
     
     def patch(self,request):
         serializer = self.serializer_class(data=request.data)
         serializer.is_valid(raise_exception=True)
         
         return Response({"message":"Password reset Successfully"})
    