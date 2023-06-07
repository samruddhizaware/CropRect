from django.forms import ModelForm
from .models import TestClass

class TestClassForm(ModelForm):
    class Meta:
        model = TestClass
        fields = '__all__'