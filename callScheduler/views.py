from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta, date
from django.conf import settings
from dateutil.relativedelta import relativedelta # Import for calculating dates
from twilio.rest import Client  # Import Twilio client
from .models import FertilizerSchedule

# Define the crops and fertilizer schedules in a dictionary
CROP_SCHEDULES = {
    "Bitter Gourd": {
        "fertilizer_applications": [
            {"time": "Basal", "urea": 75, "tsp": 200, "mop": 60},
            {"time": "After 4 Weeks", "urea": 75, "tsp": None, "mop": 60},
            {"time": "After 8 Weeks", "urea": 75, "tsp": None, "mop": 60},
        ]
    },
    "Papaya": {
        "fertilizer_applications": [
            {"time": "Two days before planting", "urea": 60, "tsp": 40, "mop": 130},
            {"time": "every 3 days after 3 months", "urea": 9, "tsp": 0.5, "mop": None},
            {"time": "Every 3 days afterwards", "urea": 2.5, "tsp": 0.5, "mop": 5.0},
        ]
    },
    "Pineapple": {  # "Dry & Intermediate Zone Specification"
        "fertilizer_applications": [
            {"time": "Basal", "urea": None, "tsp": None, "mop": None},
            {"time": "1 MAP", "urea": 10, "tsp": 7, "mop": 15},
            {"time": "After 3-4 M", "urea": 10, "tsp": 7, "mop": 5},
        ]
    },
    "Brinjal": {
        "fertilizer_applications": [
            {"time": "Basal", "urea": 75, "tsp": 395, "mop": 85},
            {"time": "After 4 Weeks", "urea": 75, "tsp": None, "mop": None},
            {"time": "After 8 Weeks", "urea": 75, "tsp": None, "mop": None},
        ]
    },
    "Ladies Fingers": {
        "fertilizer_applications": [
            {"time": "Basal (2-3 days before planting)", "urea": 50, "tsp": 195, "mop": 25},
            {"time": "2 weeks later", "urea": 50, "tsp": None, "mop": 25},
            {"time": "5 weeks later", "urea": 100, "tsp": None, "mop": 50},
            {"time": "8 weeks later", "urea": 100, "tsp": None, "mop": 50},
        ]
    },
    "Long Beans": {
        "fertilizer_applications": [
            {"time": "Basal (3 days before)", "urea": 35, "tsp": 130, "mop": 35},
            {"time": "After a month", "urea": 55, "tsp": None, "mop": 35},
        ]
    },
    "Snake Gourd": {
        "fertilizer_applications": [
            {"time": "Basal (2-3 before opening)", "urea": 75, "tsp": 200, "mop": 60},
            {"time": "4 weeks after", "urea": 75, "tsp": None, "mop": 60},
            {"time": "8 weeks after", "urea": 75, "tsp": None, "mop": 60},
        ]
    },
}

# Twilio Account Information (Replace with your actual credentials)
TWILIO_ACCOUNT_SID = "ACe9083eb05f973a4b39765c402fc08248"  # Replace with your Account SID
TWILIO_AUTH_TOKEN = "9df028d2478f5c679ec6997a0b1b1516"  # Replace with your Auth Token
TWILIO_PHONE_NUMBER = "+15419408863"  # Replace with your Twilio phone number

reminders = []

def get_user_phone_number(user_id):  # Replace with database lookup
    return "+94767627455" # Replace with your actual phone number for testing
def send_sms(to_phone_number, message):
    """Sends an SMS message using Twilio."""
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            to=to_phone_number,
            from_=TWILIO_PHONE_NUMBER,
            body=message
        )
        print(f"SMS sent to {to_phone_number}. SID: {message.sid}")  # Log the message SID
        return True
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return False
    
def emulate_call(phone_number, crop_type, fertilizer_type, application_date):  # Include crop
    print(f"Emulated Call to {phone_number}: Fertilizer reminder for {fertilizer_type} for {crop_type} on {application_date}.")


# @csrf_exempt
# def receive_schedule(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            crop_type = data.get('cropType')

            if crop_type in CROP_SCHEDULES:
                applications = CROP_SCHEDULES[crop_type]['fertilizer_applications']

                for application in applications:
                    try:
                        time_description = application['time']
                        fertilizer_types = []
                        if application.get('urea') is not None:
                            fertilizer_types.append(f"Urea ({application['urea']} kg/ha)")
                        if application.get('tsp') is not None:
                            fertilizer_types.append(f"TSP ({application['tsp']} kg/ha)")
                        if application.get('mop') is not None:
                            fertilizer_types.append(f"MOP ({application['mop']} kg/ha)")

                        fertilizer_type_str = ", ".join(fertilizer_types)

                        # Calculate the reminder date based on the 'time' description.
                        if "planting" in time_description.lower():
                            days_before = 2 if "before planting" in time_description.lower() else 3 #default to 2 days before planting
                            application_date = date.today() # Assume planting today, for testing purposes.  Replace this with actual planting date input from user.
                            reminder_date = application_date - timedelta(days=days_before)  # Reminder 2 days before planting
                        elif "days before" in time_description.lower(): # Handling "X days before"
                            days_before = int(time_description.split("days before")[0].strip() or 3)  #Get the numner of days from the string
                            application_date = date.today() # planting date here
                            reminder_date = application_date - timedelta(days=days_before)
                        elif "week" in time_description.lower():
                            weeks_after = int(time_description.split("week")[0].replace("After", "").strip()) # Extract number of weeks
                            application_date = date.today() + relativedelta(weeks=weeks_after) # date of application
                            reminder_date = application_date - timedelta(days=2) # 2 days before
                        elif "month" in time_description.lower():
                            months_after = int(time_description.split("month")[0].replace("After", "").strip())
                            application_date = date.today() + relativedelta(months=months_after)
                            reminder_date = application_date - timedelta(days=2)
                        elif "map" in time_description.lower():
                            # Specific to PineApple.
                            application_date = date.today() + relativedelta(months=1)
                            if "3-4" in time_description.lower():
                                application_date = date.today() + relativedelta(months=3) # take 3 months as an assumption here, adjust it as needed.
                            reminder_date = application_date - timedelta(days=2)
                        else:
                            # Handle other time descriptions or set a default.  For example, if the "time" field is
                            # just "Basal",  you might have a default date or not set a reminder at all.  Or,
                            # you might prompt the user to enter a planting date.
                            print(f"Warning: Unhandled time description: {time_description} for {crop_type}")
                            continue  # Skip this schedule entry


                        if reminder_date >= date.today(): #Check if reminder is in the future
                            reminders.append({
                                'reminder_date': reminder_date,
                                'fertilizer_type': fertilizer_type_str,
                                'application_date': application_date,
                                'crop_type': crop_type,
                            })
                        else:
                            print(f"Skipping reminder for {time_description} because it has passed.")

                    except (ValueError, TypeError) as e:
                        print(f"Error processing application: {application}.  Error: {e}")
                        # Log the error, skip this application, or handle it as appropriate
                        continue # Skip this application and go to the next.

                return JsonResponse({'status': 'success', 'message': 'Schedule received and reminders set.'}, status=201)
            else:
                return JsonResponse({'status': 'error', 'message': 'Crop not found'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def receive_schedule(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            crop_type = data.get('cropType')
            application_date = data.get('applicationDate')  # Receiving date

            if not crop_type or not application_date:
                return JsonResponse({'message': 'Missing crop type or date'}, status=400)

            # Save to database
            schedule = FertilizerSchedule.objects.create(
                crop_type=crop_type,
                application_date=application_date
            )

            return JsonResponse({'message': 'Schedule saved successfully!'}, status=201)

        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON data
            crop_type = data.get("cropType")

            if not crop_type:
                return JsonResponse({"message": "Missing crop type"}, status=400)

            # Create and save the schedule
            new_schedule = FertilizerSchedule.objects.create(
                crop_type=crop_type,
                fertilizer_type="Unknown",
                application_date="2025-02-22",  # Set a test date
                sms_sent=False
            )
            new_schedule.save()

            print("Schedule saved successfully:", new_schedule)

            return JsonResponse({"message": "Schedule saved successfully!"})

        except Exception as e:
            print("Error saving schedule:", str(e))
            return JsonResponse({"message": "Internal Server Error"}, status=500)


#  The 'check_reminders' function
def check_reminders():
    """Checks if any reminders are due and triggers the emulated call."""
    now = date.today()
    for reminder in reminders:
        if reminder['reminder_date'] == now:  #Correct Comparison: date object
            phone_number = get_user_phone_number(1) # Assuming user ID 1 (for testing)
            emulate_call(phone_number, reminder['crop_type'], reminder['fertilizer_type'], reminder['application_date'])  #Pass crop_type
            reminders.remove(reminder)

@csrf_exempt
def get_schedule_history(request):
    history = list(FertilizerSchedule.objects.all().values())  # Fetch all data
    print("Fetched History from DB:", history)  # Debugging log
    return JsonResponse({"history": history})