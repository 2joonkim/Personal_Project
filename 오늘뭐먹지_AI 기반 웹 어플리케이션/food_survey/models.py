from django.db import models


class UserResponse(models.Model):
    session_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    people_count = models.CharField(max_length=20, null=True, blank=True)
    hunger_level = models.CharField(max_length=50, null=True, blank=True)
    food_type = models.CharField(max_length=20, null=True, blank=True)

    spicy_level = models.IntegerField(null=True, blank=True)
    oil_level = models.IntegerField(null=True, blank=True)
    texture_level = models.IntegerField(null=True, blank=True)
    taste_level = models.IntegerField(null=True, blank=True)
    no_preference = models.BooleanField(default=False)

    def __str__(self):
        return f"Response {self.session_id} at {self.created_at}"