from django.contrib import admin
from .models import Submission, Category, Admin_Pref

class SubmissionAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    list_display= ('title_german', 'month_year',
                   'author', 'finished')
    list_filter= ('finished','publish_date')
    search_fields= ['title_german']
    def month_year(self, obj):
        return obj.publish_date.strftime('%b, %Y')

    month_year.admin_order_field = 'date'
    month_year.short_description = 'Publish date'

    fieldsets = [
        (None,
            {'fields':  ['category',
                         'author']}),
        ('Deutsch',
            {'fields':  ['title_german',
                         'text_german',
                         'link_german']}),
        ('English',
            {'fields':  ['title_english',
                         'text_english',
                         'link_english']}),
        ('Date',
            {'fields':  ['date'],
             'classes': ['collapse']}),
        ('Publish in:',
            {'fields':  ['publish_date']}),
        (None,
            {'fields':  ['finished',]}),
        ('Info',
            {'fields':  ['created',
                         'modified'],
             'classes': ['collapse']})
    ]

admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Category)
admin.site.register(Admin_Pref)
# Register your models here.
