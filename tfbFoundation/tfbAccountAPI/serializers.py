#necessary module,file,code import
from django.contrib.auth.models import User
from .models import Profile, NewsSaved
from rest_framework import serializers
import re

#----------profile serializers start----------
class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
    
    #validation check profile data
    def validation(self,data):
        profession = data['profession']
        address = data['address']
        current_address = data['current_address']
        phone_no = data['phone_no']
        district = data['district']
        sub_district = data['sub_district']
        account_type = data['account_type']

        #profession validation check
        if not profession:
            raise serializers.ValidationError({'profession':'Please enter your profession.'})
        elif len(profession) < 4:
            raise serializers.ValidationError({'profession':'Your profession name is very short.Please rewrite clearly.'})
        elif len(profession) > 200:
            raise serializers.ValidationError({'profession':'Your profession name is too long.Please rewrite clearly.'})
        
        #address validation check
        if not address:
            raise serializers.ValidationError({'address':'Please enter your address.'})
        elif len(address) < 4:
            raise serializers.ValidationError({'address':'Your address is very short.'})
        elif len(address) > 200:
            raise serializers.ValidationError({'address':'Your address is too long.'})
        
        #current_address validation check
        if not current_address:
            raise serializers.ValidationError({'current_address':'Please enter your current address.'})
        elif len(current_address) < 4:
            raise serializers.ValidationError({'current_address':'Your current address is very short.'})
        elif len(current_address) > 200:
            raise serializers.ValidationError({'current_address':'Your current address is too long.'})
        
        #phone_no validation check
        if not phone_no:
            raise serializers.ValidationError({'phone_no':'Please enter your phone number.'})
        elif len(phone_no) != 11:
            raise serializers.ValidationError({'phone_no':'Your phone number is not valid.'})
        
        #district validation check
        if not district:
            raise serializers.ValidationError({'district':'Please enter your district.'})
        elif len(district) < 4:
            raise serializers.ValidationError({'district':'Your district name is very short.'})
        elif len(district) > 200:
            raise serializers.ValidationError({'district':'Your district name is too long.'})
        
        #sub_district validation check
        if not sub_district:
            raise serializers.ValidationError({'sub_district':'Please enter your sub district.'})
        elif len(sub_district) < 4:
            raise serializers.ValidationError({'sub_district':'Your sub district name is very short.'})
        elif len(sub_district) > 200:
            raise serializers.ValidationError({'sub_district':'Your sub district name is too long.'})
        
        #account_type validation check
        if not account_type:
            raise serializers.ValidationError({'account_type':'Please enter your account type.'})
        elif len(account_type) < 4:
            raise serializers.ValidationError({'account_type':'Your account type name is very short.'})
        elif len(account_type) > 200:
            raise serializers.ValidationError({'account_type':'Your account type name is too long.'})
        
        #returning the validated data
        return data
    
        
#----------profile seralizers end----------

#---------user serializers start----------
class UserSerializers(serializers.ModelSerializer):
    profile = ProfileSerializers(read_only=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'profile']

    #validation check user data
    def validate(self, data):
        username = data['username']
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        password = data['password']
        confirm_password = data['confirm_password']
        
        #password validation check
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d!@#$%^&*()_+={}\[\]:;"\'<>,.?/~`-]{6,}$'
        if password != confirm_password:
            raise serializers.ValidationError({'confirm_password':'password and confirm password does not match.'})
        elif not password.strip():
            raise serializers.ValidationError({'password':'Please enter your password.'})
        elif not confirm_password.strip():
            raise serializers.ValidationError({'confirm_password':'Please enter your confrim password.'})
        elif not re.match(pattern, password):
            raise serializers.ValidationError({'password':'Password must be at least 6 characters with lower,Upper,number mixed.'})
        
        #username validation check
        if User.objects.filter(username = username).exists():
            raise serializers.ValidationError({'username':'Username already exists.'})
        elif not username:
            raise serializers.ValidationError({'username':'Please enter your user name.'})
        elif len(username) < 4:
            raise serializers.ValidationError({'username':'Your user name is very short.'})
        
        #first_name validation check
        if not first_name:
            raise serializers.ValidationError({'first_name':'Please enter your first name.'})
        elif len(first_name) < 4:
            raise serializers.ValidationError({'first_name':'Your first_name is very short.'})
        
        #last_name validation check
        if not last_name:
            raise serializers.ValidationError({'last_name':'Please enter your last name.'})
        elif len(last_name) < 4:
            raise serializers.ValidationError({'last_name':'Your last name is very short.'})
        
        #email validation check
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email':'Email already exists.'})
        elif not email:
            raise serializers.ValidationError({'email':'Please enter your email.'})
        elif not re.match(email_regex, email):
            raise serializers.ValidationError({'email':'Invalid email address.'})
        
        #returning validation data
        return data
    
    #save the database
    def save(self, commit=False):
        username = self.validated_data['username']
        email = self.validated_data['email']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        password = self.validated_data['password']
        
        user = User(username = username, first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.is_active = False

        if commit:
            user.save()
        return user
#----------user serializers end----------



#---------- USER NEWS SAVED START ----------
class UserNewsSavedSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsSaved
        fields = '__all__'
#---------- USER NEWS SAVED END ----------