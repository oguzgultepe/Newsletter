from django.core.management import BaseCommand, call_command, CommandError
from django.conf import settings
from ...models import Admin_Pref
from crontab import CronTab

class Command(BaseCommand):
    help = "Schedules the cron jobs for e-mail sending"

    def handle(self, *args, **options):
        pref = Admin_Pref.objects.first()
        cron = CronTab(user=True)
        for job in cron:
            if job.comment == 'newsletter':
                cron.remove(job)
        if pref.auto_send:
            root = settings.BASE_DIR
            newsletter_job = cron.new(command='python {0}/manage.py send_newsletter'.format(root), comment='newsletter')
            reminder_job = cron.new(command='python {0}/manage.py send_reminder'.format(root), comment='newsletter')
            newsletter_date = pref.newsletter_mail_date
            reminder_date = pref.reminder_mail_date
            newsletter_job.day.on(newsletter_date)
            newsletter_job.hour.on(6)
            newsletter_job.minute.on(0)
            reminder_job.day.on(reminder_date)
            reminder_job.hour.on(6)
            reminder_job.minute.on(0)
        cron.write()
        self.stdout.write(self.style.SUCCESS("Cronjobs scheduled."))
