from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date,timedelta
from django.utils.timezone import now
from django.views import generic
from django.core.management.base import CommandError
from django.core.management import call_command

from .models import Admin_Pref, Submission, Subscriber
from . import forms
@login_required
def submit(request):
    if request.method == 'POST':
        form = forms.SubmissionForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            publish_year = (int) (now().strftime('%Y'))
            current_month = (int) (now().strftime('%m'))
            publish_month = (int)(form.cleaned_data['publish_month'])
            if current_month>9 & publish_month<4:
               publish_year += 1
            instance.month = publish_month
            instance.year = publish_year
            instance.save()
            return HttpResponseRedirect(reverse('newsletter:user'))
    else:
        form = forms.SubmissionForm()

    return render(request, 'submit.html', {'form':form})

class DetailView(generic.DetailView):
    model = Submission
    template_name = 'detail.html'

@login_required
def user(request):
    user= request.user
    submissions_unfinished = Submission.objects.filter(author=user,
                                                       finished=False)
    submissions_finished = Submission.objects.filter(author=user,
                                                       finished=True)
    context={'submissions_unfinished':submissions_unfinished,
             'submissions_finished':submissions_finished}
    return render(request, 'user.html', context=context)

@login_required
def edit(request,pk):
    if request.method == 'POST':
        form = forms.EditForm(request.POST)
        if form.is_valid():
            instance = get_object_or_404(Submission, pk=pk)
            if form.cleaned_data['delete']:
                instance.delete()
                return HttpResponseRedirect(reverse('newsletter:user'))
            instance.title_german= form.cleaned_data['title_german']
            instance.title_english= form.cleaned_data['title_english']
            instance.text_german = form.cleaned_data['text_german']
            instance.text_english = form.cleaned_data['text_english']
            instance.link_german= form.cleaned_data['link_german']
            instance.link_english= form.cleaned_data['link_english']
            instance.category= form.cleaned_data['category']
            instance.date= form.cleaned_data['date']
            instance.finished= form.cleaned_data['finished']
            publish_year = (int) (now().strftime('%Y'))
            current_month = (int) (now().strftime('%m'))
            publish_month = (int)(form.cleaned_data['publish_month'])
            if current_month>9 & publish_month<4:
               publish_year += 1
            instance.month = publish_month
            instance.year = publish_year
            instance.save()
            return HttpResponseRedirect(reverse('newsletter:user'))
    else:
        submission = get_object_or_404(Submission, pk=pk)
        if submission.author!=request.user:
            return HttpResponse("You are not allowed to see this page")
        form = forms.EditForm(instance=submission,
                              initial={'publish_month':submission.month})

    return render(request, 'edit.html', {'form':form, 'submission_id':pk})

def index(request):
    if request.method == 'POST':
        form = forms.SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Subscribed!")
            return HttpResponseRedirect(reverse('newsletter:index'))
    else:
        form = forms.SubscriberForm()

    return render(request,'index.html', {'form':form})

def display(request):
    if 'year' in request.GET:
        year = (int) (request.GET['year'])
        if year == 0:
            form = forms.DisplayForm()
            context = {'form':form,'submission_list':None}
            return render(request,'display.html',context)
        this_year = (int) (now().strftime("%Y"))
        if year == this_year:
            form = forms.CurrentYearMonthForm(request.GET)
        else:
            form = forms.MonthForm(request.GET)
        context = {'form':form,'submission_list':None}
        if 'month' in request.GET:
            month = (int) (request.GET['month'])
            start = date(year,month,1)
            end = start + timedelta(days=30)
            context['submission_list'] = Submission.objects.filter(year=year,
                                                                   month=month)
    else:
        form = forms.DisplayForm()
        context = {'form':form,'submission_list':None}
    return render(request,'display.html',context)

def unsubscribe(request,pk):
    instance = get_object_or_404(Subscriber, pk=pk)
    if request.method == 'POST':
        form = forms.SubscriberForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['e_mail'] == instance.e_mail:
                instance.delete()
                messages.success(request, "Unsubscribed!")
                return HttpResponseRedirect(reverse('newsletter:index'))
        messages.warning(request, "This e-mail address isn't correct")

    else:
        form = forms.SubscriberForm()
    return render(request,'unsubscribe.html', {'form':form,'pk':pk})

## mtype 1 for reminder, 2 for newsletter
@login_required
def send(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden('You do not have permission to view this page!')
    return render(request,'send.html')


@login_required
def send_newsletter(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden('You do not have permission to view this page!')
    try:
        call_command('send_newsletter')
    except CommandError as c:
        return HttpResponse(str(c.message))
    return HttpResponse("Newsletter sent!")


@login_required
def send_reminder(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden('You do not have permission to view this page!')
    try:
        call_command('send_reminder')
    except CommandError as c:
        return HttpResponse(str(c.message))
    return HttpResponse("Reminder sent!")
