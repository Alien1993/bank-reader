from django.conf.urls import url, include
from django.contrib import admin

apipatterns = [
    url(r'', include('api.urls')),
]

urlpatterns = [
    url(r'^api/', include(apipatterns, namespace='api')),
    url(r'^admin/', admin.site.urls),
]
