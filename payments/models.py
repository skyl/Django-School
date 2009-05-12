from django.db import models

from django.contrib import admin

from constants import payment_types

class Payment(models.Model):
    from records.models import UserProfile
    profile = models.ForeignKey(UserProfile)
    item_name = models.CharField(max_length=50, choices=payment_types)
    item_number = models.PositiveIntegerField()
    mc_gross = models.DecimalField(max_digits=4, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s, %s, $%.2f on %s" % (self.profile, self.item_name,
                self.mc_gross, self.timestamp.strftime("%B %d, %Y"))

class PaymentAdmin(admin.ModelAdmin):
    list_filter = ['item_name',]
    date_hierarchy = 'timestamp'
    search_fields = ['profile', 'item_name', 'profile__student__first',\
            'profile__student__last', 'profile__student__preferred_name',]

admin.site.register(Payment, PaymentAdmin)
