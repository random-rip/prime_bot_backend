from django.urls import path, include

urlpatterns = [
    path('settings/', include("app_api.modules.team_settings.urls"), ),
    path('status/', include("app_api.modules.status.urls"), ),
    path('', include("app_api.modules.urls"), ),
]
