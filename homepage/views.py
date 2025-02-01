from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from farmland.models import Farmland
from django.contrib.auth import get_user_model
from .serializers import FarmlandSerializer

User = get_user_model()

@api_view(['GET'])
@permission_classes([AllowAny])  # Allow unauthenticated access if needed
def get_user_farmland(request, username):
    """Fetch farmland details for a specific user."""
    try:
        user = User.objects.get(username=username)  # Ensure user exists
        farmland = Farmland.objects.filter(user=user).first()

        if not farmland:
            return JsonResponse({"error": "No farmland details found for this user"}, status=404)

        # Serialize farmland data
        serializer = FarmlandSerializer(farmland)
        return JsonResponse(serializer.data, status=200)

    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist"}, status=404)


