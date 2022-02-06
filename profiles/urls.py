from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='profiles/index.html'), name='index'),
    # TODO
    # path('profiles', ProfileListView.as_view(), name='profiles'),
    # path('profiles/create', ProfileCreateView.as_view(), name='profile-create'),
    # path('profiles/<int:pk>/view', ProfileDetailView.as_view(), name='profile-detail-view'),
    # path('profiles/<int:pk>/update', ProfileUpdateView.as_view(), name='profile-update'),
    # path('profiles/<int:pk>/delete', ProfileDeleteView.as_view(), name='profile-delete'),
]
