from django.conf.urls import patterns, url
from django.contrib import admin

import comments.views

admin.autodiscover()

urlpatterns = patterns('',
    # viewer management
    url(r'^comments/addComment/$', comments.views.CommentView.as_view()),
    url(r'^comments/editComment/$', comments.views.CommentView.as_view()),
    url(r'^comments/getComments/(?P<tt_id>.+)/$',
                               comments.views.CommentView.as_view()),
    url(r'^comments/removeComment/(?P<comment_id>.+)/$', comments.views.CommentView.as_view()),
)
