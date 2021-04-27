from django.urls import path, include
from . import views


urlpatterns = [
    path('analysis', views.analysis, name='gas-analysis'),
    path('analysis/api', views.analysis_api, name='gas-analysis-api'),
    path('forecast', views.forecast, name='gas-forecast'),
    path('forecast/api', views.forecast_api, name='gas-forecast-api'),
]
