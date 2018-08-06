from django.http import HttpResponseRedirect
from django.shortcuts import render

from projekt_core.models import Project
from .forms import NewProjectForm


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
