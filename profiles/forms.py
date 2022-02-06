from django import forms


# wizard forms - for Profile ----------------------------------BEGIN
# step1
class ProfileForm1(forms.Form):
    name = forms.CharField(
        max_length=50, label='Name of Person',
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    dob = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))


# step2
class ProfileForm2(forms.Form):
    pass


# step3
class ProfileForm3(forms.Form):
    pass

# wizard forms - for Profile ----------------------------------END
