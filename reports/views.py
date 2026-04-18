from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Report
from .serializers import ReportSerializer, ReasonChoicesSerializer


class ReportCreateView(generics.CreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        project = serializer.validated_data.get('project')
        comment = serializer.validated_data.get('comment')

        already_reported = Report.objects.filter(
            user=user,
            project=project,
            comment=comment
        ).exists()

        if already_reported:
            raise ValidationError("You have already reported this")

        serializer.save(user=user)


class ReasonChoicesView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ReasonChoicesSerializer

    def get(self, request, *args, **kwargs):
        """Return available reason choices for reports"""
        choices = [
            {'value': choice[0], 'label': choice[1]}
            for choice in Report.REASON_CHOICES
        ]
        serializer = self.get_serializer(choices, many=True)
        return Response(serializer.data)