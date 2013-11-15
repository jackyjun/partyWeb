from django.contrib import admin
from activity.models import Activity,StudentActivity
admin.site.register(StudentActivity)
admin.site.register(Activity)