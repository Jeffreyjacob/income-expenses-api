from rest_framework import serializers
from authentication import models as api_models
from django.contrib.auth.password_validation import validate_password
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,force_bytes,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode 

class RegisterSerializer(serializers.ModelSerializer):
       password = serializers.CharField(min_length=7,write_only=True,validators=[validate_password])
       
       class Meta:
           model = api_models.User
           fields = [
               'email',
               'username',
               'password'
           ]
           
       def validate(self, attrs):
              email = attrs.get('email','')
              username = attrs.get('username','')
              
              if not username.isalnum():
                  raise serializers.ValidationError("The username should only contain alphanumeric characters")
              return attrs
          
       def create(self, validated_data):
             user = api_models.User.objects.create(
                 email = validated_data['email'],
                 username = validated_data['username']
             )
             user.set_password(validated_data['password'])
             user.save()
             return user


class EmailVerificationSerializer(serializers.ModelSerializer):
        token = serializers.CharField()
        
        class Meta:
            model = api_models.User
            fields = [
                'token'
            ]
            
class LoginSerializer(serializers.ModelSerializer):
       email = serializers.EmailField()
       password = serializers.CharField(min_length=6,write_only=True)
       username = serializers.CharField(read_only=True)
       tokens = serializers.CharField(read_only=True)
       
       class Meta:
           model = api_models.User
           fields = [
               'email',
               'password',
               'username',
               'tokens',
           ]
         
       def validate(self, attrs):
             email = attrs.get('email','')
             password = attrs.get('password','')
             
             user = auth.authenticate(email=email,password=password)
             if not user:
                 raise AuthenticationFailed('Invalid credentials, try again')
             if not user.is_active:
                 raise AuthenticationFailed('Account disabled, contact admin')
             if not user.is_verified:
                 raise AuthenticationFailed('Email is not verified')         
             return {
                 'email': user.email,
                 'username': user.username,
                 'tokens' : user.tokens()
             }
             
             return super().validate(attrs)
        
class ResetPasswordEmailRequestSerializer(serializers.Serializer):
       email = serializers.EmailField(min_length=2)
       
       class Meta:
           fields = ['email']
           
class SetNewPasswordSerializer(serializers.Serializer):
       password = serializers.CharField(min_length=6,write_only=True)
       token = serializers.CharField(write_only=True)
       uidb64 = serializers.CharField(write_only=True)
       
       class Meta:
           fields = [
               'password',
               'token',
               'uidb64'
           ]
       
       def validate(self, attrs):
            try:
                password = attrs.get('password')
                token = attrs.get('token')
                uidb64 = attrs.get('uidb64')
                
                id = force_str(urlsafe_base64_decode(uidb64))
                user = api_models.User.objects.get(id=id)
                
                if not PasswordResetTokenGenerator().check_token(user,token):
                    raise AuthenticationFailed('The reset link is invalid',401)
                
                user.set_password(password)
                user.save()
            except Exception as e :
                   raise AuthenticationFailed('The reset link is invalid',401)
               
            return super().validate(attrs)
               
                
       