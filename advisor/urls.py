from django.conf.urls import patterns, url
from django.contrib import admin

import advisor.views

admin.autodiscover()

urlpatterns = patterns('',
    # viewer management
    url(r'^advisor/addAdvisor/$', advisor.views.AddAdvisorView.as_view()),
    url(r'^advisor/getAdvisingTimetables/(?P<sem_name>.+)/(?P<year>[0-9]{4})/$', advisor.views.AdvisorView.as_view()),
    url(r'^advisor/deleteAdvisor/(?P<sem_name>.+)/(?P<year>[0-9]{4})/(?P<tt_name>.+)/(?P<student_email>.+)/$',
                               advisor.views.AdvisorView.as_view()),
    url(r'^advisor/getAdvisor/(?P<sem_name>.+)/(?P<year>[0-9]{4})/(?P<tt_id>.+)/$', advisor.views.RetrieveAdvisorView.as_view()),
)
