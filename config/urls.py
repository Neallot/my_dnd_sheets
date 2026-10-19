from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    # Встроенные вьюхи Django для логина/логаута (шаблоны в templates/registration/)
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('characters.urls')),
    path('', RedirectView.as_view(pattern_name='character-list', permanent=False)),
]
