from django.urls import path
from django.views.generic import TemplateView

from menenger.apps import MenengerConfig
from menenger.views import HomeView, ContentCreateView, ContentUpdateView, ContentDetailView, ContentDeleteView, \
    payment_stripe, like_view, NoPublishView, search_view

app_name = MenengerConfig.name

urlpatterns = [
    path('create/', ContentCreateView.as_view(), name='content_create'),
    path('', HomeView.as_view(), name='home'),
    path('nopublish/', NoPublishView.as_view(), name='nopublish'),
    path('update/<int:pk>/', ContentUpdateView.as_view(), name='update'),
    path('detail/<int:pk>/', ContentDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', ContentDeleteView.as_view(), name='delete'),
    path('subcribt/', payment_stripe, name='subscribe'),
    path('success/', TemplateView.as_view(template_name='menenger/success.html'), name='success'),
    path('cancel/', TemplateView.as_view(template_name='menenger/cancel.html'), name='cancel'),
    path('home/<int:pk>/<int:page>/like/', like_view, name='like_view'),
    path('search/', search_view, name='search'),
]
