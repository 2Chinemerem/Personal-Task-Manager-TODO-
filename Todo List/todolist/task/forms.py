from django import forms
from task.models import Task
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, RegexValidator

class TaskForm(forms.ModelForm):
    created_at= forms.DateTimeField(widget=forms.DateTimeInput(attrs={
                'type': 'datetime-local',
            }),initial=timezone.now().strftime('%Y-%m-%dT%H:%M'))
    
    due_date= forms.DateField(widget=forms.DateInput(attrs= {"type": "date"}))
    class Meta:
        model= Task
        exclude= ("completed", "user")


class UserForm(forms.ModelForm):      
    password= forms.CharField(widget=forms.PasswordInput, validators=[
        MinLengthValidator(8, message="Password must be at least 8 characters long."),
        RegexValidator(r'[a-zA-Z]', message="Password must contain at least one letter."),
    ])
    confirm_password= forms.CharField(widget=forms.PasswordInput)

    
    class Meta():
        model= User
        fields= ["username", "password"]

    def clean(self):
        all_cleaned_data= super().clean()
        password= all_cleaned_data.get("password")
        confirm_password= all_cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Password do not match!")

 
        
class LoginForm(forms.Form):
    username= forms.CharField(max_length=256)
    password= forms.CharField(widget=forms.PasswordInput)
