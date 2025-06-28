from django.urls import path
from task import views

app_name="task"

urlpatterns = [
    path('task/', views.TaskFormView, name="task"),
    path('register/', views.registration, name="register"),
    path('userlogin/', views.userlogin, name="userlogin"),
    path('adminlogin/', views.adminlogin, name="adminlogin"),
    path('aboutme/', views.aboutme, name="about"),
    path('logout/', views.userlogout, name="logout"),
    path('list/', views.TodoList.as_view(), name="list"),
    path('thankyou/', views.thankyouforvisiting, name="thankyouforvisiting"),
    path('list/<int:pk>', views.TodoListDetail.as_view(), name="detail"),
    path('update/<int:pk>', views.TodoListUpdate.as_view(), name="update"),
    path('delete/<int:pk>', views.DeleteView.as_view(), name="delete"),



]
