from django.urls import path
from .views import MadrashaCheckView, ValidateSignupTokenView

urlpatterns = [
    path('check/', MadrashaCheckView.as_view(), name='madrasha-check'),
    path('validate-signup-token/', ValidateSignupTokenView.as_view(), name='validate-signup-token'),
]
