
from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views


from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from utilisateurs.loginviews import *
from django.urls import reverse_lazy

urlpatterns = [
	path('accounts/password_change/',auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html')),
	#path('accounts/password_change/done/',auth_views.password_change_done,{'template_name':'registration/change-password-done.html'}),
	path('accounts/password_change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='registration/change-password-done.html'),{}),
	path('accounts/', include('django.contrib.auth.urls')),
	#path('logout/', auth_views.logout,{'next_page':'/accounts/login'},'logout' ),
	path('logout/', auth_views.LogoutView.as_view(next_page='/accueil'),{},'logout' ),
	path('admin/', admin.site.urls),
	path('communs/', include('communs.urls')),
	path('candidat/', include('candidat.urls')),
	path('pilote/', include('pilote.urls')),
	path('telecommande/', include('telecommande.urls')),
	path('structure/', include('structure.urls')),
	path('utilisateurs/', include('utilisateurs.urls')),
	path('formulaires/', include('formulaires.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

