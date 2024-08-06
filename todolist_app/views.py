from django.shortcuts import render,redirect
from django.http import HttpResponse
from todolist_app.models import TaskList
from todolist_app.form import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


# Create your views here.
#addingtask
@ login_required
def todolist(request):
    if request.method=='POST':
        form=TaskForm(request.POST or None)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.manage=request.user
            instance.save()
        messages.success(request,("new task added"))
        return redirect('todolist')
    else:
        all_tasks=TaskList.objects.filter(manage=request.user)
        paginator=Paginator(all_tasks,5)
        page=request.GET.get('pg')
        all_tasks=paginator.get_page(page)
        return render(request,'todolist.html',{'all_tasks':all_tasks})
#delete    
def delete_task(request,task_id):
    task=TaskList.objects.get(pk=task_id)
    task.delete()
    return redirect('todolist')
#edit
def edit_task(request,task_id):
   if request.method=='POST':
        task=TaskList.objects.get(pk=task_id)
        form=TaskForm(request.POST or None,instance=task)
        if form.is_valid():
            form.save()
            
        messages.success(request,("task edited"))
        return redirect('todolist')
   else:
        task_obj=TaskList.objects.get(pk=task_id)
        return render(request,'edit.html',{'task_obj':task_obj})
#done
def completed_task(request,task_id):
    task=TaskList.objects.get(pk=task_id)
    task.done=True
    task.save()
    return redirect('todolist')

def pending_task(request,task_id):
    task=TaskList.objects.get(pk=task_id)
    task.done=False
    task.save()
    return redirect('todolist')

def index(request):
    context={
        'index_text':"welcome home"
    }
    return render(request,'index.html',context)
@ login_required
def contact(request):
    context={
        'contact_text':"welcome contact"
    }
    return render(request,'contact.html',context)
@ login_required
def about(request):
    context={
        'about_text':"welcome about"
    }
    return render(request,'about.html',context)
