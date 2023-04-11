""" Create Kinohall form """

from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from kinohall.models import Movie, Session, Hall


class CreateMovieForm(forms.ModelForm):
    """The class describes the mod for creating a new movie"""

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
    """The class describes the mod for creating a new hall"""

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
    """The class describes the mod for creating a new session"""

    class Meta:
        """Describes the behavior of CreateSessionForm model """

        model = Session
        fields = ['start_time', 'end_time', 'start_date', 'end_date', 'price', 'hall', 'movie']
        labels = {
            'start_time': 'Start time',
            'end_time': 'End time',
            'start_date': 'Start Date',
            'end_date': 'End Date',
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
            'start_date': forms.DateInput(
                attrs={'type': 'date',
                       'class': 'form-control'},
                format='%d/%m/%Y'
            ),
            'end_date': forms.DateInput(
                attrs={'type': 'date',
                       'class': 'form-control'},
                format='%d/%m/%Y'
            ),
            'price': forms.TextInput(
                attrs={'class': 'form-control',
                       'type': 'number',
                       'min': '0',
                       'max': '400'
                       }),
            'hall': forms.Select(attrs={'class': 'form-control'}),
            'movie': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):

        cleaned_data = super().clean()

        hall = cleaned_data.get('hall')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date < date.today():
            raise ValidationError('Start date cannot be less than today.')

        if end_date < start_date:
            raise ValidationError('End date should be greater than or equal to start date.')

        existing_sessions = Session.objects.filter(
            Q(hall=hall),
            Q(start_date__lte=start_date, end_date__gte=start_date) | Q(start_date__lte=end_date,
                                                                        end_date__gte=end_date) | Q(
                start_date__gte=start_date, end_date__lte=end_date),
            Q(start_time__lte=start_time, end_time__gte=start_time) | Q(start_time__lte=end_time,
                                                                        end_time__gte=end_time) | Q(
                start_time__gte=start_time, end_time__lte=end_time),
        )

        if existing_sessions.exists():
            session_id = self.instance.id if self.instance else None
            existing_sessions = existing_sessions.exclude(id=session_id)
            if existing_sessions.exists():
                raise ValidationError('This hall is already reserved at this time or date.')

        return cleaned_data
