from django.urls import include, path
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('menu.urls', namespace='menu')),
]

urlpatterns += staticfiles_urlpatterns()

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
]+urlpatterns
