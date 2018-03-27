from django.conf.urls import patterns, url
from django.contrib import admin

import advisor.views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^advisor/addAdvisor/$', advisor.views.AddAdvisorView.as_view()),
    url(r'^advisor/getAdvisingTimetables/$', advisor.views.AdvisorView.as_view())
)