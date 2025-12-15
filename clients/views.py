from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from datetime import date, timedelta
import json

from .models import Client

# SIMPLE ADMIN LOGIN (same as Flask)
ADMIN_ID = "admin"
ADMIN_PASSWORD = "admin123"


def login_view(request):
    if request.method == "POST":
        if (
            request.POST.get("username") == ADMIN_ID
            and request.POST.get("password") == ADMIN_PASSWORD
        ):
            request.session["logged_in"] = True
            return redirect("dashboard")
        messages.error(request, "Invalid credentials")
    return render(request, "login.html")


def logout_view(request):
    request.session.flush()
    return redirect("login")


def dashboard(request):
    if not request.session.get("logged_in"):
        return redirect("login")

    clients = Client.objects.all()
    today = date.today()

    for c in clients:
        c.days_left = max((c.expiry_date - today).days, 0)

    return render(request, "dashboard.html", {"clients": clients})


def add_client(request):
    if not request.session.get("logged_in"):
        return redirect("login")

    if request.method == "POST":
        days = int(request.POST["membership_days"])
        today = date.today()

        Client.objects.create(
            name=request.POST["name"],
            email=request.POST["email"],
            phone="+91" + request.POST["phone"],
            join_date=today,
            expiry_date=today + timedelta(days=days),
            membership_days=days,
        )

        messages.success(request, "Client added successfully")
        return redirect("dashboard")

    return render(request, "add_client.html")


@csrf_exempt
def renew_membership(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            client = Client.objects.get(id=data["member_id"])
            client.expiry_date = data["new_expiry"]
            client.save()
            return JsonResponse({"success": True})
        except Client.DoesNotExist:
            return JsonResponse(
                {"success": False, "message": "Client not found"}, status=404
            )


@csrf_exempt
def remove_client(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            Client.objects.get(id=data["client_id"]).delete()
            return JsonResponse({"success": True})
        except Client.DoesNotExist:
            return JsonResponse({"success": False}, status=404)
