from django.urls import reverse
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import MeetingMinute
from .forms import MeetingMinuteForm

class MeetingMinuteDetailView(DetailView):
    model = MeetingMinute

class MeetingMinuteListView(ListView):
    model = MeetingMinute

class MeetingMinuteCreateView(CreateView):
    model = MeetingMinute
    form_class = MeetingMinuteForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(MeetingMinuteCreateView, self).form_valid(form)
