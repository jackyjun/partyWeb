from django.contrib import admin
from django.contrib.admin import ModelAdmin
from documents.models import News,Notice,Regulation,Attachment,Price,NivoSlider,StudentPrice
class NewsAdmin(ModelAdmin):
    search_fields = ['title']
class PriceAdmin(ModelAdmin):
    exclude = ['status']
admin.site.register(News,NewsAdmin)
admin.site.register(Notice)
admin.site.register(Regulation)
admin.site.register(Attachment)
admin.site.register(StudentPrice)
admin.site.register(Price,PriceAdmin)
admin.site.register(NivoSlider)