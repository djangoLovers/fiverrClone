from django.forms import ModelForm
from .models import UserProfile


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name',
            'description', 'biography', 'country', 'image']
