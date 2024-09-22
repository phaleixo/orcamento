from django.contrib import admin
from django.urls import path, include
from home.views import login 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),
    path('', login, name='login'),
]

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('login/', include('django.contrib.auth.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)