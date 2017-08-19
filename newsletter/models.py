from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.management import call_command

class Category(models.Model):
    name_german = models.CharField(max_length=50)
    name_english = models.CharField(max_length=50)
    priority = models.IntegerField()
    has_date = models.BooleanField(default=False)
    def __str__(self):
        return self.name_german

class Submission(models.Model):
    title_german = models.CharField(max_length=100)
    title_english = models.CharField(max_length=100)
    text_german = models.TextField(max_length=1000)
    text_english = models.TextField(max_length=1000)
    author = models.ForeignKey(User, editable=False)
    category = models.ForeignKey(Category)
    link_german = models.URLField()
    link_english = models.URLField()
    month = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(12)])
    year = models.IntegerField()
    date = models.DateField(null= True, blank=True)
    enddate = models.DateField(null= True, blank=True)
    finished = models.BooleanField(default=False)
    created= models.DateTimeField(auto_now_add=True)
    modified= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_german

class Admin_Pref(models.Model):
    reminder_mail_date = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(30)])
    last_entry_date = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(30)])
    newsletter_mail_date = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(30)])
    auto_send = models.BooleanField()
    def save(self, *args, **kwargs):
        super(Admin_Pref, self).save(*args, **kwargs)
        call_command('schedule')


class Subscriber(models.Model):
    e_mail = models.EmailField()
    def __str__(self):
        return self.e_mail

class Introduction(models.Model):
    german_text = models.TextField(max_length=1000)
    english_text = models.TextField(max_length=1000)
    month = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(12)])
    year = models.IntegerField()
