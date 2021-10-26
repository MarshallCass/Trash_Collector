from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
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
        
        context = {
            'logged_in_employee': logged_in_employee,
            'today': today,
        }
        
        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))

@login_required
def employee_index(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    customer = apps.get_model('customers.Customer')
    all_customers = Customer.objects.all()
    today = date.today()
    weekday = today.strftime('%A')
    todays_customers = []
    context = {
            'logged_in_employee': logged_in_employee,
            'today': today,
            'todays_customers': todays_customers
        }
    if request.method == "POST":
        for customer in all_customers:
            if customer.zip_code == logged_in_employee.zip_code and customer.pickup_day == weekday and customer.suspend_start == False or customer.onetime_pickup == weekday:
                todays_customers.append(customer)
        return render(request, 'employees/employee_index.html', context)
    else:
        return HttpResponseRedirect(reverse('employees:index'))


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
