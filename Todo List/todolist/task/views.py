from django.shortcuts import render
from task.forms import TaskForm, UserForm, LoginForm
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView,UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from task.models import Task
from django.http import Http404
from django.db.models import Q

# Create your views here.
class DeleteView(LoginRequiredMixin, DeleteView):
    template_name= "crud/confirmdelete.html"
    success_url= reverse_lazy("task:list")

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = type("", (), {"instance": self.object})()
        return context
    

class TodoList(LoginRequiredMixin, ListView):
    template_name= "crud/list.html"
    context_object_name= "todos"

    queried= False
    def get_queryset(self):

        queryset= Task.objects.filter(user=self.request.user).order_by('due_date')
        query = self.request.GET.get('search')

        if query:
            self.queried= True
            results= Task.objects.filter(
                Q(title__icontains=query) & Q(user=self.request.user)
            )
            
            if results.exists():
                return results
            else:
                return Task.objects.none()
        return queryset
    
        # return Task.objects.none()  # Return empty queryset if no search input

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["queried"]= self.queried
        

        return context
    
    

class TodoListDetail(LoginRequiredMixin, DetailView):
    template_name = "crud/detail.html"
    context_object_name= "todo"
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
class TodoListUpdate(LoginRequiredMixin, UpdateView):
    template_name = "crud/form.html"
    model= Task
    fields= ("title", "description", "due_date", "completed",)
    context_object_name= "form"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)



@login_required
def userlogout(request):
    logout(request)
    return redirect(reverse("task:thankyouforvisiting"))



def userlogin(request):
    failedattempt= False
    form= LoginForm()
    if request.method == "POST":
        form= LoginForm(request.POST)
        if form.is_valid():
            username= request.POST.get("username")
            password= request.POST.get("password")

            user= authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse("task:list"))
                else:
                    return HttpResponse("Account Locked!")
            else:
                failedattempt= True

    return render(request, "userlogin.html", {"fail": failedattempt, "form":form})


def adminlogin(request):
    failedattempt= False
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid:
            username= request.POST.get("username")
            password= request.POST.get("password")

            user= authenticate(username=username, password=password)
            if user:
                if user.is_staff:
                    login(request, user)
                    return redirect(reverse("admin:index"))
                else:
                    return HttpResponse(f"{username.upper()} PLEASE BE CAREFUL SO YOUR ACCOUNT DOESNT GET BANNED!")
            else:
                failedattempt= True

    return render(request, "adminlogin.html", {"fail": failedattempt, "form":form})

    


def registration(request):
    form= UserForm()
    passworderror= False
    invalid= False

    if request.method == "POST":
        form= UserForm(request.POST)
        if form.is_valid():
            user= form.save()
            user.set_password(user.password)
            user.save()

            login(request, user)
            return redirect(reverse("task:list"))

    context= {'form': form}
    return render(request, "registration.html", context)

def index(request):
    return render(request, "index.html")

@login_required
def TaskFormView(request):
    form = TaskForm()

    if request.method == "POST":
        form =TaskForm(request.POST)

        if form.is_valid:
            task= form.save(commit=False)
            task.user= request.user
            task.save()

            return redirect(reverse("task:list"))
        

    return render(request, "crud/form.html", {'form': form})


    
def aboutme(request):
    return render(request, 'aboutme.html')

def thankyouforvisiting(request):
    return render(request, "thankyou.html")
    
    