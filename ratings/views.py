from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.db.models import Avg, Count
from .models import Rating
from .serializers import RatingSerializer

class RatingCreateView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        if project.owner == self.request.user:
            raise PermissionDenied("You can't rate your own project")
        serializer.save(user=self.request.user)


class RatingListView(generics.ListAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Rating.objects.filter(project_id=project_id)


class RatingStatsView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']
        stats = Rating.objects.filter(project_id=project_id).aggregate(
            avg_rating=Avg('value'),
            count=Count('id')
        )
        return Response({
            'avg_rating': stats['avg_rating'] or 0,
            'count': stats['count'] or 0
        })