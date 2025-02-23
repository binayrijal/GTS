from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin

# Custom User Manager 
class UserManager(BaseUserManager):
    def create_user(self, email, name,address,citizenship_no, password=None, password2=None):
        """
        Creates and saves a User with the given email, name, tc and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            address=address,
            citizenship_no=citizenship_no,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None,citizenship_no,address):
        """
        Creates and saves a superuser with the given email,name and password.
        """
        user = self.create_user(
        email=email,
        password=password,
        name=name,
        citizenship_no=citizenship_no,
        address=address

        )
        user.is_admin = True
        user.save(using=self._db)
        return user


#Create Custom User
class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    
    
    # citizenship_no = models.CharField(
    #     max_length=20,
    #     validators=[MaxLengthValidator(limit_value=20)]
    # )
    
    citizenship_no = models.CharField(max_length=10, default="")

    address = models.CharField(max_length=200,default="")
    # tc=models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "address","citizenship_no"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



class Event(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
  
   

    def __str__(self):
        return self.title
