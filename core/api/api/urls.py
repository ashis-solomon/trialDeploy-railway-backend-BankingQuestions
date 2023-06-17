from django.urls import path
from api.api.views import CategoriesView, ModelPredictionView


urlpatterns = [
    path('', CategoriesView.as_view(), name='categories'),
    path('predict/', ModelPredictionView.as_view(), name='predict'),
]