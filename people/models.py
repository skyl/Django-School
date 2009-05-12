import datetime
from django.db import models
from datetime import datetime, timedelta
from django.contrib.localflavor.us.models import PhoneNumberField, USStateField

from constants import title_choices, relationship_choices

from records.models import UserProfile, Student

def studs(o):
    stud_objs = Student.objects.filter(user=o.user)
    studs = ''
    for s in stud_objs:
        studs += s.name() + ', '
    return studs

class FamilyMember(models.Model):
    user = models.ForeignKey(UserProfile)
    title = models.CharField(max_length=4, choices=title_choices, blank=True, )
    name = models.CharField(max_length=70, )
    relationship = models.CharField(max_length=11, choices=relationship_choices,)
    phone = PhoneNumberField(blank=True,)
    email = models.EmailField(blank=True,)
    street_address = models.CharField(max_length=70, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = USStateField(default='GA', blank=True, )
    zip = models.CharField(max_length=5, blank=True)

    def students(self):
        return studs(self)

    def __unicode__(self):
        return "%s %s" % (self.title, self.name)

class EmergencyContacts(models.Model):
    user = models.OneToOneField(UserProfile)
    contact1 = models.CharField(max_length=70,verbose_name="First Contact")
    phone1 = PhoneNumberField(verbose_name="Phone")
    contact2 = models.CharField(max_length=70,verbose_name="Second Contact")
    phone2 = PhoneNumberField(verbose_name="Phone") 
    doctor = models.CharField(max_length=70,verbose_name="Doctor's Name")
    doctor_phone = PhoneNumberField(verbose_name="Doctor's Phone Number")

    def __unicode__(self):
        return "%s, %s-%s, %s-%s, %s-%s" % (self.user, self.contact1, self.phone1, self.contact2, self.phone2, self.doctor, self.doctor_phone)

    def students(self):
        stud_objs = Student.objects.filter(user=self.user)
        studs = ''
        for s in stud_objs:
            studs += s.name() + ', '
        return studs

    class Meta:
        verbose_name_plural = "Emergency Contacts"

class AuthorizedPickUpPerson(models.Model):
    name = models.CharField(max_length=70)
    relationship = models.CharField(max_length=30)
    phone = PhoneNumberField()
    user = models.ForeignKey(UserProfile)

    def students(self):
        stud_objs = Student.objects.filter(user=self.user)
        studs = ''
        for s in stud_objs:
            studs += s.name() + ', '
        return studs

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Pick-up Person"
        verbose_name_plural = "Pick-up People"

class Guardian(models.Model):
    user = models.ForeignKey(UserProfile)
    relationship = models.CharField(max_length=11, choices=relationship_choices)
    salute = models.CharField(max_length=4, choices=title_choices, blank=True )
    first = models.CharField(max_length=30)
    middle = models.CharField(max_length=30, blank=True)
    last = models.CharField(max_length=50)
    street_address = models.CharField(max_length=70, blank=True)
    city = models.CharField(max_length=30, blank=True)
    state = USStateField(default='GA', blank=True, )
    zip = models.CharField(max_length=5, blank=True)
    primary_phone = PhoneNumberField()
    secondary_phone = PhoneNumberField(blank=True)# help_text='(optional)')
    tertiary_phone = PhoneNumberField(blank=True)
    email = models.EmailField(blank=True)
    employer = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=50, blank=True)

    church = models.CharField(max_length=70)
    pastor = models.CharField(max_length=70)
    church_phone_number = PhoneNumberField(verbose_name="Church's phone")

    def students(self):
        ss = Student.objects.filter(user=self.user)
        string=''
        for s in ss:
            string += s.name() + ', '
        return string

    def __unicode__(self):
        return self.first + ' ' + self.last

from django.contrib.auth.models import User
class Volunteer(models.Model):
    user = models.ForeignKey(UserProfile)
    name = models.CharField(max_length=70)

    phone_number = PhoneNumberField(blank=True, )

    def associated_household(self):
        return "%s %s" % (self.user.addressee, self.user.primary_phone)

    def email(self):
        user = User.objects.get(userprofile=self.user)
        return user.email

    #    def areas(self):
    #        for field in self:

    classroom = models.BooleanField()
    campus = models.BooleanField()
    academic = models.BooleanField()
    music = models.BooleanField()
    library = models.BooleanField()
    art = models.BooleanField()
    yearbook = models.BooleanField()
    office = models.BooleanField()
    fundraising = models.BooleanField()
    maintenance = models.BooleanField()
    resources = models.BooleanField()

    def save(self, force_insert=False, force_update=False):
        if self.grade_papers or self.drive_for_trips or self.plan_supervise_trips or self.coordinate_class or self.tutor_under or self.substitute_short or self.refreshments or self.other_classroom:
            self.classroom = True

        if self.supervise_playground or self.supervise_lunch or self.before_after_substitute or self.assist_PE or self.provide_lunch_breaks_for_staff or self.other_campus:
            self.campus = True

        if self.substitute or self.aide or self.teach_expertise or self.tutor or self.judge_meet or self.other_academic:
            self.academic = True

        if self.piano or self.assist_performance or self.event_transport or self.other_music:
            self.music = True

        if self.check_out or self.proofread or self.process or self.shelve or self.maintain or self.other_library:
            self.library = True

        if self.bulletin_boards or self.backdrops or self.graphic_artist or self.judge_festival or self.decorations or self.art_teach_assist or self.art_class_helper or self.other_arts:
            self.art = True

        if self.photography or self.advertising or self.layout or self.supervise_students or self.other_yearbook:
            self.yearbook = True

        if self.substitute_secretary or self.provide_secretary_breaks or self.help_with_mailings or self.general_office or self.phone or self.word_processing or self.work_at_home or self.other_office:
            self.office = True

        if self.jogathon or self.auction or self. prizes_sponsors or self.grant_proposal or self.financial_consulting or self.annual_banquet or self.recruit_donors or self.other_fundraising:
            self.fundraising = True

        if self.landscape or self.painting or self.lend_large_vehicle or self.carpentry or self.cleaning or self.handyman or self.communications_network or self.other_maintenance:
            self.maintenance = True

        if self.business_equipment or self.construction or self.legal_services or self.accounting or self.other_resources:
            self.resources = True

        super(Volunteer, self).save(force_insert, force_update) # Call the "real" save() method.

    # classroom helpers
    grade_papers = models.BooleanField()
    drive_for_trips = models.BooleanField()
    plan_supervise_trips = models.BooleanField()
    coordinate_class = models.BooleanField()
    tutor_under = models.BooleanField()
    substitute_short = models.BooleanField()
    refreshments = models.BooleanField()
    other_classroom = models.CharField(max_length=100, blank=True)
    # playground and campus
    supervise_playground = models.BooleanField()
    supervise_lunch = models.BooleanField()
    before_after_substitute = models.BooleanField()
    assist_PE = models.BooleanField()
    provide_lunch_breaks_for_staff = models.BooleanField()
    other_campus = models.CharField(max_length=100, blank=True)
    # academic
    substitute = models.BooleanField()
    aide = models.BooleanField()
    teach_expertise = models.BooleanField()
    tutor = models.BooleanField()
    judge_meet = models.BooleanField()
    other_academic = models.CharField(max_length=100, blank=True)
    # music
    piano = models.BooleanField()
    assist_performance = models.BooleanField()
    event_transport = models.BooleanField()
    other_music = models.CharField(max_length=100, blank=True)
    # library and media center
    check_out = models.BooleanField()
    proofread = models.BooleanField()
    process = models.BooleanField()
    shelve = models.BooleanField()
    maintain = models.BooleanField()
    other_library = models.CharField(max_length=100, blank=True)
    # arts and crafts
    bulletin_boards = models.BooleanField()
    backdrops = models.BooleanField()
    graphic_artist = models.BooleanField()
    judge_festival = models.BooleanField()
    decorations = models.BooleanField()
    art_teach_assist = models.BooleanField()
    art_class_helper = models.BooleanField()
    other_arts = models.CharField(max_length=100, blank=True)
    # yearbook
    photography = models.BooleanField()
    advertising = models.BooleanField()
    layout = models.BooleanField()
    supervise_students = models.BooleanField()
    other_yearbook = models.CharField(max_length=100, blank=True)
    # office
    substitute_secretary = models.BooleanField()
    provide_secretary_breaks = models.BooleanField()
    help_with_mailings = models.BooleanField()
    general_office = models.BooleanField()
    phone = models.BooleanField()
    word_processing = models.BooleanField()
    work_at_home = models.BooleanField()
    other_office = models.CharField(max_length=100, blank=True, )
    # fundraising
    jogathon = models.BooleanField()
    auction = models.BooleanField()
    prizes_sponsors = models.BooleanField()
    grant_proposal = models.BooleanField()
    financial_consulting = models.BooleanField()
    annual_banquet = models.BooleanField()
    recruit_donors = models.BooleanField()
    other_fundraising = models.CharField(max_length=100, blank=True, )
    # maintenance
    landscape = models.BooleanField()
    painting = models.BooleanField()
    lend_large_vehicle = models.BooleanField()
    carpentry = models.BooleanField()
    cleaning = models.BooleanField()
    handyman = models.BooleanField()
    communications_network = models.BooleanField()
    other_maintenance = models.CharField(max_length=100, blank=True, )
    # resources or contacts
    business_equipment = models.BooleanField()
    construction = models.BooleanField()
    legal_services = models.BooleanField()
    accounting = models.BooleanField()
    other_resources = models.CharField(max_length=100, blank=True, )

    date = models.DateField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "volunteers"

