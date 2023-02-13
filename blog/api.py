from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import permissions
from blog.serializers import CategorySerializer, LoginSerializer, PostSerializer, TagSerializer, UserSerializer, UpdateUserSerializer, RegisterSerializer
from blog.models import Category, Post, Tag, MyUser
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated, AllowAny

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    serializer_class = PostSerializer
    # permission_class = [permissions.IsAuthenticated]
    http_method_names = ['post','get','put','patch']
    

    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_class = [permissions.IsAuthenticated]
    http_method_names = ['get',]
    
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # permission_class = [permissions.IsAuthenticated]
    http_method_names = ['get',]
    
class UserViewSet(viewsets.ModelViewSet):
    
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    
class LoginViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = MyUser.objects.all()
    serializer_class = LoginSerializer
    http_method_names = ['post']

class UpdateProfileViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    # queryset = Token.objects.get(key="token").user          

    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer
    http_method_names = ['get', 'put','patch']

class RegisterViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    http_method_names = ['post']