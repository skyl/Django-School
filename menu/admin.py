from django.contrib import admin
from menu.models import Meal, Lunch, Order, Account, DateSet

class LunchInline(admin.TabularInline):
    model = Lunch
    extra = 10

class MealAdmin(admin.ModelAdmin):
    #    list_display = []
    search_fields = ['name', 'description',]
    list_filter = ['type']
    inlines = [LunchInline]

class LunchAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'number','date'] # future
    search_fields = ['meal__name',]
    #    list_filter = ['date']
    date_hierarchy = 'date'

class OrderAdmin(admin.ModelAdmin):
    list_display = ['student', 'lunch','paid']
    #    search_fields =

#class AccountAdmin(admin.ModelAdmin):
#    list_display=['__unicode__','paid', 'total',]

admin.site.register(Meal, MealAdmin)
admin.site.register(Lunch, LunchAdmin)
admin.site.register(Order, OrderAdmin)
#admin.site.register(Account, AccountAdmin)
admin.site.register(DateSet)


