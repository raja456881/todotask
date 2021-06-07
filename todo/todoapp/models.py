from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser

class usermanager(BaseUserManager):
	def create_user(self, username, email,  is_admin, password, **extra_fields ):
		if username is None:
			raise TypeError("users should have a username")
		if email is None:
			raise  TypeError("users  should have a email")
		user=self.model(username=username, email=self.normalize_email(email), **extra_fields)
		if is_admin:
			user.is_admin=True
			user.is_superuser=True
		user.is_staff = True
		user.set_password(password)
		user.is_active=True
		user.save()
		return user

	def create_superuser(self, username, email,  password, **extra_field):

		extra_field.setdefault('is_staff', True)
		extra_field.setdefault('is_superuser', True)
		extra_field.setdefault('is_active', True)
		if username is None:
			raise TypeError("users should have a username")

		if email is None:
			raise TypeError("users  should have a email")

		if extra_field.get('is_staff') is not True:
			raise ValueError('is_staff is not')
		if extra_field.get('is_superuser')is not True:
			raise ValueError('is_sueruser is not')
		if extra_field.get('is_active') is not True:
			raise ValueError('is_active is not')
		user = self.create_user(
			username=username,
			email=email,
			password=password,
			is_staff=True,
			is_admin=True,
			is_superuser=True
		)
		return user

class User (AbstractBaseUser, PermissionsMixin) :
	username=models.CharField(max_length=34, unique=True, db_index=True)
	first_name=models.CharField(max_length=34)
	last_name =models.CharField(max_length=34)
	email=models.EmailField(max_length=34, unique=True, db_index=True)
	is_superuser = models.BooleanField(default=False)
	is_active = models.BooleanField(default=False)
	is_staff=models.BooleanField(default=False)
	is_roles=models.CharField(max_length=34)
	is_admin=models.BooleanField(default=False)
	USERNAME_FIELD='email'
	REQUIRED_FIELDS = ['username']
	objects=usermanager()
	def __str__(self):
		return self.email


class Admin(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)

class todoiteam(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE , related_name='todoiteam')
	title=models.CharField(max_length=200)
	completed=models.BooleanField(default=False, blank=True, null=True)


	def __str__(self):
		return self.title