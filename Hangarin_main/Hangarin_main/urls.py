from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView, TemplateView
from Hangarin_app import views
from Hangarin_app.views import DashboardView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Auth
    path('accounts/', include('allauth.urls')),

    # Dashboard routes
    path('', DashboardView.as_view(), name='dashboard'),  # root dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard-alt'),  # allow /dashboard/ too

    # Tasks
    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    path('tasks/add/', views.TaskCreateView.as_view(), name='task-add'),
    path('tasks/<pk>/edit/', views.TaskUpdateView.as_view(), name='task-edit'),
    path('tasks/<pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),

    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category-add'),
    path('categories/<pk>/edit/', views.CategoryUpdateView.as_view(), name='category-edit'),
    path('categories/<pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),

    # Priorities
    path('priorities/', views.PriorityListView.as_view(), name='priority-list'),
    path('priorities/add/', views.PriorityCreateView.as_view(), name='priority-add'),
    path('priorities/<pk>/edit/', views.PriorityUpdateView.as_view(), name='priority-edit'),
    path('priorities/<pk>/delete/', views.PriorityDeleteView.as_view(), name='priority-delete'),

    # Subtasks
    path('subtasks/', views.SubTaskListView.as_view(), name='subtask-list'),
    path('subtasks/add/', views.SubTaskCreateView.as_view(), name='subtask-add'),
    path('subtasks/<pk>/edit/', views.SubTaskUpdateView.as_view(), name='subtask-edit'),
    path('subtasks/<pk>/delete/', views.SubTaskDeleteView.as_view(), name='subtask-delete'),

    # Notes
    path('notes/', views.NoteListView.as_view(), name='note-list'),
    path('notes/add/', views.NoteCreateView.as_view(), name='note-add'),
    path('notes/<pk>/edit/', views.NoteUpdateView.as_view(), name='note-edit'),
    path('notes/<pk>/delete/', views.NoteDeleteView.as_view(), name='note-delete'),

    # Offline page
    path('offline/', TemplateView.as_view(template_name="offline.html"), name='offline'),

    # PWA (must be LAST)
    re_path(r'^', include('pwa.urls')),
    re_path(r'^serviceworker\.js$', TemplateView.as_view(template_name="serviceworker.js", content_type='application/javascript'), name='serviceworker'),

]
