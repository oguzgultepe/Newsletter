from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import SubmissionForm, Admin_Pref
from django.contrib.auth.decorators import login_required
from datetime import date
from django.utils.timezone import now

@login_required
def submit(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            publish_year = (int) (now().strftime('%Y'))
            current_month = (int) (now().strftime('%m'))
            publish_month = (int)(form.cleaned_data['publish_month'])
            if current_month>9 & publish_month<4:
               publish_year += 1
            instance.publish_date = date(publish_year, publish_month,
                                         Admin_Pref.objects.first().newsletter_mail_date)
            instance.save()
            return HttpResponseRedirect(reverse('user'))
    else:
        form= SubmissionForm()

    return render(request, 'submit.html', {'form':form})

def display(request):
    return HttpResponse("You are at the display page")

@login_required
def user(request):
    return HttpResponse("You are at the user page")

def send(request):
    return HttpResponse("You are at the send page")

def edit(request):
    return HttpResponse("You are at the edit page")
