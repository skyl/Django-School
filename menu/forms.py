from django.forms import ModelForm

from menu.models import Meal, Lunch, Order

class ChickOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ('nuggets', 'sandwiches')

class PizzaOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ('cheese', 'pepperoni', )

class HotOrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ('lunch', 'student', 'nuggets','sandwiches', 'cheese', 'pepperoni', 'hot_lunch', 'paid')
