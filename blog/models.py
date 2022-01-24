# Create your models here.

from django.conf import settings
from django.db import models
from django.db.models.deletion import PROTECT
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django_extensions.db.fields import AutoSlugField

# pip install django-extensions
class MyUser(AbstractUser):
    email_id = models.EmailField()
    phone_no = models.IntegerField() #PositiveIntergerField
    image = models.ImageField(null=True, blank=True, upload_to='users/')
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    about = models.TextField()
    company = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', max_length=200,editable=False)
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    slug = AutoSlugField(populate_from='name', max_length=200,editable=False)
    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=PROTECT)
    tag = models.ManyToManyField(Tag)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    slug = AutoSlugField(populate_from='title', max_length=200,editable=False)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    featured_image = models.ImageField(upload_to='image/')
    thumbnail_image = models.ImageField(upload_to='image/')
    # slug = models.SlugField(max_length=100, null=True)


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comments(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,related_name='replies')
    def __str__(self):
        return self.name
