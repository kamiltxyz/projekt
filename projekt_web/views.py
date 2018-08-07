import random
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from projekt_core.models import Project, create_step, remove_step, create_task, remove_task, move_task, activate_task, deactivate_task
from .forms import NewProjectForm, TerminalForm


# Projects
def frontpage(request):
    return render(request, "projekt_web/frontpage.html")

def new_project(request):
    if request.method == "POST":
        form = NewProjectForm(request.POST)

        if form.is_valid():
            project = Project()

            project.title = form.cleaned_data['title']
            project.owner = request.user;
            project.save()

            return HttpResponseRedirect('/')

    else:
        form = NewProjectForm()

    return render(request, "projekt_web/new_project.html", {'form': form})

def projects_list(request):
    if request.user.is_superuser:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(owner=request.user)

    return render(request, "projekt_web/project_list.html", {'projects': projects})

def project_details(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)

    active_tasks = []
    for step in project.step_set.all():
        for task in step.task_set.all().filter(active=True):
            active_tasks.append(task)

    if request.method == 'POST':
        form = TerminalForm(request.POST)

        if form.is_valid():
            command = form.cleaned_data['command'].split(' ')
            if len(command) == 0:
                return redirect('project_details', project_slug=project_slug)

            if command[0] == 'as':
                for step_title in command[1:]:
                    create_step(project, step_title)
            elif command[0] == 'rs':
                for step_title in command[1:]:
                    remove_step(project, step_title)
            elif command[0] == 'at':
                if len(command) > 1:
                    for task_title in command[2:]:
                        create_task(project, command[1], task_title)
            elif command[0] == 'rt':
                if len(command) > 1:
                    for task_title in command[2:]:
                        remove_task(project, command[1], task_title)
            elif command[0] == 'mt':
                if len(command) == 4:
                    move_task(project, command[1], command[2], command[3])
            elif command[0] == 'act':
                if len(command) > 1:
                    for task_title in command[2:]:
                        activate_task(project, command[1], task_title)
            elif command[0] == 'det':
                if len(command) > 1:
                    for task_title in command[2:]:
                        deactivate_task(project, command[1], task_title)


            return redirect('project_details', project_slug=project_slug)

    else:
        form = TerminalForm()

    return render(request, "projekt_web/project_details.html", {
        'active_tasks': active_tasks,
        'project':project,
        'form':form,
    })
