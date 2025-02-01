from rest_framework import serializers
from farmland.models import Farmland

class FarmlandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmland
        fields = ['crop_type', 'land_area']  # ✅ Include only needed fields
