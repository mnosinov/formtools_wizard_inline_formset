from django import forms

from .models import Profile, Workplace, Certificate, Position


# wizard forms - for Profile ----------------------------------BEGIN

# SOLUTION BASED ON forms.Form and formset_factory------------

# # step1
# class ProfileForm1(forms.Form):
#     name = forms.CharField(
#         max_length=50, label='Name of Person',
#         widget=forms.TextInput(attrs={'class': "form-control"})
#     )
#     dob = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
# 
# 
# # step2
# class CertificateForm(forms.Form):
#     title = forms.CharField(max_length=50)
# 
# 
# CertificateFormSet = forms.formset_factory(CertificateForm, extra=1)
# 
# # step3
# class ProfileForm3(forms.Form):
#     pass


# SOLUTION BASED ON forms.ModelForm and modelformset_factory------------
# step1
class ProfileForm1(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'dob')
        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': 'Enter Employee name'}
            ),
            'dob': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'type': 'date',
                    'class': 'myDateClass',
                }
            ),
        }


# step2
# class ProfileForm2(forms.ModelForm):
#     class Meta:
#         model = Certificate
#         fields = ('title',)


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['title', ]


CertificateFormSet = forms.modelformset_factory(
    Certificate,
    form=CertificateForm,
    extra=1
)


# step3
class ProfileForm3(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'dob')

# wizard forms - for Profile ----------------------------------END
