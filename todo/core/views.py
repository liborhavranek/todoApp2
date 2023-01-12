from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView
from .models import Task
from .forms import TaskForm


# Create your views here.


class HomeView(TemplateView):
    template_name = "home.html"


class TaskCreateView(CreateView):
    model = Task
    fields = ['title', 'text', 'date_planned_completion']
    template_name = 'add_task.html'
    success_url = reverse_lazy('task')


class TaskListView(ListView):
    model = Task
    template_name = 'task.html'
    ordering = ['date_planned_completion']
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('complete', 'date_planned_completion')
        return queryset


class TaskUpdateView(UpdateView):
    model = Task 
    form_class = TaskForm
    template_name = 'edit_task.html'
    success_url = reverse_lazy('task')
    
