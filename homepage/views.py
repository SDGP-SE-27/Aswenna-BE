from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from farmland.models import Farmland
from django.contrib.auth import get_user_model
from .serializers import FarmlandSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password

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
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure only logged-in users can access their details
def get_user_details(request):
    """Fetch the logged-in user's details."""
    user = request.user
    data = {
        "username": user.username,
        "email": user.email,
        "phone_number": getattr(user, "phone_number", "Not set"),  # Ensure phone number exists
    }
    return Response(data, status=200)



@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Only allow logged-in users to reset passwords
def reset_password(request):
    """Allow the logged-in user to reset their password"""
    user = request.user
    new_password = request.data.get("new_password")

    if not new_password or len(new_password) < 6:
        return Response({"error": "Password must be at least 6 characters long."}, status=400)

    try:
        # Update the user's password
        user.password = make_password(new_password)
        user.save()
        return Response({"message": "Password reset successfully!"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)




