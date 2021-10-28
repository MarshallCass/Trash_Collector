from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django import forms
from datetime import datetime
from datetime import date
from .models import Employee
from customers.models import Customer

# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.

@login_required
def index(request):
    logged_in_user = request.user
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
 
    try:
        # This line will return the customer record of the logged-in user if one exists
        logged_in_employee = Employee.objects.get(user=logged_in_user)

        today = date.today()
        logged_in_employee_zip_code = logged_in_employee.zip_code
        Customer = apps.get_model('customers.Customer')
        customer_in_zip = Customer.objects.filter(zip_code=logged_in_employee_zip_code)
        
        context = {
            'logged_in_employee': logged_in_employee,
            'today': today,
            'customer_in_zip': customer_in_zip
        }
        
        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))

@login_required
def employee_index(request):
    customer = Customer.objects.all()
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    customer = apps.get_model('customers.Customer')
    logged_in_employee_zip_code = logged_in_employee.zip_code
    today = date.today()
    weekday = today.strftime('%A')
    todays_date = datetime.now()
        
    todays_customer = Customer.objects.filter(Q(zip_code=logged_in_employee_zip_code) & Q(weekly_pickup=weekday) or Q(one_time_pickup=weekday)).exclude(date_of_last_pickup=todays_date)
    context = {
            'logged_in_employee': logged_in_employee,
            'customer' : customer,
            'todays_customer' : todays_customer,
  
        }
    return render(request, 'employees/employee_index.html', context)
    

@login_required
def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        new_employee = Employee(name=name_from_form, user=logged_in_user,  address=address_from_form, zip_code=zip_from_form)
                               
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')

@login_required
def edit_profile(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zipcode')
        logged_in_employee.name = name_from_form
        logged_in_employee.address = address_from_form
        logged_in_employee.zip_code = zip_from_form
        logged_in_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'logged_in_employee': logged_in_employee
        }
        return render(request, 'employees/edit_profile.html', context)

@login_required
def confirm_pickup(request, customer_id):
    try:
        Customer = apps.get_model('customers.Customer')
        customer_pickup = Customer.objects.get(id = customer_id)
        customer_pickup.balance += 20
        customer_pickup.date_of_last_pickup = datetime.now()
        customer_pickup.save()

        return render(request, 'employees/index.html')
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:index'))           
