import random
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from projekt_core.models import Project, create_step, remove_step
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

    if request.method == 'POST':
        form = TerminalForm(request.POST)

        if form.is_valid():
            command = form.cleaned_data['command'].split(' ')

            if len(command) > 1:
                if command[0] == 'as':
                    if len(command) >= 2:
                        create_step(project, command[1])
                elif command[0] == 'rs':
                    if len(command) >= 2:
                        remove_step(project, command[1])

            return redirect('project_details', project_slug=project_slug)

    else:
        form = TerminalForm()

    return render(request, "projekt_web/project_details.html", {
        'project':project,
        'form':form,
    })
