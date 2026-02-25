from django import forms
from .models import Profile, Blog, Tag

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']


class BlogForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Blog
        fields = ['title', 'content', 'category', 'tags', 'image', 'img_url']
