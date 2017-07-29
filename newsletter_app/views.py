from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import SubmissionForm, Admin_Pref, Submission, EditForm
from django.contrib.auth.decorators import login_required
from datetime import date
from django.utils.timezone import now
from django.views import generic

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
            return HttpResponseRedirect(reverse('newsletter:user'))
    else:
        form= SubmissionForm()

    return render(request, 'submit.html', {'form':form})

class DetailView(generic.DetailView):
    model = Submission
    template_name = 'detail.html'
    fields= ['title_german', 'text_german', 'link_german',
             'title_english', 'text_english', 'link_english',
             'category', 'publish_date', 'date']

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
        form = EditForm(request.POST)
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
            instance.publish_date = date(publish_year, publish_month,
                                         Admin_Pref.objects.first().newsletter_mail_date)
            instance.save()
            return HttpResponseRedirect(reverse('newsletter:user'))
    else:
        submission = get_object_or_404(Submission, pk=pk)
        if submission.author!=request.user:
            return HttpResponse("You are not allowed to see this page")
        form = EditForm(instance=submission)

    return render(request, 'edit.html', {'form':form, 'submission_id':pk})

#TODO
def index(request):
    return HttpResponse("You are visiting the display page.")

def display(request):
    return HttpResponse("You are visiting the display page.")

@login_required
def send(request):
    return HttpResponse("You are at the send page")
