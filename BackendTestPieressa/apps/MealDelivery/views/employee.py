from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from ..forms.employee import EmployeeForm
from ..models.employee import Employee

@login_required(login_url='MealDelivery:login')
def employee(request):
    """Controls the employee view. It shows all current employees with the
    possibility of removing them from the system. Users can add new employees
    given a username and a name.

    Args:
        request (object): request given to the view

    Returns:
        render: render user to the view
    """
    employees = Employee.objects.all()
    if request.method == 'POST':
        employee_form = EmployeeForm(request.POST)
        if employee_form.is_valid():
            employee_form.save()
            return redirect('MealDelivery:add_employee')
    else:
        employee_form = EmployeeForm()
    return render(request, 'MealDelivery/components/models/employee.html', {
        'employee_form': employee_form,
        'employees': employees
    })

@login_required(login_url='MealDelivery:login')
def delete_employee(request, id):
    """Deletes an employee from the system.

    Args:
        request (object): request given to the view
        id (string): username of the employee to remove

    Returns:
        redirect: redirect user to the view employee view
    """
    employee_object = Employee.objects.get(username=id)
    employee_object.delete()
    return redirect('MealDelivery:add_employee')
