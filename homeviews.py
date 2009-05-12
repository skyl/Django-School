import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext

from menu.models import DateSet
def home(request):
    try:
        menu = DateSet.objects.get(start_taking_orders__lte =\
                datetime.date.today(), end_taking_orders__gte =\
                datetime.date.today())
    except:
        menu = None

    home=True
    try:
        profile = request.user.get_profile()
    except:
        profile=None
    context = {'menu':menu, 'home':home, 'profile':profile,}
    return render_to_response('home.html', context,\
            context_instance=RequestContext(request))

def calendar(request):
    context = {}
    return render_to_response('calendar.html', context,\
            context_instance=RequestContext(request))
