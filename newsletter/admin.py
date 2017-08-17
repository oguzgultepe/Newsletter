from django.contrib import admin
from .models import Submission, Category, Admin_Pref, Subscriber, Introduction

MONTH_CHOICES= [(1,'January'),(2,'February'),(3,'March'),
  (4,'April'),(5,'May'),(6,'June'),
      (7,'July'),(8,'August'),(9,'September'),
      (10,'October'),(11,'November'),(12,'December')]

class SubmissionAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified', 'author')
    def publish_month (self, obj):
        return MONTH_CHOICES[obj.month-1][1]
    list_display= ('title_german', 'publish_month',
                   'year', 'author', 'finished')
    list_filter= ('finished','month', 'year')
    search_fields= ['title_german']
    publish_month.admin_order_field = 'year'
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
            {'fields':  ['month','year']}),
        (None,
            {'fields':  ['finished',]}),
        ('Info',
            {'fields':  ['created',
                         'modified'],
             'classes': ['collapse']})
    ]

class IntroductionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Publish Month',
            {'fields': ['month','year']}),
        (None,
            {'fields': ['german_text','english_text']})
    ]
    def publish_month (self, obj):
        return MONTH_CHOICES[obj.month-1][1]
    publish_month.admin_order_field = 'year'
    list_display = ('publish_month','year')
    list_filter = (['year'])
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Category)
admin.site.register(Admin_Pref)
#remove the next line after development
admin.site.register(Subscriber)
admin.site.register(Introduction, IntroductionAdmin)
