from django import template
register = template.Library()

@register.filter
def EQ(value,arg): return value == arg

@register.filter
def LT(value,arg): return value < arg

@register.filter
def GT(value,arg): return value > arg

@register.filter
def LE(value,arg): return value <= arg

@register.filter
def GE(value,arg): return value >= arg

@register.filter
def NE(value,arg): return value != arg

@register.filter
def IS(value,arg): return value is arg

@register.filter
def IN(value,arg): return value in arg

