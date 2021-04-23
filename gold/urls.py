from django.urls import path, include
from . import views


urlpatterns = [
    path('analysis', views.analysis, name='gold-analysis'),
    path('analysis/api', views.analysis_api, name='gold-analysis-api'),
    path('forecast', views.forecast, name='gold-forecast'),
    path('forecast/api', views.forecast_api, name='gold-forecast-api'),
]
