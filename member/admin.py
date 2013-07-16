from django.contrib import admin
from member.models import Student,PartyBranch,StudentAssessment,UserStudent
admin.site.register(PartyBranch)
admin.site.register(Student)
admin.site.register(StudentAssessment)
admin.site.register(UserStudent)