import datetime
from django.db import models

meal_choices = (
        ('A', 'Hot Lunch' ),
        ('B', 'Pizza' ),
        ('C', 'Chick-fil-a'),
        ('D', 'No Lunch'),
)

def iterdates(first, last):
    for day in range((last - first).days + 1):
        yield first + datetime.timedelta(day)

class Meal(models.Model):
    name = models.CharField(max_length=50)
    # description = models.TextField()
    type = models.CharField(max_length=1, choices=meal_choices)

    def __unicode__(self):
        return self.name

class Lunch(models.Model):
    date = models.DateField(unique=True)
    meal = models.ForeignKey('Meal', unique_for_date='date')
    description = models.CharField(max_length=100, blank=True)

    def is_mon(self):
        return self.date.weekday() == 0

    def is_tue(self):
        return self.date.weekday() == 1

    def is_wed(self):
        return self.date.weekday() == 2

    def is_thu(self):
        return self.date.weekday() == 3

    def is_fri(self):
        return self.date.weekday() == 4

    def is_first_of_month(self):
        monthlunches = Lunch.objects.filter(date__month=self.date.month)
        for l in monthlunches:
            if l.date.day < self.date.day:
                return False
        return True

    def month(self):
        return self.date.strftime("%B")

    def future(self):
        today = datetime.date.today()
        return self.date >= today

    def __unicode__(self):
        return self.meal.name + ' ' + str(self.date)

    def students(self):
        orders = Order.objects.filter(lunch=self)
        students = []

        for order in orders:
            students.append(order.student)

        return students

    def students_paid(self):
        orders = Order.objects.filter(lunch=self, paid=True)
        students = []

        for order in orders:
            students.append(order.student)
        return students

    def student_has_ordered(self, s):
        orders = Order.objects.filter(lunch=self)
        students = []

        for order in orders:
            students.append(order.student)

        if s in students:
            return True

        else:
            return False

    # def number_total(self):

    def number(self):
        orders = Order.objects.filter(lunch=self, paid=True)

        if self.meal.type == 'A':
            number = 0
            for order in orders:
                number += order.hot_lunch
            return '%d hot meals' % number

        if self.meal.type == 'B':
            cheese = 0
            pepperoni = 0

            for order in orders:
                cheese += order.cheese
                pepperoni += order.pepperoni
            return '%d cheese and %d pepperoni' % (cheese, pepperoni)

        if self.meal.type == 'C':
            nuggets = 0
            sandwiches = 0

            for order in orders:
                nuggets += order.nuggets
                sandwiches += order.sandwiches
            return '%d nuggets and %d sandwiches' % (nuggets, sandwiches)

    class Meta:
        verbose_name_plural = "Lunches"

number_choices = (
    (0,'0'),
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)

prices = {
        'chik':3.00,
        'pizza':1.25,
        'hot':3.25,
}


from records.models import Student, UserProfile

class DateSet(models.Model):
    start_taking_orders = models.DateField()
    end_taking_orders = models.DateField()

    start = models.DateField()
    end = models.DateField()

    def lunches(self):
        ls = Lunch.objects.filter(date__gte = self.start, date__lte = self.end).order_by('date')
        return ls

    def __unicode__(self):
        if self.start.month in (6,7,8,9,10):
            return "Fall %s" % (self.start.year)
        if self.start.month in (12,1,2):
            return "Winter %s-%s" % (self.start.year, self.end.year)
        if self.start.month in (3,4,5):
            return "Spring %s" % (self.start.year)

    def save(self, force_insert=False, force_update=False):
        for day in iterdates(self.start, self.end):
            try:
                l=Lunch.objects.get(date=day)
            except:
                if day.weekday() == 0:
                    meal = Meal.objects.get(type='C')
                    l=Lunch(date=day, meal=meal, description="8 piece nuggets \
                                                                or sandwich, $3.00")
                    l.save()

                if day.weekday() == 4:
                    meal = Meal.objects.get(type='B')
                    l=Lunch(date=day, meal=meal, description="Cheese or pepperoni, $1.25")
                    l.save()

                if day.weekday() in [1, 2, 3]:
                    meal = Meal.objects.get(type='A')
                    l=Lunch(date=day, meal=meal, description="This hotmeal is $3.25")
                    l.save()

        super(DateSet, self).save(force_insert, force_update) # Call the "real" save() method.

class Account(models.Model):
    profile = models.ForeignKey(UserProfile)
    dateset = models.ForeignKey('DateSet')
    paid = models.BooleanField()

    def already_paid(self):
        total=0
        orders = Order.objects.filter(paid=True, student__user=self.profile, lunch__in=self.dateset.lunches())
        for order in orders:
            total += order.charge()

        return "%.2f" % total

    def total(self):
        total = 0
        orders = Order.objects.filter(paid=False, student__user=self.profile).filter(lunch__in=self.dateset.lunches())

        for order in orders:
            total += order.charge()

        return "%.2f" % total

    def vouchers(self):
        return Voucher.objects.filter(student__user=self.profile)

    def vouchers_total(self):
        total = 0
        for v in self.vouchers():
            total += v.amount
        return "%.2f" % total

    def total_minus_vouchers(self):
        r = float(self.total()) - float(self.vouchers_total())
        return "%.2f" % r


    def __unicode__(self):
        return "%s, %s" % (self.profile, self.dateset)

class Order(models.Model):
    student = models.ForeignKey(Student)
    lunch = models.ForeignKey('Lunch')
    # account = models.ForeignKey('Account')
    paid = models.BooleanField()

    nuggets = models.IntegerField(choices = number_choices, blank=True, default=0)
    sandwiches = models.IntegerField(choices = number_choices, blank=True, default=0)

    cheese = models.IntegerField(choices = number_choices, blank=True, default=0)
    pepperoni = models.IntegerField(choices = number_choices, blank=True, default=0)

    hot_lunch = models.IntegerField(blank=True, default=0)

    def save(self, force_insert=False, force_update=False):
        if self.lunch.meal.type=='A':
            self.hot_lunch=1
        super(Order, self).save(force_insert, force_update) # Call the "real" save() method.

    def charge(self):
        return self.hot_lunch*prices['hot'] + self.cheese*prices['pizza'] + self.pepperoni*prices['pizza']\
                + self.sandwiches*prices['chik'] + self.nuggets*prices['chik']

    def __unicode__(self):
        return "%s, %s" % (self.student, self.lunch)

    @models.permalink
    def get_absolute_url(self):
        return ('place_order', (), {
                'studentid': self.student.id,
                'year': self.lunch.date.year,
                'month': self.lunch.date.month,
                'day': self.lunch.date.day,})

class Voucher(models.Model):
    student = models.OneToOneField(Student)
    amount = models.DecimalField(max_digits=4, decimal_places=2)

    date = models.DateField(blank=True, null=True,)
    def __unicode__(self):
        return "%s, %s" % (self.student, self.amount)


