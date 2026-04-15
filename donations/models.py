from django.db import models
from django.conf import settings
from projects.models import Project


class Donation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="donations",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="donations",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.project.refresh_progress()

    def delete(self, *args, **kwargs):
        project = self.project
        super().delete(*args, **kwargs)
        project.refresh_progress()

    def __str__(self):
        return f"{self.user} donated {self.amount} to {self.project}"