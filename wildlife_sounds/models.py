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

    def __str__(self):
        return self.taxon_name

class Order(models.Model):
    order_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, default='', null=True, blank=True)

    def __str__(self):
        return self.order_name

class Family(models.Model):
    family_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, default='', null=True, blank=True)

    def __str__(self):
        return self.family_name

class Genus(models.Model):
    genus_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, default='', null=True, blank=True)

    def __str__(self):
        return self.genus_name



class Specie(models.Model):
    vernacular_name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    family = models.ForeignKey(Family, on_delete=models.SET_NULL, null=True)
    genus = models.ForeignKey(Genus, on_delete=models.SET_NULL, null=True)
    taxon = models.ForeignKey(Taxon, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=1000, default='', null=True, blank=True)

    def __str__(self):
        return self.vernacular_name


class SpecieSound(models.Model):
    sound = models.FileField(upload_to="SpecieSound/")
    specie = models.ForeignKey(Specie, on_delete=models.CASCADE)
    TYPES = [("call", "Call"), ("song", "Song")]
    type = models.CharField(max_length=100, choices=TYPES)
    country = models.CharField(max_length=100, default="", null=True, blank=True)

    def __str__(self):
        return f"{self.specie.vernacular_name} - {self.type} ({self.country})" 

    
class List(models.Model):
    # List of birds you want to learn.
    name = models.CharField(max_length=100)
    description = models.TextField(default = '', null = True, blank = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.user.username}"




class SpecieForList(models.Model):
    specie = models.ForeignKey(Specie, on_delete=models.CASCADE)
    list = models.ForeignKey(List, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.specie.vernacular_name} - {self.list.name}"
    

class Score(models.Model):
    score = models.IntegerField('score')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.score} ({self.date} / {self.user.username})"



class UnknownSpecie(models.Model):
    scientific_name = models.CharField(max_length=100)


# Create your models here.
