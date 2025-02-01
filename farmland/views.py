from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Farmland
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response  # ✅ Import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from farmland.models import Farmland  # ✅ Import Farmland model
from django.contrib.auth.models import User  # ✅ Import User model


User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def create_farmland(request):
    """Saves farmland data"""
    data = request.data

    if "username" not in data or "crop_type" not in data or "land_area" not in data:
        return JsonResponse({"error": "All fields are required"}, status=400)

    try:
        user = User.objects.get(username=data["username"])  # Ensure user exists
    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist"}, status=404)

    Farmland.objects.create(
        user=user,
        crop_type=data["crop_type"],
        land_area=float(data["land_area"]),
    )

    return JsonResponse({"message": "Farmland saved successfully!"}, status=201)


@api_view(['GET'])
def get_user_farmland(request, username):
    """Fetch farmland details for a specific user"""
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist"}, status=404)

    try:
        farmland = Farmland.objects.get(user=user)
        return JsonResponse({
            "crop_type": farmland.crop_type,
            "land_area": farmland.land_area,
        }, status=200)
    except Farmland.DoesNotExist:
        return JsonResponse({"error": "Farmland details not found"}, status=404)

