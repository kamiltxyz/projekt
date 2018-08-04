from django.shortcuts import render

def frontpage(request):
    return render(request, "projekt_web/frontpage.html")
