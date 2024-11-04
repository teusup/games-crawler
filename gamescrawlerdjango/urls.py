from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from gamescrawlerweb.views import get_list, search, game_details, result

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', get_list),
    path('search/', search, name="search"),
    path('result/', result, name="result"),
    path('game_details/<str:primary_key>/', game_details, name="game_details")
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
