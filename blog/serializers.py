from pyexpat import model
from rest_framework import serializers
from blog.models import Post, Category,Comments,MyUser, Tag
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    token_details = serializers.SerializerMethodField('get_token_details')

    class Meta:
        model = MyUser
        fields = ('username','first_name', 'last_name', 'email_id', 'phone_no',
                  'image', 'city', 'state', 'country')

    def get_token_details(self, obj):
        token = Token.objects.get_or_create(user = obj)[0]
        
        return str(token)
    
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('username', 'password')
        extra_kwargs = {
            'username': {'required': True, 'validators':[]},
            'password': {'required': True}
        }
    def to_representation(self, instance):
        user = UserSerializer(instance = instance)
        return user.data
    
class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = MyUser
        fields = ('username', 'first_name', 'last_name', 'email_id')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if MyUser.objects.exclude(pk=user.pk).filter(email_id=value).exists():
            raise serializers.ValidationError({"email_id": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if MyUser.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email_id = validated_data['email_id']
        instance.username = validated_data['username']
        instance.save()
        return instance

class RegisterSerializer(serializers.ModelSerializer):
    email_id = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=MyUser.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = MyUser
        fields = ('username', 'first_name', 'last_name', 'email_id', 'phone_no',
                  'image', 'city', 'state', 'country', 'about', 'company', 'designation',)
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password1": "Password fields didn't match."})

        return attrs

    def to_representation(self, instance):
        user = UserSerializer(instance = instance)
        return user.data

    def create(self, validated_data):
        user = MyUser.objects.create(
            username=validated_data['username'],
            email_id=validated_data['email_id'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user

    def get_token_details(self, obj):
        token = Token.objects.get_or_create(user = obj)
        return token.key