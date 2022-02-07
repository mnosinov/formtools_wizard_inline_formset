import os
from django.conf import settings
from django.views.generic import ListView
from django.core.files.storage import FileSystemStorage
from django.forms.models import model_to_dict
from django.contrib import messages
from django.shortcuts import redirect
from formtools.wizard.views import SessionWizardView
from django.forms import modelformset_factory

from .models import Profile, Workplace, Certificate, Position
from . import forms


class ProfileListView(ListView):
    model = Profile


# multistep wizard form for profile -----------------------------------BEGIN
class ProfileWizard(SessionWizardView):
    # forms
    FORMS = [
        ("step1", forms.ProfileForm1),
        ("step2", forms.CertificateFormSet),
        ("step3", forms.ProfileForm3),
    ]
    # form templates
    TEMPLATES = {
        "step1": "profiles/profile_wizard/step1.html",
        "step2": "profiles/profile_wizard/step2.html",
        "step3": "profiles/profile_wizard/step3.html",
    }
    file_storage = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, 'profile_photos')
    )

    def get_template_names(self):
        return [ProfileWizard.TEMPLATES[self.steps.current]]

    def get_form(self, step=None, data=None, files=None):
        form = super(ProfileWizard, self).get_form(step, data, files)

        if step is None:
            step = self.steps.current

        if step == 'step2':
            # CertificateFormSet = modelformset_factory(
            #     Certificate,
            #     form=forms.CertificateForm,
            #     extra=1
            # )
            # form = forms.CertificateFormSet(self.request.POST)
            form = forms.CertificateFormSet()

        print('--3')

        return form

    def get_form_initial(self, step):
        if 'pk' in self.kwargs:
            profile_id = self.kwargs['pk']
            profile = Profile.objects.get(pk=profile_id)
            return model_to_dict(profile)
        else:
            if step == 'step2':
                print('--0')
                pass
            print('--1')
            return self.initial_dict.get(step, {})

    def get_form_instance(self, step):
        if 'pk' in self.kwargs:
            pass
        else:
            if step == 'step2':
                print('--2')
                # return Certificate(self.request.POST)
                return Certificate()
        print('--4')
        return self.instance_dict.get(step, None)

    # def post(self, *args, **kwargs):
        # import pdb; pdb.set_trace()
        # print('---6')
        # go_to_step = self.request.POST.get('wizard_goto_step', None)  # get the step name
        # form = self.get_form(data=self.request.POST)
        # if form.forms:
        #     print('---hello formset')
        # current_index = self.get_step_index(self.steps.current)
        # goto_index = self.get_step_index(go_to_step)

        # print('---current_index', current_index)
        # print('--- goto_index',  goto_index)
        # # import pdb; pdb.set_trace()
        # if current_index > goto_index:
        #     print('---7')
        #     import pdb; pdb.set_trace()
        #     if form.is_valid():
        #         print('---8')
        #         self.storage.set_step_data(self.steps.current, self.process_step(form))

        # print('---9')
        # result = super(ProfileWizard, self).post(*args, **kwargs)
        # print(result)
        # return result

    def done(self, form_list, form_dict, **kwargs):
        print('---5')
        for form in form_list:
            if form.is_valid():
                import pdb; pdb.set_trace()
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
