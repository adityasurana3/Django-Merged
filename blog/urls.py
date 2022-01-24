from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<int:id>/',views.category_detail, name='category_detail'),
    path('tag/<slug:slug>/',views.tag_detail, name='tag_detail'),
    path('new_post', views.post_new, name='post_new'),
    path('profile-detail/',views.profile_edit,name='profile_detail'),
    path('profile/',views.user_profile,name='user_profile'),
    path('category/',views.category_list, name='category_list'),
    path('tag/',views.tag_list, name='tag_list'),
    path('add/', views.add_category, name='add_category'),
    # path('csv/', views.export_csv, name='exportcsv'),
    path('',views.post_list,name='post_list'),
]
