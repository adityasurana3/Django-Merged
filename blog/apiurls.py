from os import name
from rest_framework import routers
from .api import *
from rest_framework.routers import DefaultRouter

router = routers.DefaultRouter()
router.register('postapi',PostViewSet,basename='postapi')
router.register('categoryapi',CategoryViewSet,basename='categoryapi')
router.register('tagapi',TagViewSet,basename='tagapi')
router.register('userapi', UserViewSet, basename='userapi')
router.register('user_signupapi', RegisterViewSet, basename='user_signupapi')
router.register('loginapi', LoginViewSet, basename='loginapi') 
router.register('update_profileapi', UpdateProfileViewSet, basename='update_profileapi')  


urlpatterns = [
    # router.register('postapi/',api.PostViewSet),
    # # router.register('categoryapi/',api.)
]

