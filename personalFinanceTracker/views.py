
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from datetime import datetime
# from .models import Expense, Income
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from .models import Expense
# from .serializers import ExpenseSerializer


# @csrf_exempt
# def add_expense(request):
#     if request.method == "POST":
#         try:
#             # Parse the JSON data from the request body
#             data = json.loads(request.body)
#             date_str = data.get("date")
#             expense_type = data.get("expense_type")
#             amount = data.get("amount")
#             description = data.get("description")

#             # Add your logic to save the expense to the database
#             # Example: Create a new expense object in the database
#             from .models import Expense  # Import your model
#             expense = Expense.objects.create (
#                 date = date_str,
#                 expense_type=expense_type,
#                 amount=amount,
#                 description=description,
#             )

#             if not expense_type or not amount or not date_str: 
#                 return JsonResponse({"error": "Expense type and amount are required "}, status = 400)

#             # Respond with success
#             return JsonResponse({"message": "Expense added successfully", "id": expense.id}, status=201)
#         except Exception as e:
#             # Return an error response if something goes wrong
#             return JsonResponse({"error": str(e)}, status=400)

#     # If the request is not POST, return a method not allowed error
#     return JsonResponse({"error": "Invalid HTTP method"}, status=405)

#     import logging
#     logger = logging.getLogger(__name__)
#     logger.info(request.body)  # Log the raw payload



# @csrf_exempt
# def add_income(request):
#     if request.method == "POST":
#         try:
#             # Parse the JSON data from the request body
#             data = json.loads(request.body)
#             date_str = data.get("date")
#             income_type = data.get("income_type")
#             amount = data.get("amount")
#             description = data.get("description")

#             # Add your logic to save the expense to the database
#             # Example: Create a new expense object in the database
#             from .models import Income  # Import your model
#             income = Income.objects.create (
#                 date = date_str,
#                 income_type=income_type,
#                 amount=amount,
#                 description=description,
#             )

#             if not income_type or not amount or not date_str: 
#                 return JsonResponse({"error": "Expense type and amount are required "}, status = 400)

#             # Respond with success
#             return JsonResponse({"message": "Expense added successfully", "id": income.id}, status=201)
#         except Exception as e:
#             # Return an error response if something goes wrong
#             return JsonResponse({"error": str(e)}, status=400)

#     # If the request is not POST, return a method not allowed error
#     return JsonResponse({"error": "Invalid HTTP method"}, status=405)



# def transaction_history(request):
#     if request.method == "GET":
#         # Fetch all expense and income entries
#         expenses = list(Expense.objects.all().values())
#         incomes = list(Income.objects.all().values())
        
#         # Combine and sort by date
#         transactions = sorted(expenses + incomes, key=lambda x: x['date'], reverse=True)

#         return JsonResponse({"transactions": transactions}, safe=False)
#     else:
#         return JsonResponse({"error": "GET request required"}, status=400)
    

    
# class ExpenseListView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         expenses = Expense.objects.filter(user=request.user)
#         serializer = ExpenseSerializer(expenses, many=True)
#         return Response(serializer.data)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Expense, Income
from .serializers import ExpenseSerializer
import json
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_expense(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            date_str = data.get("date")
            expense_type = data.get("expense_type")
            amount = data.get("amount")
            description = data.get("description")

            if not expense_type or not amount or not date_str:
                return JsonResponse(
                    {"error": "Expense type, amount, and date are required"}, status=400
                )

            # Parse date
            date = datetime.strptime(date_str, "%Y-%m-%d").date()

            # Save expense
            expense = Expense.objects.create(
                user=request.user,
                date=date,
                expense_type=expense_type,
                amount=amount,
                description=description,
            )

            return JsonResponse({"message": "Expense added successfully", "id": expense.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid HTTP method"}, status=405)


 # Check if the user is authenticated


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_income(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            date_str = data.get("date")
            income_type = data.get("income_type")
            amount = data.get("amount")
            description = data.get("description")

            if not income_type or not amount or not date_str:
                return JsonResponse(
                    {"error": "Income type, amount, and date are required"}, status=400
                )

            # Parse date
            date = datetime.strptime(date_str, "%Y-%m-%d").date()

            # Save income
            income = Income.objects.create(
                user=request.user,
                date=date,
                income_type=income_type,
                amount=amount,
                description=description,
            )

            return JsonResponse({"message": "Income added successfully", "id": income.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid HTTP method"}, status=405)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_history(request):
    if request.method == "GET":
        expenses = list(
            Expense.objects.filter(user=request.user).values(
                "id", "expense_type", "amount", "description", "date"
            )
        )
        incomes = list(
            Income.objects.filter(user=request.user).values(
                "id", "income_type", "amount", "description", "date"
            )
        )

        transactions = sorted(expenses + incomes, key=lambda x: x["date"], reverse=True)
        return JsonResponse({"transactions": transactions}, safe=False)
    return JsonResponse({"error": "GET request required"}, status=400)



class ExpenseListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        expenses = Expense.objects.filter(user=request.user)
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)
