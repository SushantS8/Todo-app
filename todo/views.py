from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required  # Protect views
from .models import Task
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Show only the logged-in user's tasks
@login_required
def task_form(request):
    tasks = Task.objects.filter(user=request.user).order_by('due_date')
    return render(request, 'task_form.html', {'tasks' : tasks})

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('due_date')
    return render(request, 'task_list.html', {'tasks' : tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due_date')
        if title:
            Task.objects.create(title=title, user=request.user, due_date=due_date)  # Assign task to user
    return redirect('task_form')

@login_required
def edit_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)    # Ensure ownership
    except Task.DoesNotExist:
        messages.error(request, "Task not found or unauthorized access!")
        return redirect('task_list')   # Prevents unauthorized access

    if request.method == 'POST':
        new_title = request.POST.get('title')
        if new_title:
            task.title = new_title
            task.save()
            messages.success(request, "Task updated successfully!")
            return redirect('task_list')
        
    return render(request, 'edit_task.html', {'task': task})

@login_required
def delete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)  # Ensure ownership
        task.delete()
    except Task.DoesNotExist:
        pass   # Ignore if task doesn't exist or doesn't belong to the user
    return redirect('task_list')

@login_required
def toggle_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)    # Ensure ownership
        task.completed = not task.completed
        task.save()
    except Task.DoesNotExist:
        pass # Ignore invalid task toggle attempts
    return redirect('task_list')

# User Registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_form')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# User Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('task_form')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
        
    return render(request, 'login.html')

# User Logout
def user_logout(request):
    logout(request)
    return redirect('login')