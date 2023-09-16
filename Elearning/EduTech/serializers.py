from rest_framework import routers, serializers

from .models import *

# Serializers define the API representation.
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signup
        fields = '__all__'
        # fields = ['url', 'username', 'email', 'is_staff']