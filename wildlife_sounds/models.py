from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager




class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a user with the given email, logo and password.
        """
        user = self.model(
            email = self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, logo and password.
        """
        user = self.create_user(
            email,
            password=password,
            **extra_fields
        )

        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user



class User(AbstractUser):
    objects = UserManager()
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Utilisateur'

    def __str__(self):
        return f'{self.username}'



class Taxon(models.Model):
    taxon_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, default='', null=True, blank=True)

class Order(models.Model):
    order_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, default='', null=True, blank=True)

class Family(models.Model):
    family_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, default='', null=True, blank=True)

class Genus(models.Model):
    genus_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, default='', null=True, blank=True)



class Specie(models.Model):
    vernacular_name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    family = models.ForeignKey(Family, on_delete=models.SET_NULL, null=True)
    genus = models.ForeignKey(Genus, on_delete=models.SET_NULL, null=True)
    taxon = models.ForeignKey(Taxon, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=1000, default='', null=True, blank=True)


class SpecieSound(models.Model):
    sound = models.FileField(upload_to="SpecieSound/")
    specie = models.ForeignKey(Specie, on_delete=models.CASCADE)
    TYPES = [("call", "Call"), ("song", "Song")]
    type = models.CharField(max_length=100, choices=TYPES)
    country = models.CharField(max_length=100, default="", null=True, blank=True)

    




# Create your models here.
