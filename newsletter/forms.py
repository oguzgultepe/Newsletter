from .models import Category, Submission, Admin_Pref, Subscriber
from django.utils.timezone import timedelta,now
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.db.models import Min, Max


MONTH_CHOICES= [(1,'January'),(2,'February'),(3,'March'),
          (4,'April'),(5,'May'),(6,'June'),
          (7,'July'),(8,'August'),(9,'September'),
          (10,'October'),(11,'November'),(12,'December')]

class SubmissionForm(forms.ModelForm):
    current_day = (int) (now().strftime('%d'))
    first_month = (int) (now().strftime('%m'))
    if current_day>Admin_Pref.objects.first().last_entry_date:
        first_month+=1
    CHOICES = [MONTH_CHOICES[first_month%12],MONTH_CHOICES[(first_month+1)%12],MONTH_CHOICES[(first_month+2)%12]]
    publish_month= forms.ChoiceField(choices=CHOICES)
    class Meta:
        model = Submission
        exclude = ['month','year']
        widgets = {
            'date': SelectDateWidget,
            'enddate': SelectDateWidget
        }
        help_texts = {
            'date': _('Optional'),
            'enddate': _('Optional'),
        }
class EditForm(SubmissionForm):
    delete = forms.BooleanField(required=False)

class DisplayForm(forms.Form):
    years = Submission.objects.aggregate(Min("year"),Max("year"))
    start_year = years['year__min']
    end_year = years['year__max']
    this_year = (int) (now().strftime("%Y"))
    if end_year > this_year:
        end_year = this_year
    year_choices = [(0,"Please select a year.")]
    for x in range(start_year,end_year+1):
        year_choices.append((x,x))
    year =forms.ChoiceField(widget=forms.Select(attrs={'onchange':'this.form.submit();'}),choices=year_choices)

class MonthForm(DisplayForm):
    month = forms.ChoiceField(widget=forms.Select(attrs={'onchange':'this.form.submit();'}),choices=MONTH_CHOICES, required=False)

class CurrentYearMonthForm(DisplayForm):
    current_month = (int) (now().strftime("%m"))
    month = forms.ChoiceField(widget=forms.Select(attrs={'onchange':'this.form.submit();'}),choices=MONTH_CHOICES[:current_month], required=False)

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['e_mail']
