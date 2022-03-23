from django.urls import path, include
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('liste/', staff_member_required(views.Liste), {}, 'liste'),
    path('ajout/', staff_member_required(views.Ajout.as_view()), {}, 'ajout'),
    path('modif/<str:pk>', staff_member_required(views.Modif.as_view()), {}, 'modif'),
    path('suppr/<str:pk>', staff_member_required(views.Suppr.as_view()), {}, 'suppr'),
    path('reset-mdp/<str:username>', staff_member_required(views.ResetMdp), {}, 'reset_mdp'),
    path('utilisateurs-connectes', login_required(views.UtilisateursConnectes.as_view()), {}, 'utilisateurs_connectes'),


    path('groupe/liste/<str:groupe>', views.GroupeListe.as_view(), {}, 'groupe_liste'),
    path('suppr/groupe/<str:pk>/<str:groupe>', views.UserSupprGroupe.as_view(), {}, 'user_suppr_groupe'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

   