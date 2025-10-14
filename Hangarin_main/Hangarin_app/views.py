from django.shortcuts import render
from .models import Task

def dashboard(request):
    tasks = Task.objects.all()
    overdue = [t for t in tasks if t.is_overdue()]
    context = {
        "tasks": tasks,
        "pending": tasks.filter(status="pending").count(),
        "in_progress": tasks.filter(status="in_progress").count(),
        "completed": tasks.filter(status="completed").count(),
        "overdue": len(overdue),
    }
    return render(request, "home.html", context)
