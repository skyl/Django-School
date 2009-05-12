import datetime

from django.http import HttpResponseRedirect  #, HttpResponse
from django.shortcuts import render_to_response

from django.template import RequestContext

from django.contrib.auth.decorators import login_required

from records.models import UserProfile, Student
from menu.models import Meal, Lunch, Order, Account, DateSet, Voucher
from menu.forms import PizzaOrderForm, ChickOrderForm, HotOrderForm

#hot_order_price = 5.00
min_order=1.00

@login_required
def order(request, studentid, year, month, day):
    date = datetime.date(int(year), int(month), int(day))
    try:
            profile = request.user.get_profile()

    except:
            return HttpResponseRedirect('/records/profile/')

    try:
        student = Student.objects.get(id=studentid)
        profile_for_student = UserProfile.objects.get(student=student)

    except:
            return HttpResponseRedirect('/apply/')

    try:
        today = datetime.date.today()
        dateset = DateSet.objects.get(start_taking_orders__lte = today, end_taking_orders__gte = today)
        account = Account.objects.get(profile=profile, paid=False, dateset=dateset)
    except:
        return HttpResponseRedirect('/') # There is no ordering going on right now!  Or, there is no account

    if profile == profile_for_student:
        try:
            lunch = Lunch.objects.get(date__year=year, date__month=month, date__day=day)
        except:
            return HttpResponseRedirect('/menu/')

        try:
            order = Order.objects.get(lunch=lunch, student=student)
            if request.method == 'POST':

                if lunch.meal.type == 'A':
                    form = HotOrderForm(request.POST, instance=order)

                    if form.is_valid():
                        order = form.save(commit=False)
                        order.student = student
                        order.lunch = lunch
                        order.hot_lunch=1
                        order.save()
                        return HttpResponseRedirect('/menu/') # where?

                if lunch.meal.type == 'B':
                    form = PizzaOrderForm(request.POST, instance=order)

                    if form.is_valid():
                        order = form.save(commit=False)
                        order.student = student
                        order.lunch = lunch
                        order.save()
                        return HttpResponseRedirect('/menu/') # where?

                if lunch.meal.type == 'C':
                    form = ChickOrderForm(request.POST, instance=order)

                    if form.is_valid():
                        order = form.save(commit=False)
                        order.student = student
                        order.lunch = lunch
                        order.save()
                        return HttpResponseRedirect('/menu/') # where?

            else:
                cancel = True
                if lunch.meal.type == 'A':
                    form = HotOrderForm(instance=order)

                if lunch.meal.type == 'B':
                    form = PizzaOrderForm(instance=order)

                if lunch.meal.type == 'C':
                    form = ChickOrderForm(instance=order)

        except:
            if request.method == 'POST':

                if lunch.meal.type == 'A':
                    form = HotOrderForm(request.POST)

                    if form.is_valid():
                        order = form.save(commit=False)
                        order.student = student
                        order.lunch = lunch
                        order.save()
                        return HttpResponseRedirect('/menu/') # where?

                if lunch.meal.type == 'B':
                    form = PizzaOrderForm(request.POST)

                    if form.is_valid():
                        order = form.save(commit=False)
                        order.student = student
                        order.lunch = lunch
                        order.save()
                        return HttpResponseRedirect('/menu/') # where?

                if lunch.meal.type == 'C':
                    form = ChickOrderForm(request.POST)

                    if form.is_valid():
                        order = form.save(commit=False)
                        order.student = student
                        order.lunch = lunch
                        order.save()
                        return HttpResponseRedirect('/menu/') # where?

            else:
                cancel = False
                if lunch.meal.type == 'A':
                    form = HotOrderForm()

                if lunch.meal.type == 'B':
                    form = PizzaOrderForm()

                if lunch.meal.type == 'C':
                    form = ChickOrderForm()
    else:
        return HttpResponseRedirect('/')
    path = request.path
    context = {'student':student, 'profile':profile, 'lunch':lunch,\
            'form':form, 'path':path, 'cancel':cancel, }
    return render_to_response('menu/order.html', context,  context_instance=RequestContext(request))

@login_required
def paynow(request, id):
    try:
        account = Account.objects.get(id=id)
    except:
        return HttpResponseRedirect('/menu/')

    if account.profile == request.user.get_profile():
        from settings import MEDIA_URL
        context = {'account':account, 'MEDIA_URL':MEDIA_URL, }
        return render_to_response('menu/paynow.html', context) #RequestContext?
    else:
        return HttpResponseRedirect('/menu/')


@login_required
def see(request):
    try:
        profile = request.user.get_profile()
    except:
        return HttpResponseRedirect('/records/profile/')


    today = datetime.date.today()

    try:
        dateset = DateSet.objects.get(start_taking_orders__lte = today, end_taking_orders__gte = today)
    except:
        return HttpResponseRedirect('/') # There is no ordering going on right now!

    lunches = dateset.lunches()
    students = Student.objects.filter(user=profile).filter(currently_student=True)

    try:
        account = Account.objects.get(profile=profile, dateset=dateset, paid=False)
    except:
        account = Account.objects.create(profile=profile, dateset=dateset)

    if float(account.total()) > min_order:
        pay = True

    else:
        pay = False

    vouchers = Voucher.objects.filter(student__user=profile)

    from people.models import Volunteer
    volunteers = Volunteer.objects.filter(user=profile)
    context = {'volunteers':volunteers, 'lunches':lunches, 'profile':profile,\
               'students':students, 'dateset':dateset, 'account':account, 'pay':pay,\
               'vouchers':vouchers}
    return render_to_response('menu/see.html', context, context_instance=RequestContext(request))

@login_required
def cancel(request, studentid, year, month, day):
    try:
        student = Student.objects.get(user=request.user.get_profile(), id=studentid)
        lunch = Lunch.objects.get(date__year=year, date__month=month, date__day=day)
        order = Order.objects.get(lunch=lunch, student=student)
        order.delete()
        return HttpResponseRedirect('/menu/')

    except:
        return HttpResponseRedirect('/menu/')



