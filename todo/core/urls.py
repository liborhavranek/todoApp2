from django.urls import path, include
from .views import HomeView, TaskCreateView, TaskListView, TaskUpdateView, CustomLoginView, CustomRegisterView, TaskDeleteView, TaskDetailView, AdminUserList
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', HomeView.as_view(), name='home' ),
    path('add_task', TaskCreateView.as_view(), name='add_task'),
    path('task', TaskListView.as_view(), name='task'),
    path('edit_task/<int:pk>', TaskUpdateView.as_view(), name='edit_task'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('delete_task/<int:pk>/', TaskDeleteView.as_view(), name='delete_task'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='detail_task'),
    path('userlist', AdminUserList.as_view(), name='userlist'),
]
