from django.contrib import admin
from documents.models import News,Notice,Regulation,Attachment
admin.site.register(News)
admin.site.register(Notice)
admin.site.register(Regulation)
admin.site.register(Attachment)