from django import forms
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from .models import Review, Rating, RatingStar


class ReviewForm(forms.ModelForm):
    """Форма отзывов"""
    captcha = ReCaptchaField()

    class Meta:
        model = Review
        fields = ("name", "email", "text", "captcha")
        # widget потому что мы будем рендерить нашу форму
        # (а нам нужно чтоб остались норм стили полей формы)
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control border"}),
            "email": forms.EmailInput(attrs={"class": "form-control border"}),
            "text": forms.Textarea(attrs={"class": "form-control border", "id": "contactcomment"})
        }


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(),
        empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star",)

#region ========= Profile =============
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    """ Форма регистрации Юзера """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    """ Форма изменения инфы Профиля юзера """
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["likeability", 'user', 'blocked_by']

#endregion =========/Profile =============
