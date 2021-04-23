from django.urls import path, include
from . import views


urlpatterns = [
    path('analysis', views.analysis, name='silver-analysis'),
    path('analysis/api', views.analysis_api, name='silver-analysis-api'),
    path('forecast', views.forecast, name='silver-forecast'),
    path('forecast/api', views.forecast_api, name='silver-forecast-api'),
]
