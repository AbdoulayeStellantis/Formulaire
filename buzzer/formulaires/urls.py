from django.urls import path, include
from django.conf import settings
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [
    path('get-dept', login_required(views.get_departement), {}, 'get_departement'),
]


