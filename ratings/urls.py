from django.urls import path
from .views import RatingCreateView, RatingListView, RatingStatsView

urlpatterns = [
    path('project/<int:project_id>/', RatingStatsView.as_view(), name='project-rating-stats'),
    path('create/', RatingCreateView.as_view(), name='create-rating'),
]
