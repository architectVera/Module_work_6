""" Create Kinohall form """

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from kinohall.models import Movie, Session, Hall


class CreateMovieForm(forms.ModelForm):
    """
    The class describes the mod for creating a new movie
    """
    class Meta:
        """Describes the behavior of CreateMovieForm model """

        model = Movie
        fields = [
            "title",
            "image",
            "description",
            "year",
        ]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "id": "title",
                "placeholder": "Title",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "id": "description",
                "placeholder": "Description",

            }),
            "year": forms.TextInput(attrs={
                "class": "form-control",
                "id": "year",
                "placeholder": "year",
            }),
        }


class CreateHallForm(forms.ModelForm):
    """
    The class describes the mod for creating a new hall
    """
    class Meta:
        """Describes the behavior of CreateHallForm model """

        model = Hall
        fields = [
            "name",
            "seats"
        ]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "id": "name",
                "placeholder": "Name",
            }),
            "seats": forms.TextInput(attrs={
                "class": "form-control",
                "id": "seats",
                "placeholder": "seats",

            }),
        }


class CreateSessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['start_time', 'end_time', 'date', 'price', 'hall', 'movie']
        labels = {
            'start_time': 'Start time',
            'end_time': 'End time',
            'date': 'Date',
            'price': 'Price',
            'hall': 'Hall',
            'movie': 'Movie',
        }
        widgets = {
            'start_time': forms.TimeInput(
                attrs={'type': 'time',
                       'class': 'form-control'},
                format='%H:%M'
            ),
            'end_time': forms.TimeInput(
                attrs={'type': 'time',
                       'class': 'form-control'},
                format='%H:%M'
            ),
            'date': forms.DateInput(
                attrs={'type': 'date',
                       'class': 'form-control'},
                format='%d/%m/%Y'
            ),
            'price': forms.TextInput(
                attrs={'class': 'form-control',
                       'type': 'number',
                       'min': '0',
                       'max': '350'
                       }),
            'hall': forms.Select(attrs={'class': 'form-control'}),
            'movie': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        print("Method clean")
        cleaned_data = super().clean()

        hall = cleaned_data.get('hall')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        date = cleaned_data.get('date')

        # Checking that there is no other session scheduled in the room at the same time
        existing_sessions = Session.objects.filter(
            hall=hall,
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time,
        )
        print(existing_sessions)

        if existing_sessions.exists():
            raise ValidationError('This hall is already reserved at this time.')

        return cleaned_data
