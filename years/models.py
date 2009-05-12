from django.db import models
from datetime import datetime, timedelta

from records.models import Student

grade_choices = (
    ('k4','K4'),
    ('k5','K5'),
    ('1','1st'),
    ('2','2nd'),
    ('3','3rd'),
    ('4','4th'),
    ('5','5th'),
    ('6','6th'),
    ('7','7th'),
    ('8','8th'),
)

title_choices = (
    ('Mr','Mr.'),
    ('Mrs','Mrs.'),
    ('Ms','Ms.'),
    ('Miss','Miss'),
    ('Dr','Dr.'),
    ('Prof','Prof.'),
    ('Rev','Rev.'),
)

class HomeroomLeader(models.Model):
    title = models.CharField(max_length=4, choices = title_choices)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return "%s %s" % (self.title, self.name)


class SchoolYear(models.Model):
    first_day_of_school = models.DateField(unique=True)
    last_day_of_school = models.DateField()

    application_deadline = models.DateField(verbose_name="Application Deadline")
    application_price = models.PositiveIntegerField()

    enroll1 = models.DateField(verbose_name="Enrollment Price 1 Deadline")
    enroll1_price = models.PositiveIntegerField()
    enroll2 = models.DateField(verbose_name="Enrollment Price 2 Deadline")
    enroll2_price = models.PositiveIntegerField()
    enroll3 = models.DateField(verbose_name="Final Enrollment Deadline")
    enroll3_price = models.PositiveIntegerField()

    register1 = models.DateField(verbose_name="Discount Registration Deadline")
    register1_price = models.PositiveIntegerField()
    register2 = models.DateField(verbose_name="Final Registration Deadline")
    register2_price = models.PositiveIntegerField()

    deadline4 = models.DateField()
    deadline5 = models.DateField()

    last = models.BooleanField()
    current = models.BooleanField()
    next = models.BooleanField()

    def is_current_year(self):
        if datetime.date.today() >= self.start_date and datetime.date.today() <= self.end_date:
            return True
        else:
            return False 

    def __unicode__(self):
        return "%s-%s" % (self.first_day_of_school.year, self.last_day_of_school.year)

    def save(self, force_insert=False, force_update=False):
        if self.is_current_year:
            self.current=True
        super(SchoolYear, self).save(force_insert, force_update) # Call the "real" save() method.


class HomeroomMember(models.Model):

    def __unicode__(self):
        return "%s, %s %s" % (self.member.name, self.homeroom.grade, self.homeroom.leader)

from django.db.models import Q
class HomeroomMemberK4(HomeroomMember):
    homeroom = models.ForeignKey('HomeroomK4')
    member = models.ForeignKey(Student, limit_choices_to=Q(present_grade='k4')|Q(next_grade='k4'))

#class HomeroomMemberK5(HomeroomMember):
#    homeroom = models.ForeignKey('HomeroomK5')

#class HomeroomMember1(HomeroomMember):
#    homeroom = models.ForeignKey('Homeroom1')

#class HomeroomMember2(HomeroomMember):
#    homeroom = models.ForeignKey('Homeroom2')

#class HomeroomMember3(HomeroomMember):
#    homeroom = models.ForeignKey('Homeroom3')

#class HomeroomMember4(HomeroomMember):
#    homeroom = models.ForeignKey('Homeroom4')

#class HomeroomMember5(HomeroomMember):
#    homeroom = models.ForeignKey('Homeroom5')

#class HomeroomMember6(HomeroomMember):
#    homeroom = models.ForeignKey('Homeroom6')

#class HomeroomMember7(HomeroomMember):
#    homeroom = models.ForeignKey('Homeroom7')

#class HomeroomMember8(HomeroomMember):
#    homeroom = models.ForeignKey('Homeroom8')


class Homeroom(models.Model):
    year = models.ForeignKey('SchoolYear')
    leader = models.ForeignKey('HomeroomLeader')

    def __unicode__(self):
        return "%s %s" % (self.leader, self.year)

    def student_list(self):
        ss = Students.objects.filter(classroom=self)
        return ss

    def students_set(self):
        ss = ''
        for s in self.student_list:
            ss += s + ', '
        return ss

class HomeroomK4(Homeroom):
    grade = 'k4'            
#class HomeroomK5(Homeroom):
#    grade = 'k5'            
#class Homeroom1(Homeroom):
#    grade = '1'            
#class Homeroom2(Homeroom):
#    grade = '2'            
#class Homeroom3(Homeroom):
#    grade = '3'            
#class Homeroom4(Homeroom):
#    grade = '4'            
#class Homeroom5(Homeroom):
#    grade = '5'            
#class Homeroom6(Homeroom):
#    grade = '6'            
#class Homeroom7(Homeroom):
#    grade = '7'            
#class Homeroom8(Homeroom):
#    grade = '8'            

