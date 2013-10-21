from django.contrib import admin
from django.contrib.admin import ModelAdmin
from member.models import Student,PartyBranch,StudentAssessment,UserStudent
admin.site.register(PartyBranch)
class StudentAdmin(ModelAdmin):
    search_fields = ['student_id','name']
admin.site.register(Student,StudentAdmin)
admin.site.register(StudentAssessment)
admin.site.register(UserStudent)

