from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from django.conf import settings

class UserCreator(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("поле email обязательно для создания пользователя")

        email = self.normalize_email(email)                 
        user = self.model(email=email, **extra_fields)      
        user.set_password(password)                          
        user.save(using=self._db)                           
        return user                                         
    
    def create_superuser(self, email, password=None, **extra_fields):   
        extra_fields.setdefault("is_staff", True)           
        extra_fields.setdefault("is_superuser", True)                
        return self.create_user(email, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)      

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []               

    objects = UserCreator()  

    def __str__(self):
        return self.email
    
class AuthToken(models.Model):                          
    key = models.CharField(max_length=40, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                             related_name='tokens', 
                             on_delete=models.CASCADE)                        
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = uuid.uuid4().hex
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.email} - {self.key}"

