from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, LoginForm, LearningModuleSubmissionForm
from .models import LearningModules, CompletedModules

import json

# Create your views here.
def index(request):
    template = loader.get_template('occ/index.html')
    return HttpResponse(template.render(None, request))

"""
@summary: View for the user creation page.
"""
def create_user_page(request):
    submitbutton = request.POST.get("submit")
    exception = ''

    form = SignUpForm(request.POST or None)
    if form.is_valid():
        firstname = form.cleaned_data.get("first_name")
        lastname = form.cleaned_data.get("last_name")
        email = form.cleaned_data.get("email")
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        # HERE : Create a new user object and save the data if valid.
                # if not valid, return an error message.
        try:
            newuser = User.objects.create_user(username, email, password)
            newuser.save()

            #newuserpoints = UserPoints(username=username, points=0, completed_modules='{"completed_modules":[]}')
            #newuserpoints.save()
        except Exception as err:
            exception = str(err)

        # authenticate the user
        try:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("/occ/home")
            else:
                exception = "Failed to login"
        except Exception as err:
            exception = str(err)

    context = {'form':form, 'exception':exception}
    template = loader.get_template('occ/signup.html')
    return HttpResponse(template.render(context, request))

"""
@summary: View for the login page.
"""
def login_page(request):
    submitbutton = request.POST.get("submit")
    exception = ''

    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        try:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("/occ/home")
            else:
                exception = "Failed to login"
        except Exception as err:
            exception = str(err)

    context = {'form':form, 'exception':exception}
    template = loader.get_template('occ/login.html')
    return HttpResponse(template.render(context, request))

"""
@summary: The main home page.
"""
def home_page(request):
    # check user is logged in.
    points = 0
    finished_modules = {}

    if not request.user.is_authenticated:
        template = loader.get_template('occ/login.html')
    else:
        learning_modules = LearningModules.objects.all()
        for module in learning_modules:
            finished_modules[module.module_id] = module
            
        try:
            for query in CompletedModules.objects.filter(username=request.user.username):
                points += query.points
                del finished_modules[query.module_id]
                
        except Exception as err:
            print(err)
            #return redirect("/occ/home")
        
    context = {"finished_modules":[x for x in finished_modules.values()], "points":points, "learning_modules":learning_modules}
    template = loader.get_template('occ/home.html')
    return HttpResponse(template.render(context, request))

def module_page(request, id):
    if not request.user.is_authenticated:
        template = loader.get_template('occ/login.html')

    submitbutton = request.POST.get("submit")
    exception = ''

    try:
        learning_module = LearningModules.objects.get(module_id=id)
    except LearningModules.DoesNotExist:
        return HttpResponseNotFound("404: Learning Module not found")

    if not learning_module:
        return HttpResponseNotFound("404: Learning Module not found")

    form = LearningModuleSubmissionForm(request.POST or None)
    if form.is_valid():
        forminput = form.cleaned_data.get("forminput")
        if forminput:
            try:
                CompletedModules.objects.get(username=request.user.username, module_id=learning_module.module_id)
            except Exception as err:
                newcompletedmodule = CompletedModules(
                    username=request.user.username,
                    points=learning_module.module_points,
                    module_id=learning_module.module_id
                 )
                newcompletedmodule.save()
    context = {"form":form, "learning_module":learning_module}
    template = loader.get_template('occ/module.html')
    return HttpResponse(template.render(context, request))