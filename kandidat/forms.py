from django.contrib.auth import get_user_model
from django.forms import ModelForm,BaseForm

class RegisterForm(ModelForm):

    class Meta:
        model = get_user_model()
        fields = ['username','password']



