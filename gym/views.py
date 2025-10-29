from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .form import UserRegistrationForm, ProductForm
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from datetime import datetime
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
import calendar

def log(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {username}!")
                if user.is_staff:
                    return redirect('/admin/') 
                return redirect('Home')  
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def index(request):
    return redirect('log')
@login_required
def Home(request):
    template = loader.get_template("Home.html")
    context = {}
    return HttpResponse(template.render(context, request))

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()
            return redirect('log')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').capitalize()}: {error}")
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def payment(request):
    return render(request, "three month.html", {})

@login_required
def render_three_month_payment_view(request):
    if request.method == "POST":
        try:
            input_fee = int(request.POST.get("Fee", 0))
            input_actualfee = int(request.POST.get("Actualfee", 0))
            input_datetime_str = request.POST.get("Datetime", "")
            input_pendingfee = 0
            if input_actualfee < input_fee:
                input_pendingfee = input_fee - input_actualfee
            obj = fee()
            obj.user = request.user
            obj.Fee = input_fee
            obj.Actualfee = input_actualfee
            obj.Pendingfee = input_pendingfee
            obj.Datetime = input_datetime_str
            obj.save()
            messages.success(request, "Payment recorded successfully!")
            return redirect('render_three_month_payment_view')
        except (ValueError, TypeError) as e:
            messages.error(request, f"Invalid input. Please enter valid numbers. Error: {e}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")
    all_data = fee.objects.all().order_by('-Datetime')
    if not request.user.is_superuser:
        all_data = all_data.filter(user=request.user)
    context = {
        "datas": all_data,
        "current_datetime": datetime.now(),
    }
    return render(request, "paymentview.html", context)

@login_required
def updatethree(request, id):
    instance = get_object_or_404(fee, id=id)
    if not request.user.is_superuser and instance.user != request.user:
        messages.error(request, "You are not authorized to update this record.")
        return redirect('render_three_month_payment_view')
    if request.method == "POST":
        try:
            input_actualfee = int(request.POST.get("Actualfee", 0))
            input_datetime_str = request.POST.get("Datetime", "")
            old_pendingfee = instance.Pendingfee
            if input_actualfee == old_pendingfee:
                new_pendingfee = 0
            elif input_actualfee < old_pendingfee:
                new_pendingfee = old_pendingfee - input_actualfee
            else:
                messages.error(request, "Paid amount cannot exceed pending amount.")
                return redirect(request.path)
            instance.Actualfee += input_actualfee
            instance.Pendingfee = new_pendingfee
            instance.Datetime = input_datetime_str
            instance.save()
            messages.success(request, "Payment updated successfully!")
            return redirect('render_three_month_payment_view')
        except (ValueError, TypeError) as e:
            messages.error(request, f"Invalid input: {e}")
        except Exception as e:
            messages.error(request, f"Unexpected error occurred: {e}")
    context = {
        "instance": instance
    }
    return render(request, "updatethree.html", context)

@login_required
def render_six_month_payment_view(request):
    if request.method == "POST":
        try:
            input_fee = int(request.POST.get("Fee", 0))
            input_actualfee = int(request.POST.get("Actualfee", 0))
            input_datetime_str = request.POST.get("Datetime", "")
            input_pendingfee = 0
            if input_actualfee < input_fee:
                input_pendingfee = input_fee - input_actualfee
            obj = fee()
            obj.user = request.user
            obj.Fee = input_fee
            obj.Actualfee = input_actualfee
            obj.Pendingfee = input_pendingfee
            obj.Datetime = input_datetime_str
            obj.save()
            messages.success(request, "Payment recorded successfully!")
            return redirect(request.path)
        except (ValueError, TypeError) as e:
            messages.error(request, f"Invalid input. Please enter valid numbers. Error: {e}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")
    all_data = fee.objects.all().order_by('-Datetime')
    if not request.user.is_superuser:
        all_data = all_data.filter(user=request.user)
    context = {
        "datas": all_data,
        "current_datetime": datetime.now(),
        "default_fee": 6500
    }
    return render(request, "six view.html", context)

@login_required
def updatesix(request, id):
    instance = get_object_or_404(fee, id=id)
    if not request.user.is_superuser and instance.user != request.user:
        messages.error(request, "You are not authorized to update this record.")
        return redirect('render_six_month_payment_view')
    if request.method == "POST":
        try:
            input_actualfee = int(request.POST.get("Actualfee", 0))
            input_datetime_str = request.POST.get("Datetime", "")
            old_pendingfee = instance.Pendingfee
            if input_actualfee == old_pendingfee:
                new_pendingfee = 0
            elif input_actualfee < old_pendingfee:
                new_pendingfee = old_pendingfee - input_actualfee
            else:
                messages.error(request, "Paid amount cannot exceed pending amount.")
                return redirect(request.path)
            instance.Actualfee += input_actualfee
            instance.Pendingfee = new_pendingfee
            instance.Datetime = input_datetime_str
            instance.save()
            messages.success(request, "Payment updated successfully!")
            return redirect('render_six_month_payment_view')
        except (ValueError, TypeError) as e:
            messages.error(request, f"Invalid input: {e}")
        except Exception as e:
            messages.error(request, f"Unexpected error occurred: {e}")
    context = {
        "instance": instance
    }
    return render(request, "updatesix.html", context)

@login_required
def updateyear(request, id):
    instance = get_object_or_404(fee, id=id)
    if not request.user.is_superuser and instance.user != request.user:
        messages.error(request, "You are not authorized to update this record.")
        return redirect('render_one_year_payment_view')
    if request.method == "POST":
        try:
            input_actualfee = int(request.POST.get("Actualfee", 0))
            input_datetime_str = request.POST.get("Datetime", "")
            old_pendingfee = instance.Pendingfee
            if input_actualfee == old_pendingfee:
                new_pendingfee = 0
            elif input_actualfee < old_pendingfee:
                new_pendingfee = old_pendingfee - input_actualfee
            else:
                messages.error(request, "Paid amount cannot exceed pending amount.")
                return redirect(request.path)
            instance.Actualfee += input_actualfee
            instance.Pendingfee = new_pendingfee
            instance.Datetime = input_datetime_str
            instance.save()
            messages.success(request, "Payment updated successfully!")
            return redirect('render_one_year_payment_view')
        except (ValueError, TypeError) as e:
            messages.error(request, f"Invalid input: {e}")
        except Exception as e:
            messages.error(request, f"Unexpected error occurred: {e}")
    context = {
        "instance": instance
    }
    return render(request, "updateyear.html", context)

def adpayment(request):
    return render_three_month_payment_view(request)

def sixpayment(request):
    return render_six_month_payment_view(request)

def pay(request):
    return render(request, "sixmonth.html", {})

def one(request):
    return render(request, "one year.html", {})

@login_required
def render_one_year_payment_view(request):
    if request.method == "POST":
        try:
            input_fee = int(request.POST.get("Fee", 0))
            input_actualfee = int(request.POST.get("Actualfee", 0))
            input_datetime_str = request.POST.get("Datetime", "")
            input_pendingfee = 0
            if input_actualfee < input_fee:
                input_pendingfee = input_fee - input_actualfee
            obj = fee()
            obj.user = request.user
            obj.Fee = input_fee
            obj.Actualfee = input_actualfee
            obj.Pendingfee = input_pendingfee
            obj.Datetime = input_datetime_str
            obj.save()
            messages.success(request, "Payment recorded successfully!")
            return redirect(request.path)
        except (ValueError, TypeError) as e:
            messages.error(request, f"Invalid input. Please enter valid numbers. Error: {e}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")
    all_data = fee.objects.all().order_by('-Datetime')
    if not request.user.is_superuser:
        all_data = all_data.filter(user=request.user)
    context = {
        "datas": all_data,
        "current_datetime": datetime.now(),
        "default_fee": 10000
    }
    return render(request, "oneyearview.html", context)

def onepayment(request):
    return render_one_year_payment_view(request)

@login_required
def attendanceview(request):
    if request.method == "POST":
        month = request.POST.get("month")
        attendance_date = request.POST.get("attendance_date")
        status = request.POST.get("status")
        try:
            attendance_date = datetime.strptime(attendance_date, '%Y-%m-%dT%H:%M').date()
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect('attendanceview')
        Attendance.objects.create(
            user=request.user,
            month=month,
            attendance_date=attendance_date,
            status=status
        )
        messages.success(request, "Attendance recorded successfully!")
        return redirect("attendanceview")
    filter_month = request.GET.get("month")
    if filter_month:
        user_attendance = Attendance.objects.filter(user=request.user, month=filter_month).order_by('-attendance_date')
    else:
        user_attendance = Attendance.objects.filter(user=request.user).order_by('-attendance_date')
    return render(request, "attendanceview.html", {"user_attendance": user_attendance})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully.")
            return redirect('add_product')
    else:
        form = ProductForm()
    return render(request, 'product.html', {'form': form})

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'prod.html', {'products': products})
