import os
from django.conf import settings
from django.views.generic import ListView
from django.core.files.storage import FileSystemStorage
from django.forms.models import model_to_dict
from django.contrib import messages
from django.shortcuts import redirect
from formtools.wizard.views import SessionWizardView

from .models import Profile, Workplace, Certificate, Position
from . import forms


class ProfileListView(ListView):
    model = Profile


# multistep wizard form for profile -----------------------------------BEGIN
class ProfileWizard(SessionWizardView):
    # forms
    FORMS = [
        ("form1", forms.ProfileForm1),
        ("form2", forms.ProfileForm2),
        ("form3", forms.ProfileForm3),
    ]
    # form templates
    TEMPLATES = {
        "form1": "profiles/profile_wizard/step1.html",
        "form2": "profiles/profile_wizard/step2.html",
        "form3": "profiles/profile_wizard/step3.html",
    }
    file_storage = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, 'profile_photos')
    )

    def get_template_names(self):
        return [ProfileWizard.TEMPLATES[self.steps.current]]

    def get_form_initial(self, step):
        if 'pk' in self.kwargs:
            profile_id = self.kwargs['pk']
            profile = Profile.objects.get(pk=profile_id)
            return model_to_dict(profile)
        else:
            return self.initial_dict.get(step, {})

    def done(self, form_list, form_dict, **kwargs):
        # save data from all of the steps
        profile = Profile(
            name=form_dict['form1'].cleaned_data['name'],
            dob=form_dict['form1'].cleaned_data['dob'],
        )
        # if pk exists then it is UPDATE mode
        if 'pk' in self.kwargs:
            profile.id = self.kwargs['pk']

        profile.save()

        # certificates set
        certificate_forms = form_dict['form2'].cleaned_data['certificates']

        for certificate_form in certificate_forms:
            cert = Certificate(
                profile=profile,
                title=certificate_form.form_dict['form2'].cleaned_data['title'],
            )
            cert.save()

        # workplaces set
        workplace_forms = form_dict['form2'].cleaned_data['certificates']
        for workplace_form in workplace_forms:
            workplace = Workplace(
                profile=profile,
                name=workplace_form.form_dict['form3'].cleaned_data['name'],
                address=workplace_form.form_dict['form3'].
                    cleaned_data['address'],
            )
            workplace.save()
            position_forms = form_dict['form3'].cleaned_data['positions']
            for position_form in position_forms:
                position = Position(
                    workplace=workplace,
                    title=position_form.form_dict['form3'].cleaned_data['title'],
                )
                position.save()

        profile.save()
        success_message = 'Profile successfully saved.'

        messages.success(self.request, success_message)
        return redirect('profiles')
# multistep wizard form for profile -----------------------------------END
