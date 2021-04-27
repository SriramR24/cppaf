from django.urls import path, include
from . import views


urlpatterns = [
    path('analysis', views.analysis, name='oil-analysis'),
    path('analysis/api', views.analysis_api, name='oil-analysis-api'),
    path('forecast', views.forecast, name='oil-forecast'),
    path('forecast/api', views.forecast_api, name='oil-forecast-api'),
]
