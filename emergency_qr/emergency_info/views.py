from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import EmergencyInfo

def register_user(request):
    """Register a new person & generate their QR code."""
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        age = request.POST.get("age")
        blood_group = request.POST.get("blood_group")
        address = request.POST.get("address")
        emergency_contact = request.POST.get("emergency_contact")
        medical_conditions = request.POST.get("medical_conditions", "")

        # Check if email already exists
        if EmergencyInfo.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already registered."}, status=400)

        user = EmergencyInfo(
            name=name,
            email=email,
            age=age,
            blood_group=blood_group,
            address=address,
            emergency_contact=emergency_contact,
            medical_conditions=medical_conditions,
        )
        user.save()

        return JsonResponse({
            "message": "User registered successfully! QR code has been emailed.",
            "qr_code": user.qr_code.url
        })

    return render(request, "register.html")

def emergency_info(request, user_id):
    """Display the emergency details when the QR code is scanned."""
    user = get_object_or_404(EmergencyInfo, user_id=user_id)
    return render(request, "emergency_info.html", {"user": user})
