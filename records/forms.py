
from records.models import UserProfile, Student, Application, MiddleSchoolStudentQuestionnaire, CurrentSchool, ParentPart

from people.models import Guardian, FamilyMember, AuthorizedPickUpPerson, Volunteer, EmergencyContacts

from django.forms import ModelForm
from django.forms import DateField
from django.forms.extras.widgets import SelectDateWidget


class VolunteerForm(ModelForm):
    class Meta:
        model = Volunteer
        exclude = ('user','date', 'classroom',
                'campus', 
                'academic', 
                'music', 
                'library', 
                'art', 
                'yearbook', 
                'office', 
                'fundraising',
                'maintenance', 
                'resources',
)

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'has_completed_profile', 'has_added_guardians', 'has_added_church',
                   'has_added_family', 'has_signed_form', 'has_signed_contract', )

# These are the forms that are part of the application process


class StudentApplyForm(ModelForm):
    date_of_birth = DateField(widget=SelectDateWidget(years=[1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009]))
    class Meta:
        model = Student
#        exclude = ('application_completed', 'registration_signed_paid', 'currently_student', 'enrolled_for_upcoming_year', 'alumni', 'user', 'allergies', 'allergy_description','date', 'changes_affect')
        fields = ('last','first','middle','preferred_name','present_grade','next_grade','date_of_birth','gender','living_with')

class StudentAddForm(StudentApplyForm):
    class Meta:
        model = Student
        fields = ('last','first','middle','preferred_name','present_grade','next_grade','date_of_birth','gender','living_with', 'allergies', 'allergy_description',)
        

import datetime    
class ApplicationForm(ModelForm):
    dated = DateField(initial=datetime.date.today())
    class Meta:
        model = Application
        exclude = ('student')

class MSSQForm(ModelForm):
    dated = DateField(initial=datetime.date.today())
    class Meta:
        model = MiddleSchoolStudentQuestionnaire
        exclude = ('application')

class CurrentSchoolForm(ModelForm):
    class Meta:
        model = CurrentSchool
        exclude = ('application')

class ParentForm(ModelForm):
    dated = DateField(initial=datetime.date.today())
    class Meta:
        model = ParentPart
        exclude = ('application')

class EmergencyContactsForm(ModelForm):
    class Meta:
        model = EmergencyContacts
        exclude = ('user')

