from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http.response import HttpResponseRedirect

# Create your views here.
class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")

#tasks = ["foo","bar","baz"]
def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    return render(request, "tasks/index.html", {
        "tasks":request.session['tasks']
    })

def add(request):
    #POST method
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            #tasks.append(task)
            request.session["tasks"] +=[task]
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "tasks/add.html", {
                "form":form
            })
    return render(request, "tasks/add.html", { #GET method
        "form":NewTaskForm()
    })