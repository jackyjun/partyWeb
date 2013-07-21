from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^news/(?P<id>\d+)','documents.views.get_news'),
    url(r'^notice/(?P<id>\d+)','documents.views.get_notice'),
    url(r'^regulation/(?P<id>\d+)','documents.views.get_regulation'),
    url(r'list_news/(?P<page>\d+)','documents.views.list_news'),
    url(r'list_notice/(?P<type>\d+)/(?P<page>\d+)','documents.views.list_notice'),
    url(r'list_regulation/(?P<page>\d+)','documents.views.list_regulation'),
    url(r'list_price/','documents.views.list_price'),
    url(r'apply_price/(?P<id>\d+)','documents.views.apply_price'),
    url(r'cancel_price/(?P<id>\d+)','documents.views.cancel_price'),
    url(r'price_detail/(?P<id>\d+)','documents.views.price_detail'),
    url(r'student_price/','documents.views.student_price'),
    url(r'examine_price/(?P<id>\d+)','documents.views.examine_price'),
    url(r'examine_price_result/(?P<id>\d+)','documents.views.examine_price_result'),
    url(r'examine_price_list/','documents.views.examine_price_list'),
    url(r'attachment_list/','documents.views.attachment_list'),
    url(r'get_attachment/(?P<id>\d+)','documents.views.get_attachment'),
    url(r'user_login/', 'member.views.login_view'),
    url(r'login/', 'member.views.user_login'),
    url(r'logout/', 'member.views.user_logout'),
    url(r'home/', 'member.views.home'),
    url(r'student_center/', 'member.views.student_center'),
    url(r'^student_info/', 'member.views.student_info'),
    url(r'branch_summary/','member.views.branch_summary'),
    url(r'branch_detail/(?P<id>\d+)','member.views.branch_detail'),
    url(r'branch_assessment/','member.views.branch_assessment'),
    url(r'branch_search/','member.views.branch_search'),
    url(r'join_activity/(?P<id>\d+)','activity.views.join_activity'),
    url(r'cancel_activity/(?P<id>\d+)','activity.views.cancel_activity'),
    url(r'^activity_detail/(?P<id>\d+)','activity.views.get_activity'),
    url(r'list_activity/(?P<type>\d+)','activity.views.list_activity'),
    url(r'user_activity_detail/','activity.views.user_activity_detail'),
    #back
    url(r'add_activity/','activity.views.add_activity'),
    url(r'modify_activity/(?P<id>\d+)','activity.views.modify_activity'),
    url(r'delete_activity/(?P<id>\d+)','activity.views.delete_activity'),
    url(r'search_activity','activity.views.search_activity'),
    url(r'examine_activity/(?P<id>\d+)','activity.views.examine_activity'),
    url(r'examine_result/(?P<id>\d+)','activity.views.examine_result'),
    url(r'search_student_activity/','activity.views.search_student_activity'),
    url(r'^student_activity_detail/(?P<id>\d+)','activity.views.student_activity_detail'),
    url(r'^back_student_info/(?P<id>\d+)','member.views.back_student_info'),
    # Examples:
    # url(r'^$', 'partyWebsite.views.home', name='home'),
    # url(r'^partyWebsite/', include('partyWebsite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

)
