from django.contrib import admin
from django.urls import path, include  # include is new

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('monitor.urls')),  # send root URL to monitor app
]
