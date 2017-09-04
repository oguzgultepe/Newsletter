# vim:fileencoding=utf-8
from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now
from django.core.mail import send_mass_mail
from smtplib import SMTPException
from django.urls import reverse
from ...models import Subscriber, Submission, Category, Introduction, Admin_Pref
from_mail = Admin_Pref.objects.first().sender
def generate_newsletter(month, year):
    submissions = Submission.objects.filter(month=month, year=year)
    newsletter = "--English version below--\n\n"
    newsletter += Introduction.objects.get(month=month, year=year).german_text
    newsletter += "\n\nThemen in diesem Newsletter:\n"
    categories = Category.objects.order_by('priority')
    counter = 1
    for c in categories:
        newsletter += "{0} \n".format(c.name_german)
        temp = submissions.filter(category=c)
        if c.has_date:
            temp.order_by('date')
        for submission in temp:
            if submission.finished:
                newsletter += "{0}. {1} \n".format(counter, submission.title_german)
                counter+=1
        newsletter += "\n"
    counter = 1
    for c in categories:
        newsletter += "\n{0} \n\n".format(c.name_german)
        temp = submissions.filter(category=c)
        if c.has_date:
            temp.order_by('date')
        for submission in temp:
            if submission.finished:
                newsletter += "{0}. {1} \n".format(counter, submission.title_german)
                if c.has_date:
                    if submission.enddate is not None:
                        newsletter += "Vom {0} bis {1}\n".format(submission.date.strftime('%d/%m/%y'), submission.enddate.strftime('%d/%m/%y'))
                    else:
                        newsletter += "Am {0}\n".format(submission.date.strftime('%d/%m/%y'))
                newsletter += "{0} \n\n".format(submission.text_german)
                newsletter += "{0} \n\n".format(submission.link_german)
                counter+=1
        newsletter += "\n"
    newsletter += """Wenn euch der Newsletter gefallen hat, \
würden wir uns freuen, wenn ihr ihn \
an eure Freunde weiterempfehlt.
Registrieren kann man sich unter
https://mpi.fs.tum.de/newsletter/index

Viele Grüße,
Eure Fachschaft MPI"""
    newsletter += "\n\n\n------------------------------------------\n\n\n"
    newsletter += Introduction.objects.get(month=month, year=year).english_text
    newsletter += "\n\nTopics in this newsletter:\n"
    categories = Category.objects.order_by('priority')
    counter = 1
    for c in categories:
        newsletter += "{0} \n".format(c.name_english)
        temp = submissions.filter(category=c)
        if c.has_date:
            temp.order_by('date')
        for submission in temp:
            if submission.finished:
                newsletter += "{0}. {1} \n".format(counter, submission.title_english)
                counter+=1
        newsletter += "\n"
    counter = 1
    for c in categories:
        newsletter += "\n{0} \n\n".format(c.name_english)
        temp = submissions.filter(category=c)
        if c.has_date:
            temp.order_by('date')
        for submission in temp:
            if submission.finished:
                if c.has_date:
                    if submission.enddate is not None:
                        newsletter += "From {0} to {1}\n".format(submission.date.strftime('%d/%m/%y'), submission.enddate.strftime('%d/%m/%y'))
                    else:
                        newsletter += "On {0}\n".format(submission.date.strftime('%d/%m/%y'))
                newsletter += "{0}. {1} \n".format(counter, submission.title_english)
                newsletter += "{0} \n\n".format(submission.text_english)
                newsletter += "{0} \n\n".format(submission.link_english)
                counter+=1
        newsletter += "\n"
    newsletter += """If you like our newsletter, we would appreciate it if you recommend the\
newsletter to your friends.
One can register at
https://mpi.fs.tum.de/newsletter/index

Best regards,
Your Departmental Student Council MPI (Fachschaft MPI)

--

Fachschaft Mathematik/Physik/Informatik
Technische Universität München
Boltzmannstraße 3
85748 Garching

E-Mail: fsmpi@fs.tum.de
Tel: (+49) 089 289 18545
Fax: (+49) 089 289 18546
https://mpi.fs.tum.de


Newsletter abbestellen/Unsubscribe:
"""
    return newsletter

class Command(BaseCommand):
    help = "Sends the next month's newsletter."

    def add_arguments(self, parser):
        parser.add_argument(
            '--current',
            action = 'store_true',
            dest = 'current',
            default = False,
            help = "Sends the current month's newsletter."
        )

    def handle(self, *args, **options):
        month = ((int) (now().strftime('%m')))%12
        if options['current']:
            month = (month-1)%12
        year = now().strftime('%Y')
        if not options['current'] and month==11:
            year +=1
        MONTHS= ['January', 'February', 'March',
                 'April' ,'May' ,'June',
                 'July', 'August', 'September',
                 'October', 'November', 'December']
        subject = "{0} Newsletter".format(MONTHS[month])
        newsletter = generate_newsletter(month+1, year)
        subscribers = Subscriber.objects.all()
        mail_list = []
        for subscriber in subscribers:
            text = newsletter + "https://mpi.fs.tum.de" + reverse('newsletter:unsubscribe', args=(subscriber.pk,))
            mail_list.append((subject, text, from_mail, [subscriber.e_mail]))

        try:
            send_mass_mail(mail_list, fail_silently=False)
        except SMTPException:
            raise CommandError("Newsletter could not be sent!")

        self.stdout.write(self.style.SUCCESS("Successfully sent the newsletter for {0} {1}.".format(MONTHS[month], year)))
