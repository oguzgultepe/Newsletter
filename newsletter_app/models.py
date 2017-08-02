from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=50)
    priority = models.IntegerField()
    def __str__(self):
        return self.name

class Submission(models.Model):
    title_german = models.CharField(max_length=50)
    title_english = models.CharField(max_length=50)
    text_german = models.TextField(max_length=1000)
    text_english = models.TextField(max_length=1000)
    author = models.ForeignKey(User, editable=False)
    category = models.ForeignKey(Category)
    link_german = models.URLField()
    link_english = models.URLField()
    publish_date = models.DateField()
    date = models.DateField(null= True, blank=True)
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


