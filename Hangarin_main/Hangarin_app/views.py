from django.db.models import Q
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Task, Category, Priority, SubTask, Note
from .forms import TaskForm
from django import forms


# --------------------------
# DASHBOARD VIEW
# --------------------------

class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # always fetch live data
        tasks = Task.objects.all()

        # make sure to trigger DB queries freshly
        context["total_tasks"] = tasks.count()
        context["completed_tasks"] = tasks.filter(status="completed").count()
        context["pending_tasks"] = tasks.filter(status="pending").count()
        context["overdue_tasks"] = tasks.filter(deadline__lt=timezone.now(), status__in=["pending", "in_progress"]).count()

        # get only last 5 for preview
        context["recent_tasks"] = tasks.order_by("-created_at")[:5]

        return context
    

# --------------------------
# TASK CRUD
# --------------------------
class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'
    paginate_by = 20  # Adjust as needed
    
    def get_queryset(self):
        qs = super().get_queryset().select_related("priority", "category")
        query = self.request.GET.get("q")
        sort_by = self.request.GET.get("sort_by")

        if query:
            qs = qs.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(category__name__icontains=query)
                | Q(priority__name__icontains=query)
            )

        allowed = ["title", "deadline", "status", "priority__name", "category__name"]
        if sort_by in allowed:
            qs = qs.order_by(sort_by)
        else:
            qs = qs.order_by("deadline")

        return qs


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task_delete.html'
    success_url = reverse_lazy('task-list')


# --------------------------
# CATEGORY CRUD
# --------------------------
class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'
    paginate_by = 20  # Adjust as needed


class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']
    template_name = 'category_form.html'
    success_url = reverse_lazy('category-list')


class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']
    template_name = 'category_form.html'
    success_url = reverse_lazy('category-list')


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category_delete.html'
    success_url = reverse_lazy('category-list')


# --------------------------
# PRIORITY CRUD
# --------------------------
class PriorityListView(ListView):
    model = Priority
    template_name = 'priority_list.html'
    context_object_name = 'priorities'
    paginate_by = 20  # Adjust as needed


class PriorityCreateView(CreateView):
    model = Priority
    fields = ['name']
    template_name = 'priority_form.html'
    success_url = reverse_lazy('priority-list')


class PriorityUpdateView(UpdateView):
    model = Priority
    fields = ['name']
    template_name = 'priority_form.html'
    success_url = reverse_lazy('priority-list')


class PriorityDeleteView(DeleteView):
    model = Priority
    template_name = 'priority_delete.html'
    success_url = reverse_lazy('priority-list')


# --------------------------
# SUBTASK CRUD
# --------------------------
class SubTaskListView(ListView):
    model = SubTask
    template_name = 'subtask_list.html'
    context_object_name = 'subtasks'
    paginate_by = 20  # Adjust as needed


class SubTaskCreateView(CreateView):
    model = SubTask
    fields = ['task', 'title', 'status']
    template_name = 'subtask_form.html'
    success_url = reverse_lazy('subtask-list')


class SubTaskUpdateView(UpdateView):
    model = SubTask
    fields = ['task', 'title', 'status']
    template_name = 'subtask_form.html'
    success_url = reverse_lazy('subtask-list')


class SubTaskDeleteView(DeleteView):
    model = SubTask
    template_name = 'subtask_delete.html'
    success_url = reverse_lazy('subtask-list')


# --------------------------
# NOTE CRUD
# --------------------------
class NoteListView(ListView):
    model = Note
    template_name = 'note_list.html'
    context_object_name = 'notes'
    paginate_by = 20  # Adjust as needed


class NoteCreateView(CreateView):
    model = Note
    fields = ['task', 'content']
    template_name = 'note_form.html'
    success_url = reverse_lazy('note-list')


class NoteUpdateView(UpdateView):
    model = Note
    fields = ['task', 'content']
    template_name = 'note_form.html'
    success_url = reverse_lazy('note-list')


class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'note_delete.html'
    success_url = reverse_lazy('note-list')
