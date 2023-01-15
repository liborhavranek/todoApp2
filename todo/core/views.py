from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, FormView, DeleteView, DetailView
from .models import Task, User
from .forms import TaskForm,TaskUpdateForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from  django.contrib.auth import login
from django.contrib import messages
from datetime import datetime
from django.db.models import Count, Q
from typing import Type, TypeVar, List, Dict, Union
from . import models
from django.db.models import QuerySet

# Create your views here.


class HomeView(TemplateView):
    template_name = "home.html"


class TaskCreateView(CreateView):
    model: Type[Task] = Task
    form_class: Type[TaskForm] = TaskForm
    template_name = 'add_task.html'
    success_url = reverse_lazy('task')
    
    # The form_valid method of the CreateView class returns a Boolean indicating whether the form is valid or not.
    def form_valid(self, form: TaskForm) -> bool:
        title = form.cleaned_data.get('title')
        text = form.cleaned_data.get('text')
        if len(title) < 4:
            messages.error(self.request, 'Title must be at least 4 characters long')
            return self.form_invalid(form)
        if len(text) < 10:
            messages.error(self.request, 'Text must be at least 10 characters long')
            return self.form_invalid(form)
        form.instance.user = self.request.user
        response =  super().form_valid(form)
        messages.success(self.request, 'Task created successfully!')
        return response




class TaskListView(LoginRequiredMixin, ListView):
    model: Type[Task] = Task
    template_name = 'task.html'
    ordering = ['date_planned_completion']
    context_object_name = 'tasks'
    
    def get_queryset(self)-> QuerySet:
        queryset = super().get_queryset()
        queryset = queryset.order_by('complete', 'date_planned_completion')
        return queryset
    
    # Return dictionary is because tasks will set string username of current user 
    # count will set like integer nuber of complete task 
    # done will set like integer number of incomplete task 
    def get_context_data(self, **kwargs)-> Dict[str, int]:
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user = self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        context['done'] = context['tasks'].filter(complete=True).count()
        return context
        


class TaskUpdateView(UpdateView):
    model: Type[Task] = Task 
    form_class: Type[TaskUpdateForm] = TaskUpdateForm
    template_name = 'edit_task.html'
    success_url = reverse_lazy('task')
    
    # is the same like Task create view function return valid or invalid form bool
    def form_valid(self, form:TaskUpdateForm) -> bool:
        title = form.cleaned_data.get('title')
        text = form.cleaned_data.get('text')
        if len(title) < 4:
            messages.error(self.request, 'Title must be at least 4 characters long')
            return self.form_invalid(form)
        if len(text) < 10:
            messages.error(self.request, 'Text must be at least 10 characters long')
            return self.form_invalid(form)
        form.instance.user = self.request.user
        response =  super().form_valid(form)
        messages.success(self.request, 'Task created successfully!')
        return response
    

class TaskDetailView(DetailView):
    template_name = 'detail_task.html'
    model: Type[Task] = Task
    context_object_name = 'task'



class TaskDeleteView(DeleteView):
    model: Type[Task] = Task
    context_object_name = 'task'
    template_name = 'delete_task.html'
    success_url = reverse_lazy('task')
    
    def get_queryset(self) -> QuerySet:
        owner = self.request.user
        return self.model.objects.filter(user=owner)



class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    # Union return string or reverse lazy. 
    def get_success_url(self) -> Union[str, reverse_lazy]:
        return reverse_lazy('task')
    
    
class CustomRegisterView(FormView):
    template_name = 'register.html'
    form_class: Type[UserCreationForm] = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task')
    
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(CustomRegisterView, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task')
        return super(CustomRegisterView, self).get(*args, **kwargs)
    




class AdminUserList(ListView):
    model: Type[User] = User
    template_name = "admin.html"
    
    def get_queryset(self)  -> List[User]:
        queryset = super().get_queryset()
        queryset = queryset.annotate(task_count=Count('task'))
        queryset = queryset.annotate(complete_task_count=Count('task', filter=Q(task__complete=True)))
        queryset = queryset.annotate(uncomplete_task_count=Count('task', filter=Q(task__complete=False)))
        queryset = queryset.annotate(incomplete_task_count=Count('task', filter=Q(task__complete=False) & Q(task__date_planned_completion__lt=datetime.now())))
        queryset = queryset.order_by('-incomplete_task_count')
        return queryset

    