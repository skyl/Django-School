import datetime
from django.db import models
from datetime import datetime, timedelta
from django.contrib.localflavor.us.models import PhoneNumberField, USStateField

gender_choices = (
    ('m', 'Male'),
    ('f', 'Female')
)

relationship_choices = (
    ('mother', 'Mother'),
    ('father', 'Father'),
    ('grandfather', 'Grandfather'),
    ('grandmother', 'Grandmother'),
    ('aunt', 'Aunt'),
    ('uncle', 'Uncle'),
    ('brother', 'Brother'),
    ('sister', 'Sister'),
    ('cousin', 'Cousin'),
    ('other', 'Other'),
)

scale_choices = (
    ('5', '5'),
    ('4', '4'),
    ('3', '3'),
    ('2', '2'),
    ('1', '1'),
)

from constants import title_choices, grade_choices, gender_choices

attend_choices = (
    ('y', 'Daily'),
    ('s', 'Some'),
    ('n', 'Never'),
)

from django.contrib.auth.models import User
#from people.models import EmergencyContacts
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, )
    addressee = models.CharField(max_length=70, verbose_name="Account Name",help_text="This could be 'The Smiths' or 'John & Diane Smith'",)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = USStateField(default='GA')
    zip = models.CharField(max_length=5)
    primary_phone = PhoneNumberField()

    def students(self):
        ss = Student.objects.filter(user=self.user)
        string=''
        for s in ss:
            string += s.name() + ', '
        return string


    def guardians(self):
        from people.models import Guardian
        gs = Guardian.objects.filter(user=self.user)
        string=''
        for g in gs:
            string += "%s %s, " % (g.first, g.last)
        return string

    def email(self):
        return self.user.email

    def __unicode__(self):
        return self.addressee

    def emergency_contacts(self):
        from people.models import EmergencyContacts
        ec = EmergencyContacts.objects.get(user=self)
        return "%s @%s, %s @%s, Doctor %s @%s" % (ec.contact1, ec.phone1,\
                ec.contact2, ec.phone2, ec.doctor, ec.doctor_phone)

    def ongoing_app_form(self):
        if Student.objects.filter(user=self, application_form_complete=False):
            return True
        else:
            return False

    def pending_application(self):
        if Student.objects.filter(user=self, application_form_complete=True,
                decision_made=None):
            return True
        else:
            return False

class Student(models.Model):
    user = models.ForeignKey('UserProfile')
    last = models.CharField(max_length=50)
    first = models.CharField(max_length=30)
    middle = models.CharField(max_length=30, blank=True)
    preferred_name = models.CharField(max_length=30)
    present_grade = models.CharField(max_length=3, choices=grade_choices)
    next_grade = models.CharField(max_length=3, choices=grade_choices)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=gender_choices)
    living_with_choices = (
        ('b', 'Both Parents'),
        ('m', 'Mother'),
        ('f', 'Father'),
        ('o', 'Other'),
    )
    living_with = models.CharField(max_length=1, choices=living_with_choices)
    changes_affect = models.TextField(blank=True)
    allergies = models.BooleanField()
    allergy_description = models.TextField(blank=True)

    # Application Process
    application_form_completed_on = models.DateField(blank=True, null=True)
    application_form_complete = models.BooleanField()

    application_payment_completed_on = models.DateField(blank=True,null=True)
    application_payment_complete = models.BooleanField()

    entrance_testing_scheduled_for = models.DateField(blank=True,null=True)
    entrance_testing_complete = models.BooleanField()

    parent_interview_scheduled_for = models.DateField(blank=True,null=True)
    parent_interview_complete = models.BooleanField()

    student_interview_scheduled_for = models.DateField(blank=True,null=True)
    student_interview_complete = models.BooleanField()

    decision_made = models.DateField(blank=True,null=True)
    student_accepted = models.BooleanField()

    # Registration Process
    registration_signed_paid = models.BooleanField()
    registration_signed_paid_on = models.DateField(blank=True,null=True)

    complete_documents = models.BooleanField()
    complete_documents_on = models.DateField(blank=True,null=True)

    custody_decision_received = models.BooleanField()
    custody_decision_received_on = models.DateField(blank=True,null=True)

    birth_certificate_received = models.BooleanField()
    birth_certificate_received_on = models.DateField(blank=True,null=True)

    immunization_record_received = models.BooleanField()
    immunization_record_received_on = models.DateField(blank=True,null=True )

    emergency_medical_card_received = models.BooleanField()
    emergency_medical_card_received_on = models.DateField(blank=True, null=True)

    plan = (
        ('1','This plan'),
        ('2', 'That plan'),
    )
    payment_plan =  models.CharField(max_length=1, choices=plan, blank=True)
    registration_complete = models.BooleanField()

    # General status
    currently_student = models.BooleanField()
    enrolled_for_upcoming_year = models.BooleanField()
    alumni = models.BooleanField()

    def age_in_years(self):
        return str((datetime.date.today()-self.date_of_birth).days/365)

    def guardians(self):
        from people.models import Guardian
        g=Guardian.objects.filter(user=self.user)
        s=''
        for o in g:
            s += o.__unicode__() + ', '
        return s

    def __unicode__(self):
        name = self.preferred_name + ' ' + self.last
        return name

    def name(self):
        return self.preferred_name + ' ' + self.last

    class Meta:
        verbose_name_plural = "students"

class BeforeAfterPrograms(models.Model):
    student = models.OneToOneField('Student')
    before_school = models.CharField(max_length=1, choices=attend_choices)
    after_school = models.CharField(max_length=1, choices=attend_choices)

from years.models import SchoolYear
class Enrollment(models.Model):
    student = models.ForeignKey('Student')
    year = models.ForeignKey(SchoolYear)
    date_paid = models.DateField()

    def __unicode__(self):
        return "%s - %s" % (self.student, self.year)

class Application(models.Model):
    student = models.OneToOneField('Student')
    scholastic_difficulties = models.BooleanField()
    learning_differences = models.BooleanField()
    special_education = models.BooleanField()
    extended_absences = models.BooleanField()
    physical_emotional = models.BooleanField()
    reason_to_not_attend = models.BooleanField()
    if_yes_explain = models.TextField(blank=True)
    interests_skills_hobbies = models.TextField(blank=True)
    why_enroll = models.TextField(blank=True)
    why_change_school = models.TextField(blank=True)
    hope_to_benefit = models.TextField(blank=True)
    entering_6th_7th_or_8th = models.BooleanField()

    signed = models.CharField(max_length=70)
    dated = models.DateField()

    def __unicode__(self):
        return self.student.preferred_name + ' ' + self.student.last + ' '  + str(self.dated)

class ParentPart(models.Model):
    application = models.OneToOneField('Application')
    why_believe = models.TextField(blank=True, )
    bible = models.TextField(blank=True)
    ways_follow_bible = models.TextField(blank=True)
    bible_as_parent = models.TextField(blank=True)
    ccs_help_as_christian_parent = models.TextField(blank=True)
    why_not_enrolling_siblings = models.TextField(blank=True)
    where_did_you_hear_about = models.TextField(blank=True)

    signed = models.CharField(max_length=70)
    dated = models.DateField()

    def __unicode__(self):
        return "%s %s" % (self.application, self.signed)

    class Meta:
        verbose_name_plural = "Parent Portion of Application"

class MiddleSchoolStudentQuestionnaire(models.Model):
    application = models.OneToOneField('Application')
    church_choices = (
        ('1', 'Almost every Sunday'),
        ('2', '2 or 3 times a month'),
        ('3', 'Once a month'),
        ('4', '3 or 4 times a year'),
    )
    church_attendance = models.CharField(max_length=1, choices=church_choices,\
            verbose_name="You attend church")
    grade_choices = (
        ('A', "I get mostly A's"),
        ('B', "I get mostly B's"),
        ('C', "I get mostly C's"),
        ('D', "I get mostly D's"),
    )
    grades = models.CharField(max_length=1, choices=grade_choices, verbose_name="Grades you get")
    activities_enjoy = models.TextField(verbose_name="Tell us about activities you enjoy")
    best_courses = models.TextField(verbose_name="Tell us about your favorite classes")
    worst_courses = models.TextField(verbose_name="Least favorite classes?")
    life = models.TextField(verbose_name="What do you envision doing with your life?")
    means_to_be_christian = models.TextField(verbose_name="What does being a Christian mean to you?" )
    other_choices = (
        ('1', 'I really enjoy doing things with others'),
        ('2', 'I enjoy doing things with others but also enjoy spending time with myself'),
        ('3', 'I would rather spend time alone than with others'),
    )
    with_others = models.CharField(max_length=1, choices=other_choices, verbose_name="Which best describes you?")
    music = models.CharField(max_length=1, choices=scale_choices)
    reading = models.CharField(max_length=1, choices=scale_choices)
    bible_study = models.CharField(max_length=1, choices=scale_choices)
    school = models.CharField(max_length=1, choices=scale_choices, verbose_name="Doing Homework")
    television = models.CharField(max_length=1, choices=scale_choices)
    attending_college = models.CharField(max_length=1, choices=scale_choices)
    athletics = models.CharField(max_length=1, choices=scale_choices)

    won_awards = models.BooleanField(verbose_name="Have you won awards?")
    awards_explain = models.TextField(blank=True, verbose_name="If yes, explain")
    trouble = models.BooleanField(verbose_name="Have you been in trouble?")
    trouble_explain = models.TextField(blank=True, verbose_name="If yes, explain")
    christian = models.BooleanField(verbose_name="Are you a Christian?")
    christian_explain = models.TextField(blank=True, verbose_name="Tell us about your religion")
    considering_other = models.BooleanField(verbose_name="Are you considering other schools?")
    considering_other_explain = models.TextField(blank=True, verbose_name="If yes, which ones? What will determine your decision?")

    signed = models.CharField(max_length=40)
    dated = models.DateField()

    def __unicode__(self):
        return "%s %s" % (self.application, self.signed)

    class Meta:
        verbose_name_plural = "Middle School Student Questionnaires"

class CurrentSchool(models.Model):
    application = models.OneToOneField('Application')
    name = models.CharField(max_length=50, blank=True)
    street_address = models.CharField(max_length=70, blank=True)
    city = models.CharField(max_length=30, blank=True)
    state = USStateField(default='GA', blank=True)
    zip = models.CharField(max_length=5, blank=True)
    phone = PhoneNumberField(blank=True)
    email = models.EmailField(blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Applicant's School"

class DisciplinaryAction(models.Model):
    student = models.ForeignKey('Student')
    short_description = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()

    def __unicode__(self):
        return "%s %s" % (self.student, self.short_description)


