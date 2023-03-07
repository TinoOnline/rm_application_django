from django import forms


class UserForm(forms.Form):
    name = forms.EmailField(label="Enter Name")
    surname = forms.EmailField(label="Enter Email")
    email = forms.EmailField(label="Enter Email")
    file = forms.FileField()  # for creating file input


class DocumentForm(forms.Form):
    # for creating file input
    file = forms.FileField(allow_empty_file=False, required=True)
