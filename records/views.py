import datetime
from django.http import HttpResponseRedirect  #, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from records.models import UserProfile, Student, ParentPart, Application, MiddleSchoolStudentQuestionnaire, CurrentSchool

from people.models import FamilyMember, AuthorizedPickUpPerson, Volunteer, EmergencyContacts, Guardian

no_profile_redirect = '/records/profile/'
######## Utilities
def profileOrRedirect(request):
    ''' Utility to make sure that we have a profile to jointo'''
    try:
        return request.user.get_profile()

    except:
        return HttpResponseRedirect(no_profile_redirect)

def addQuerySet(set, context):
    ''' Utility to add a queryset to a context with naming convention '''
    c = context.update({set.model._meta.verbose_name_plural:set})
    return c

def addToContext(profile, context):
    ''' Add a user's objects to context '''
    students = Student.objects.filter(user=profile)
    volunteers = Volunteer.objects.filter(user=profile)
    context.update({students.model._meta.verbose_name_plural:students,\
            volunteers.model._meta.verbose_name_plural:volunteers})

###### Request Handlers
def home(request):
    ''' Parent Dashboard '''
    try:
        profile = request.user.get_profile()
    except:
        profile = None

    if profile:
        volunteers = Volunteer.objects.filter(user=profile)
        connections = FamilyMember.objects.filter(user=profile)
        pickups = AuthorizedPickUpPerson.objects.filter(user=profile)
        guardians = Guardian.objects.filter(user=profile)
        students = Student.objects.filter(user=profile)
        ecs = EmergencyContacts.objects.filter(user=profile)

    else:
        volunteers=connections=pickups=guardians=students=ecs=None

    if request.path == '/thankyou/':
        thanks=True
    else:
        thanks=False

    dash = True
    context = {'profile': profile, 'volunteers':volunteers,\
            'connections':connections, 'pickups':pickups,\
            'guardians':guardians, 'students': students,\
            'ecs':ecs, 'thanks':thanks, 'dash': dash,\
            }
    return render_to_response('records/home_start.html', context, context_instance=RequestContext(request))

from records.forms import VolunteerForm
@login_required
def volunteer(request):
    ''' Add a new volunteer '''
    profile = profileOrRedirect(request.user)

    if request.method == 'POST':
        form = VolunteerForm(request.POST)

        if form.is_valid():
            new_volunteer = form.save(commit=False)
            new_volunteer.user = request.user.get_profile()
            new_volunteer.date = datetime.date.today()
            new_volunteer.save()

            if request.path == '/records/apply/volunteer/':
                return HttpResponseRedirect('/records/apply/complete/')

            else:
                return HttpResponseRedirect('/')

    else:
        form = VolunteerForm()

    context = {'form':form, 'profile':profile}
    addToContext(profile, context)
    return render_to_response('records/volunteer.html', context, context_instance=RequestContext(request))

@login_required
def changeVol(request, id):
    ''' Change an existing volunteer '''
    profile = profileOrRedirect(request.user)

    try:
        volunteer = Volunteer.objects.get(user=profile, id=id)

    except:
        return HttpResponseRedirect('/records/')

    if request.method == 'POST':
        form = VolunteerForm(request.POST, instance=volunteer)

        if form.is_valid():
            vol = form.save(commit=False)
            vol.date = datetime.date.today()
            vol.save()
            return HttpResponseRedirect('/records/')

    else:
        form = VolunteerForm(instance=volunteer)

    context = {'form':form, 'profile':profile}
    addToContext(profile, context)
    return render_to_response('records/changeVol.html', context, context_instance=RequestContext(request))

@login_required
def changeStudent(request, id):
    ''' Change an existing student (intro phase only) '''
    profile = profileOrRedirect(request.user)

    try:
        student = Student.objects.get(user=profile, id=id)

    except:
        return HttpResponseRedirect('/records/')

    if request.method == 'POST':
        form = StudentAddForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/records/')

    else:
        form = StudentAddForm(instance=student)

    context = {'form':form, 'profile':profile,}
    addToContext(profile, context)
    return render_to_response('records/changeStudent.html', context, context_instance=RequestContext(request))

from records.forms import EmergencyContactsForm
@login_required
def ecf(request):
    ''' Add/change Emergency Contact Info '''
    try:
        profile = request.user.get_profile()
    except:
        return HttpResponseRedirect('/records/profile/')

    try:
        ec = EmergencyContacts.objects.get(user=profile)
        if request.method == 'POST':
              form = EmergencyContactsForm(request.POST, instance=ec)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/records/')
        else:
            form = EmergencyContactsForm(instance=ec)

    except:
        if request.method == 'POST':
            form = EmergencyContactsForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = profile
                instance.save()
                return HttpResponseRedirect('/records/')
        else:
            form = EmergencyContactsForm()

    context = {'form':form, 'profile': profile,}
    addToContext(profile, context)
    return render_to_response('records/emergency.html', context, context_instance=RequestContext(request))

from records.forms import ProfileForm
@login_required
def profile(request):
    ''' Add/change UserProfile '''
    if request.method == 'POST':
        try:
            profile = UserProfile.objects.get(user=request.user)
            form = ProfileForm(request.POST, instance=profile)

            if form.is_valid():
                form.save()
                if request.path == '/records/apply/profile/':
                    return HttpResponseRedirect('/records/apply/')
                else:
                    return HttpResponseRedirect('/records/') #should probably go to generic success

        except:
            form = ProfileForm(request.POST)

            if form.is_valid():
                new_profile = form.save(commit=False)
                new_profile.user = request.user
                new_profile.has_completed_profile = True
                form.save()
                if request.path == '/records/apply/profile/':
                    return HttpResponseRedirect('/records/apply/')
                else:
                    return HttpResponseRedirect('/records/')

    else:
        try:
            profile = request.user.get_profile() # alternate form of the above try:
            form = ProfileForm(instance=profile)
            students = Student.objects.filter(user=profile)
            volunteers = Volunteer.objects.filter(user=profile)
        except:
            form = ProfileForm()
            profile = []
            volunteers = []
            students = []

    context = {'form':form, 'profile': profile, 'path':request.path, 'students':students, 'volunteers':volunteers}
    return render_to_response('records/profile.html', context, context_instance=RequestContext(request))

#from records.forms import PickUpForm
from django.forms.models import inlineformset_factory
@login_required
def pickup(request):
    ''' Add/change AuthorizedPickUpPeople '''
    try:
        profile = request.user.get_profile()
    except:
        return HttpResponseRedirect('/records/profile/')

    PickUpFormSet = inlineformset_factory(UserProfile, AuthorizedPickUpPerson, extra=5, max_num=4, fields=('name', 'relationship', 'phone'))
    if request.method == "POST":
        formset = PickUpFormSet(request.POST, instance=profile )
        if formset.is_valid():
            instances = formset.save()
            return HttpResponseRedirect('/records/')

    else:
        formset = PickUpFormSet(instance=profile, )
        
    context = {'formset':formset, 'profile':profile,}
    addToContext(profile, context)
    return render_to_response('records/pickup.html', context, context_instance=RequestContext(request))    

@login_required
def family(request):
    ''' Add/change family members '''
    try:
        profile = request.user.get_profile()

    except:
        return HttpResponseRedirect('/records/profile/')

    FamilyFormSet = inlineformset_factory(UserProfile, FamilyMember, extra=10, max_num=10, fields=('name', 'street_address', 'city', 'state', 'zip','relationship', 'phone', 'email',))

    if request.method == 'POST':
        formset = FamilyFormSet(request.POST, instance=profile)

        if formset.is_valid():
            instances = formset.save()
            if request.path == '/records/apply/family/':
                return HttpResponseRedirect('/records/apply/complete/')
            else:
                return HttpResponseRedirect('/records/')

    else:
        formset = FamilyFormSet(instance=profile )

    context = {'formset':formset, 'profile':profile, }
    addToContext(profile, context)
    return render_to_response('records/family.html', context, context_instance=RequestContext(request))

@login_required
def guardians(request):
    ''' Add/change guardian information '''
    try:
        profile = request.user.get_profile()

    except:
        return HttpResponseRedirect('/records/profile/')

    GuardianFormSet = inlineformset_factory(UserProfile, Guardian, extra=3, max_num=2, )

    if request.method == 'POST':
        formset = GuardianFormSet(request.POST, instance=profile )

        if formset.is_valid():
            instances = formset.save(commit=False)

            for instance in instances:
                instance.user = profile
                instance.save()

            if request.path == '/records/apply/guardians/':
                return HttpResponseRedirect('/records/apply/complete/')
            else:
                return HttpResponseRedirect('/records/')

    else:
        formset = GuardianFormSet(instance=profile )

    context = {'profile':profile, 'formset':formset, }
    addToContext(profile, context)
    return render_to_response('records/guardians.html', context, context_instance=RequestContext(request))

from records.forms import StudentApplyForm
@login_required
def apply(request):
    ''' Add new Student/Application-front-end '''
    try:
        profile = request.user.get_profile()

    except:
        return HttpResponseRedirect('/records/apply/profile/')

    if request.method == 'POST':
        form = StudentApplyForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)

            try:
                student = Student.objects.filter(user=profile).filter(last=instance.last).get(first=instance.first)
                return HttpResponseRedirect('/records/apply/questions/%s' % student.id)

            except:        
                 instance.user = profile
                student = instance.save()
                return HttpResponseRedirect('/records/apply/questions/%s' % instance.id)

    else:
        form = StudentApplyForm()
            
    context = {'profile':profile, 'form':form}
    return render_to_response('records/apply.html', context, context_instance=RequestContext(request))

from records.forms import StudentAddForm
@login_required
def addStudent(request):
    ''' Add new Student (intro-phase only) '''
    try:
        profile = request.user.get_profile()
    except:
        return HttpResponseRedirect('/records/profile/')

    if request.method == 'POST':
        form = StudentAddForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = profile
            instance.save()
            return HttpResponseRedirect('/records/')

    else:
        form = StudentAddForm()

    context = {'profile':profile, 'form':form }
    addToContext(profile, context)
    return render_to_response('records/addStudent.html', context, context_instance=RequestContext(request))

@login_required
def register(request):
    ''' see your students and whether or not they have completed
    the registration '''
    profile = profileOrRedirect(request.user)
    students_complete = Student.objects.filter(user=profile,\
            registration_complete=True)
    students_left = Student.objects.filter(user=profile,\
            registration_complete=False)
    context = {
            'students_complete': students_complete,\
            'students_left': students_left,\
            }
    return render_to_response('records/register.html', context,\
            context_instance=RequestContext(request))

def registerStudent(request, id):
    ''' base of the trail for an individual student to go through
    the registration process '''
    try:
        student = Student.objects.get(id=id)
    except:
        return HttpResponseRedirect('/records/') # get out!

    context = {'student':student,}
    return render_to_response('records/registerStudent.html', context,\
            context_instance=RequestContext(request))

@login_required
def enroll(request):
    ''' See available students and whether or not they are enrolled
    for the upcoming year '''
    try:
        profile = request.user.get_profile()
    except:
        return HttpResponseRedirect(no_profile_redirect)
    students= Student.objects.filter(user=profile, student_accepted=True)
    context = {'students':students}
    return render_to_response('records/enroll.html', context,\
            context_instance=RequestContext(request))

def enrollStudent(request):
    ''' should be able to handle this with a single page'''
    context = {}
    return render_to_response('records/enrollStudent.html', context,\
            context_instance=RequestContext(request))

from records.forms import MSSQForm
@login_required
def mssq(request, id):
    ''' Part of the application for the older students '''
    try:
        student = Student.objects.get(user=request.user.get_profile, id=id)
    except:
        return HttpResponseRedirect('/records/')
    try:
        application = Application.objects.get(student=student)
    except:
        return HttpResponseRedirect('/records/apply/questions/%s' % id)
    try:
        mssq = MiddleSchoolStudentQuestionnaire.objects.get(application=application)
        return HttpResponseRedirect('/records/apply/questions/parent/%s' % id)

    except:

        if request.method == 'POST':
            form = MSSQForm(request.POST)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.application = application
                instance.save()
                return HttpResponseRedirect('/records/apply/questions/parent/%s' % id)

        else:
            form = MSSQForm()

    context = {'student':student,'application':application, 'form':form}
    return render_to_response('records/mssq.html', context, context_instance=RequestContext(request))

from records.forms import ApplicationForm
@login_required
def questions(request, id):
    ''' I think that these are the basic questions about the student '''
    try:
        profile = request.user.get_profile()

    except:
        return HttpResponseRedirect('/records/apply/profile/')

    try:
        student = Student.objects.get(user=profile, id=id)

    except:
        return HttpResponseRedirect('/records/apply/')

    try:
        application = Application.objects.get(student=student)
        return HttpResponseRedirect('/records/apply/questions/parent/%s' % id)

    except:

        if profile == UserProfile.objects.get(student__id=id):

            if request.method == 'POST':
                   form = ApplicationForm(request.POST)
            
                if form.is_valid():

                    instance = form.save(commit=False)
                    instance.student = student
                    instance.user = profile
                    instance.save()
                    
                    if student.next_grade in ('6', '7', '8'):
                        return HttpResponseRedirect('/records/apply/questions/mssq/%s' % id)
                
                    if instance.entering_6th_7th_or_8th:
                        return HttpResponseRedirect('/records/apply/questions/mssq/%s' % id)

                    else:
                        return HttpResponseRedirect('/records/apply/questions/parent/%s' % id)

               else:
                form = ApplicationForm()

        else:
            return HttpResponseRedirect('/records/')

    context = {'profile':profile, 'form':form, 'student':student, }
    return render_to_response('records/questions.html', context, context_instance=RequestContext(request))

from records.forms import ParentForm
@login_required
def parent(request,id):
    try:
        profile = request.user.get_profile()

    except:
        return HttpResponseRedirect('/records/apply/profile/')

    try:
        student = Student.objects.get(user=profile, id = id )

    except:
        return HttpResponseRedirect('/records/apply/')

    try:
        application = Application.objects.get(student=student)

    except:
        return HttpResponseRedirect('/records/apply/questions/%s' % id )

    try:
        parent_part = ParentPart.objects.get(application=application)
        return HttpResponseRedirect('/records/apply/current/%s' %id )

    except:
        if profile == UserProfile.objects.get(student__id=id):

            if request.method == 'POST':
                form = ParentForm(request.POST)

                if form.is_valid():

                    instance = form.save(commit=False)
                    instance.application = application
                    instance.save()

                    return HttpResponseRedirect('/records/apply/current/%s' % id)

            else:
                form = ParentForm()

        else:
            return HttpResponseRedirect('/records/')

    context = {'student':student, 'application':application, 'form':form, }
    return render_to_response('records/parent.html', context, context_instance=RequestContext(request))

from records.forms import CurrentSchoolForm
@login_required
def current(request, id):
    try:
        profile = request.user.get_profile()

    except:
        return HttpResponseRedirect('/records/apply/profile/')

    try:
        student = Student.objects.get(user=profile, id=id)

    except:
        return HttpResponseRedirect('/records/apply/')

    try:
        application = Application.objects.get(student=student)
    except:
        return HttpResponseRedirect('/records/apply/questions/%s' % id)

    try:
        parentpart = ParentPart.objects.get(application=application)

    except:
        return HttpResponseRedirect('/records/apply/questions/parent/%s' % id)

    try:
        current = CurrentSchool.objects.get(application=application)
        return HttpResponseRedirect('/records/apply/complete/%s' % id)

    except:
        if request.method == 'POST':
            form = CurrentSchoolForm(request.POST)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.application = application
                instance.save()
                return HttpResponseRedirect('/records/apply/complete/%s' % id )

        else:
            form = CurrentSchoolForm()

    context = {'form':form, 'student': student, 'application': application}
    return render_to_response('records/current.html', context, context_instance=RequestContext(request))

@login_required
def appcomplete(request, id):
    try:
        profile = request.user.get_profile()
    except:
        return HttpResponseRedirect('/records/apply/profile/')
    try:
        student = Student.objects.get(user=profile, id=id)
    except:
        return HttpResponseRedirect('/records/apply/')
    try:
        application = Application.objects.get(student=student)
    except:
        return HttpResponseRedirect('/records/apply/questions/%s' % id)
    if student.next_grade in ('6','7','8') or application.entering_6th_7th_or_8th:
        try:
            mssq = MiddleSchoolStudentQuestionnaire.objects.get(application=application)
            student.student_interview_complete = True
            student.save()
        except:
            return HttpResponseRedirect('/records/apply/questions/mssq/%s' % id)
    try:
        current_school = CurrentSchool.objects.get(application=application)
    except:
        return HttpResponseRedirect('/records/apply/current/%s' % id)

    guardians = Guardian.objects.filter(user=profile)
    
    if guardians.count() == 0:
        return HttpResponseRedirect('/records/apply/guardians/')

    family = FamilyMember.objects.filter(user=profile)

    if family.count() == 0:
        return HttpResponseRedirect('/records/apply/family/')

    volunteers = Volunteer.objects.filter(user=profile)

    if volunteers.count() == 0:
        return HttpResponseRedirect('/records/apply/volunteer/')

    student.application_form_complete = True
    student.application_form_completed_on = datetime.date.today()
    student.save()

    context = {'student':student, 'application':application, }
    return render_to_response('records/complete.html', context, context_instance=RequestContext(request))

@login_required
def appcontinue(request):
    try:
        profile = request.user.get_profile()
    except:
        return HttpResponseRedirect('/records/apply/profile/')

    students_uncomplete = Student.objects.filter(user=profile).filter(application_form_complete=False)
    students_complete = Student.objects.filter(user=profile).filter(application_form_complete=True)
    context = {'uncomplete':students_uncomplete, 'complete':students_complete, }
    return render_to_response('records/continue.html', context, context_instance=RequestContext(request))




from django.core.xheaders import populate_xheaders
from django.http import HttpResponse
from django.db.models import get_model
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
def print_detail(request, app_label, model_name, pk, template_name=None,
        template_name_field=None,\
        template_loader=loader, extra_context=None,\
        context_processors=None, template_object_name='object',\
        mimetype=None):
    """
    Put the following line in your urls.py BEFORE your admin include
    (r'^admin/(?P<app_label>[\d\w]+)/(?P<model_name>[\d\w]+)/(?P<pk>[\d]+)/print/', 'biola.utils.print_view.print_detail'),

    Generic detail of an object.

    Templates: ``<app_label>/<model_name>_print_detail.html``
    Context:
        object
            the object
    """
    if not request.user.is_staff:
        return HttpResponseForbidden()
    if extra_context is None: extra_context = {}
    try:
        model = get_model(app_label, model_name)
        obj = model.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404, "No %s found matching the query" % (model._meta.verbose_name)
    if not template_name:
        template_name = "admin/%s/%s_print_detail.html" % (model._meta.app_label, model._meta.object_name.lower())
    if template_name_field:
        template_name_list = [getattr(obj, template_name_field), template_name]
        t = template_loader.select_template(template_name_list)
    else:
        t = template_loader.get_template(template_name)
    if model_name == 'application':
        try:
            pp = ParentPart.objects.get(application = obj)
        except:
            pp = []

    c = RequestContext(request, {
        template_object_name: obj,
        'pp':pp,
    }, context_processors)
    for key, value in extra_context.items():
        if callable(value):
            c[key] = value()
        else:
            c[key] = value
    response = HttpResponse(t.render(c), mimetype=mimetype)
    populate_xheaders(request, response, model, getattr(obj, obj._meta.pk.name))
    return response

