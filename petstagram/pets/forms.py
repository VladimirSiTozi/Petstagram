from django import forms
from petstagram.pets.models import Pet


class PetBaseForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'date_of_birth', 'personal_pet_photo']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Pet name'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'personal_pet_photo': forms.TextInput(attrs={'placeholder': 'Add pet photo url...'}),
        }

        labels = {
            'name': 'Pet name',
            'date_of_birth': 'Date of Birth',
            'personal_pet_photo': 'Link to Image',
        }


class PetAddForm(PetBaseForm):
    pass


class PetEditForm(PetBaseForm):
    pass


class PetDeleteForm(PetBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():  # ('name': object_field)
            field.widget.attrs['disabled'] = True
            field.widget.attrs['readonly'] = True
