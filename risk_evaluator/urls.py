# risk_evaluator/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.evaluate_risk, name='evaluate_risk'),
]
