from django.contrib import admin
from records.models import Student, UserProfile, Application, DisciplinaryAction, ParentPart, MiddleSchoolStudentQuestionnaire, CurrentSchool, Enrollment

from people.models import FamilyMember, AuthorizedPickUpPerson, Guardian, Volunteer, EmergencyContacts



class GuardianInline(admin.TabularInline):
    model = Guardian
    extra = 1

class StudentInline(admin.TabularInline):
    model = Student
    extra = 1

class FamilyMemberInline(admin.TabularInline):
    model = FamilyMember
    extra = 1

class AuthorizedPickUpPersonInline(admin.TabularInline):
    model = AuthorizedPickUpPerson
    extra = 1

class EmergencyContactsInline(admin.StackedInline):
    model = EmergencyContacts

class VolunteerInline(admin.TabularInline):
    model = Volunteer
    extra = 1

class UserProfileAdmin(admin.ModelAdmin):
    save_on_top=True
    list_display = ('addressee','primary_phone', 'email', 'street_address', 'city', 'state', 'zip',)#'guardians', 'students')
    search_fields = ['addressee', 'student__last','student__first', 'student__preferred_name',]
    inlines = [GuardianInline, StudentInline, FamilyMemberInline, VolunteerInline, AuthorizedPickUpPersonInline, EmergencyContactsInline, ]

class DisciplinaryActionInline(admin.TabularInline):
    model = DisciplinaryAction
    extra = 1 

class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1

#class ApplicationInline(admin.StackedInline):
#    model = Application
from menu.models import Voucher
class VoucherInline(admin.TabularInline):
    model = Voucher


class StudentAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Vitals', {
            'classes': ('collapse',),
            'fields': ('user', 'first', 'middle', 'last', 'preferred_name', 
                                'present_grade','next_grade','date_of_birth','gender', 'living_with',
                                'changes_affect', )
        }),
        ('Allergies', {
            'classes': ('collapse',),
            'fields': ('allergies', 'allergy_description',)
        }),
        ('Application', {
            'classes': ('collapse',),
            'fields': (('application_form_completed_on', 'application_form_complete'),
                        ('application_payment_completed_on', 'application_payment_complete'),
                        ('entrance_testing_scheduled_for','entrance_testing_complete'),
                        ('parent_interview_scheduled_for','parent_interview_complete'),
                        ('student_interview_scheduled_for','student_interview_complete'),
                        ('decision_made','student_accepted')   ) 
        }),
        ('Registration', {
            'classes': ('collapse',),
            'fields': ( 
                ('registration_signed_paid_on','registration_signed_paid',),
                ('complete_documents_on', 'complete_documents'),
                ('custody_decision_received_on', 'custody_decision_received', ),
                ('birth_certificate_received_on', 'birth_certificate_received'),
                ('immunization_record_received_on', 'immunization_record_received'),
                ('emergency_medical_card_received_on', 'emergency_medical_card_received'),
                'payment_plan',
                'registration_complete',
            )
        }),
        ('Status', {
            'classes': ('collapse',),
            'fields': (
                'currently_student', 'enrolled_for_upcoming_year', 'alumni', 
            )

        }),

    )


    list_display = ('__unicode__',  'present_grade', 'date_of_birth', 'gender','guardians', )
    search_fields = ['last', 'first', 'middle', 'preferred_name',  ]
    list_filter = ['currently_student', 'present_grade', 'enrolled_for_upcoming_year','gender', 'living_with', 
    ##application
        'application_form_complete', 'entrance_testing_complete', 'parent_interview_complete', 
        'student_accepted', 
    ##registration
        'registration_signed_paid', 'complete_documents', 'custody_decision_received', 
        'birth_certificate_received', 'immunization_record_received', 
        'emergency_medical_card_received', 'registration_complete',
    ##enrollment
        'enrolled_for_upcoming_year','payment_plan',]
    inlines = [EnrollmentInline, DisciplinaryActionInline, VoucherInline]


class ParentPartInline(admin.StackedInline):
    model = ParentPart

class CurrentSchoolInline(admin.StackedInline):
    model = CurrentSchool

class MSSQInline(admin.StackedInline):
    model = MiddleSchoolStudentQuestionnaire

class ApplicationAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, { 'fields': ('student',),}),
        
        ('Questionnaire', {
            'classes': ('collapse',),
            'fields': ('scholastic_difficulties','learning_differences', 'special_education', 'extended_absences', 
                    'physical_emotional', 'reason_to_not_attend', 'if_yes_explain', 'interests_skills_hobbies', 
                    'why_enroll', 'why_change_school', 'hope_to_benefit', 'entering_6th_7th_or_8th',
                    'signed',
                    'dated', )
        }),
    )
    inlines = [ParentPartInline, CurrentSchoolInline, MSSQInline]


class GuardianAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'primary_phone', 'email', 'students', 'title', 'church', )
    search_fields = ['first', 'last', 'employer', 'primary_phone','user__student__preferred_name', 'user__student__first', 'user__student__last', ]
    list_filter = ['relationship',]
    inlines = []

class AuthorizedPickUpPersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'students', 'relationship', 'phone',)
    search_fields = ['name', 'user__student__preferred_name', 'user__student__last', 'user__student__first', 'phone',]
#    list_filter = ['user__student__present_grade']
# To get the "pickup people list for each grade" view I think that we would have to write custom views.

class FamilyMemberAdmin(admin.ModelAdmin):
    search_fields = ['name', 'user__student__present_grade','user__student__preferred_name', 'user__student__last', 'user__addressee',]
    list_display = ['name', 'relationship', 'phone',
            'email',  
            'street_address',
            'city', 
            'state', 
            'zip', 'students',
    ]
    list_filter = ['relationship',]

class VolunteerAdmin(admin.ModelAdmin):
    search_fields = ['name', 'user__addressee', 'user__student__preferred_name', 'user__student__present_grade']
    list_display = ['name', 'phone_number','email', 'associated_household']
    list_filter = [
        'classroom',
        'campus', 
        'academic', 
        'music', 
        'library', 
        'art', 
        'yearbook', 
        'office', 
        'fundraising',
        'maintenance', 
        'resources', ] 
    fieldsets = (
        (None, { 'fields':('user', 'name', 'phone_number', 'date',)}),
        ('Categories', { 
                                    'classes': ('collapse',),
                                'fields': ('classroom', 'campus',
                                    'academic', 'music',
                                        'library',
                                    'art', 
                                    'yearbook', 
                                    'office', 
                                    'fundraising', 
                                    'maintenance',),}),
        ('Classroom', {
                                'classes':('collapse',),
                                'fields': ('grade_papers',
                                    'drive_for_trips',
                                    'plan_supervise_trips',
                                    'coordinate_class',
                                    'tutor_under',
                                    'substitute_short',
                                    'refreshments',
                                    'other_classroom',)}),
        ('Campus', {
                                'classes':('collapse',),                
                                'fields': ('supervise_playground',
                                    'supervise_lunch',
                                    'before_after_substitute',
                                    'assist_PE',
                                    'provide_lunch_breaks_for_staff',
                                    'other_campus',)}),
        ('Academic', {
                                'classes':('collapse',),                
                                'fields': ('substitute',
                                    'aide',
                                    'teach_expertise',
                                    'tutor',
                                    'judge_meet',
                                    'other_academic',)}),
        ('Music', {
                                'classes':('collapse',),                
                                'fields': ('piano',
                                    'assist_performance',
                                    'event_transport',
                                    'other_music',)}),
        ('Library', {
                                'classes':('collapse',),                
                                'fields': ('check_out',
                                    'proofread',
                                    'process',
                                    'shelve',
                                    'maintain',
                                    'other_library',)}),
        ('Arts', {
                                'classes':('collapse',),                
                                'fields': ('bulletin_boards',
                                    'backdrops',
                                    'graphic_artist',
                                    'judge_festival',
                                    'decorations',
                                    'art_teach_assist',
                                    'art_class_helper',
                                    'other_arts',)}),

        ('Yearbook', {
                                'classes':('collapse',),                
                                'fields': ('photography',
                                    'advertising',
                                    'layout',
                                    'supervise_students',
                                    'other_yearbook',)}),
        ('Office', {
                                'classes':('collapse',),                
                                'fields': ('substitute_secretary',
                                    'provide_secretary_breaks',
                                    'help_with_mailings',
                                    'general_office',
                                    'phone',
                                    'word_processing',
                                    'work_at_home',
                                    'other_office',)}),
        ('Fundraising', {
                                'classes':('collapse',),                
                                'fields': ('jogathon',
                                    'auction',
                                    'prizes_sponsors',
                                    'grant_proposal',
                                    'financial_consulting',
                                    'annual_banquet',
                                    'recruit_donors',
                                    'other_fundraising',)}),

        ('Maintenance', {
                                'classes':('collapse',),                
                                'fields': ('landscape',
                                    'painting',
                                    'lend_large_vehicle',
                                    'carpentry',
                                    'cleaning',
                                    'handyman',
                                    'communications_network',
                                    'other_maintenance',)}),
        ('Resources', {
                                'classes':('collapse',),                
                                'fields': ('business_equipment',
                                    'construction',
                                    'legal_services',
                                    'accounting',
                                    'other_resources',)}),


    )

    #'grade_papers', 'drive_for_trips', 'plan_supervise_trips',
    #                   'coordinate_class', 'tutor_under', 'substitute_short', 'refreshments',]

class EmergencyContactsAdmin(admin.ModelAdmin):
    list_display = ['user', 'students', 'contact1', 'phone1', 'contact2', 'phone2', 'doctor', 'doctor_phone',]
    search_fields = ['user__student__preferred_name', 'user__addressee','contact1', 'contact2', 'doctor', 'user__student__last', 'user__student__first']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Guardian, GuardianAdmin)
admin.site.register(AuthorizedPickUpPerson, AuthorizedPickUpPersonAdmin)
admin.site.register(FamilyMember, FamilyMemberAdmin)
admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(MiddleSchoolStudentQuestionnaire)
admin.site.register(Enrollment)
admin.site.register(EmergencyContacts, EmergencyContactsAdmin)

from years.models import Homeroom, SchoolYear, HomeroomLeader, HomeroomMemberK4, HomeroomK4#, Holiday
#class HomeroomInline(admin.TabularInline):
#    model = Homeroom
#    extra = 10

#class SchoolYearAdmin(admin.ModelAdmin):
#    list_display = ['__unicode__', ]
#    search_fields = ['__unicode__',]
#    list_filter = ['current', 'last', 'next']
#    inlines = ['ClassroomInline']

#class HomeroomAdmin(admin.ModelAdmin):
#    list_display = ['__unicode__', 'students_set',]
#    list_filter = ['year', 'leader', 'grade']
#    search_fields = ['students', 'leader', 'year', 'grade']

class K4memberInline(admin.TabularInline):
    model = HomeroomMemberK4
    extra = 10

class HomeroomK4admin(admin.ModelAdmin):
    inlines = [K4memberInline,]

class SchoolYearAdmin(admin.ModelAdmin):
    fieldsets = (
       ('Important Dates', {
            'classes': ('collapse',),
            'fields': (('first_day_of_school', 'last_day_of_school'),('application_deadline','application_price'),
                ('enroll1','enroll1_price'),
                ('enroll2','enroll2_price'),
                ('enroll3','enroll3_price'),
                ('register1','register1_price'),
                ('register2','register2_price'),            )
        }),
    )
    #    inlines = [HomeroomInline]


admin.site.register(SchoolYear, SchoolYearAdmin)
admin.site.register(HomeroomK4, HomeroomK4admin)
#admin.site.register(Homeroom, HomeroomAdmin)
admin.site.register(HomeroomLeader)
#admin.site.register(Holiday)



