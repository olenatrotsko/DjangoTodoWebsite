from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import TodoForm
from .models import Todo

def index(request):
    return render(request, 'todo/index.html')

def create_todo(request):
    form = TodoForm()
    context = {'form': form}

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_completed = request.POST.get('is_completed', False)

        todo = Todo()
        todo.title = title
        todo.description = description
        todo.is_completed = True if is_completed == 'on' else False
    
        todo.save()
        return HttpResponseRedirect(reverse("todo-detail", args={'id': todo.pk}))
    return render(request, 'todo/create_todo.html', context)

def todo_detail(request, id):
    return render(request, 'todo/todo_detail.html')