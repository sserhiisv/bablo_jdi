from rest_framework import serializers
from webapp.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('android_id', 'profile_data')
