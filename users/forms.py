# users/forms.py
from django import forms
from users.models import User

class ProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = '__all__'
