from django.urls import path, include
from .views import HomeView, TaskCreateView, TaskListView, TaskUpdateView
urlpatterns = [
    path('', HomeView.as_view(), name='home' ),
    path('add_task', TaskCreateView.as_view(), name='add_task'),
    path('task', TaskListView.as_view(), name='task'),
    path('edit_task/<int:pk>', TaskUpdateView.as_view(), name='edit_task'),

]
