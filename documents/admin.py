from django.contrib import admin
from django.contrib.admin import ModelAdmin
from documents.models import News,Notice,Regulation,Attachment,Price,StudentPrice
class NewsAdmin(ModelAdmin):
    search_fields = ['title']
admin.site.register(News,NewsAdmin)
admin.site.register(Notice)
admin.site.register(Regulation)
admin.site.register(Attachment)
admin.site.register(Price)
admin.site.register(StudentPrice)