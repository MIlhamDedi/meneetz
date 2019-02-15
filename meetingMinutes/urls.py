from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

from .views import MeetingMinuteCreateView, MeetingMinuteDetailView, MeetingMinuteListView

urlpatterns = [
    path('list', MeetingMinuteListView.as_view(template_name='meeting_minute_list.html'), name='list_meeting_minutes'),
    path('create', MeetingMinuteCreateView.as_view(template_name='meeting_minute_create_form.html'), name='create_meeting_minute'),
    path('<pk>', MeetingMinuteDetailView.as_view(template_name='meeting_minute_detail.html'), name='meeting_minute_detail')
]
