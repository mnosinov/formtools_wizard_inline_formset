from django.urls import path
from django.views.generic import TemplateView

from .views import ProfileListView, ProfileWizard

urlpatterns = [
    path('', TemplateView.as_view(template_name='profiles/index.html'), name='index'),
    path('profiles', ProfileListView.as_view(), name='profiles'),
    path('profiles/create', ProfileWizard.as_view(ProfileWizard.FORMS), name='profile-create-wizard'),
    # TODO
    # path('profiles/<int:pk>/view', ProfileDetailView.as_view(), name='profile-detail-view'),
    # path('profiles/<int:pk>/update', ProfileUpdateView.as_view(), name='profile-update'),
    # path('profiles/<int:pk>/delete', ProfileDeleteView.as_view(), name='profile-delete'),
]
