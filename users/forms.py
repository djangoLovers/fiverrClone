from django.forms import ModelForm
from core.models import UserProfile
from django.contrib.auth.forms import UserCreationForm


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name',
            'description', 'biography', 'country']
