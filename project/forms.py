from django.forms import ModelForm
from user.models import Users
from project.models import Project

class formProject(ModelForm):
    class Meta:
        model = Project
        fields = ['project_name']

class formUsers(ModelForm):
    class Meta:
        model = Users
        fields = ['name','email','password']
        