from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now
from ...models import Admin_Pref
from django.contrib.auth.models import User
from django.core.mail import send_mail
from smtplib import SMTPException

pref = Admin_Pref.objects.first()
day = pref.last_entry_date
from_mail = pref.sender
month = (((int) (now().strftime('%m')))-1)%12
MONTHS= ['January', 'February', 'March',
         'April' ,'May' ,'June',
         'July', 'August', 'September',
         'October', 'November', 'December']
reminder_text="""Dear Members of the Fachschaft,
we would like to kindly remind you that \
the last submission date for \
the {0} Newsletter is {1} {2}.
Thank you for your concern,
Newsletter Team""".format(MONTHS[month+1],day, MONTHS[month])

email_list = list(User.objects.values_list('email', flat=True))

class Command(BaseCommand):
    help = "Sends the submission reminder."

    def handle(self, *args, **options):
        try:
            send_mail(
                'Newsletter Reminder',
                reminder_text,
                from_mail,
                email_list,
                fail_silently=False
            )
        except SMTPException:
            raise CommandError("Reminder mail could not be sent!")
        self.stdout.write(self.style.SUCCESS("Successfully sent the newsletter reminder."))
