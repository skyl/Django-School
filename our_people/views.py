from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import list_detail
from our_people.models import Person

import datetime
import re

def person_list(request, page=0, **kwargs):
    return list_detail.object_list(request,\
            queryset = Person.objects.filter(featured=True),\
            paginate_by = 20,\
            page = page,\
            **kwargs
    )
person_list.__doc__ = list_detail.object_list.__doc__

def detail(request, id):
    try:
        person = Person.objects.get(id=id)
    except:
        return HttpResponseRedirect('/')
    context = {'person':person, }
    return render_to_response('our_people/detail.html', context,\
            context_instance = RequestContext(request))
