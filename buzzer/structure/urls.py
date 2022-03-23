from django.urls import path, include
from django.conf import settings
from django.contrib.auth.decorators import login_required

from . import views
from . import wsviews


urlpatterns = [
    path('liste/racine', login_required(views.ListeRacine.as_view()), {}, 'listeracine'),
    path('ajout/element/<int:indicehierarchie>/<str:id_racine>', login_required(views.AjoutElement.as_view()), {}, 'ajout_element'),
    path('modif/element/<str:pk>', login_required(views.ModifElement.as_view()), {}, 'modif_element'),
    path('suppr/element/<str:pk>', login_required(views.SupprElement.as_view()), {}, 'suppr_element'),

    path('gamme/<int:id_moyen>', login_required(views.GammeList.as_view()), {}, 'listegamme'),
    path('gamme/ajout/<int:id_moyen>', login_required(views.AjoutGamme), {}, 'ajout_gamme'),
    path('gamme/suppr/<int:pk>', login_required(views.SupprGamme.as_view()), {}, 'suppr_gamme'),

    path('user/ajout/<str:type_user>/<str:element_structure>', login_required(views.AjoutUser), {}, 'ajout_user'),
    path('user/confirm/ajout/<str:type_user>/<str:element_structure>/<str:identifiant>', login_required(views.AjoutUserConfirm), {}, 'ajout_user_confirm'),
    path('user/confirm/retrait/<str:type_user>/<str:element_structure>/<str:identifiant>', login_required(views.RetraitUserConfirm), {}, 'retrait_user_confirm'),
    path('ajout-organisation/<int:id_struct>', login_required(views.AjoutOrganisation.as_view()), {}, 'ajout_organisation'),
]
