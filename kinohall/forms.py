""" Create Kinohall form """

from django import forms

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

