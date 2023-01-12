from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, FormView, DeleteView
from .models import Task
from .forms import TaskForm,TaskUpdateForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from  django.contrib.auth import login
from django.contrib import messages

# Create your views here.


class HomeView(TemplateView):
    template_name = "home.html"


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'add_task.html'
    success_url = reverse_lazy('task')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response =  super().form_valid(form)
        messages.success(self.request, 'Task created successfully!')
        return response



class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task.html'
    ordering = ['date_planned_completion']
    context_object_name = 'tasks'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('complete', 'date_planned_completion')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user = self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        context['done'] = context['tasks'].filter(complete=True).count()
        return context
        


class TaskUpdateView(UpdateView):
    model = Task 
    form_class = TaskUpdateForm
    template_name = 'edit_task.html'
    success_url = reverse_lazy('task')
    

class TaskDeleteView(DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'delete_task.html'
    success_url = reverse_lazy('task')
    
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)



class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('task')
    
    
class CustomRegisterView(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
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
    