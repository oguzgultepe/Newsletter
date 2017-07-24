from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import timedelta,now
from django.forms import ModelForm, extras, ChoiceField
from django.utils.translation import ugettext_lazy as _
from django.forms.extras.widgets import SelectDateWidget

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


class SubmissionForm(ModelForm):
    MONTH_CHOICES= [(1,'January'),(2,'February'),(3,'March'),
              (4,'April'),(5,'May'),(6,'June'),
              (7,'July'),(8,'August'),(9,'September'),
              (10,'October'),(11,'November'),(12,'December')]
    current_day = (int) (now().strftime('%d'))
    first_month = (int) (now().strftime('%m'))
    if current_day>Admin_Pref.objects.first().last_entry_date:
        first_month+=1
    CHOICES = [MONTH_CHOICES[first_month%12],MONTH_CHOICES[(first_month+1)%12],MONTH_CHOICES[(first_month+2)%12]]
    publish_month= ChoiceField(choices=CHOICES)
    class Meta:
        model = Submission
        exclude = ['publish_date']
        widgets = {
            'date': SelectDateWidget
        }
        help_texts = {
            'date': _('Optional'),
        }
