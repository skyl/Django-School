import csv
from django.http import HttpResponse, HttpResponseForbidden
from django.template.defaultfilters import slugify
from django.db.models.loading import get_model

def export(qs, fields=None):
    model = qs.model
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % slugify(model.__name__)
    writer = csv.writer(response)
    # Write headers to CSV file
    if fields:
        headers = fields
    else:
        headers = []
        for field in model._meta.fields:
            headers.append(field.name)
    writer.writerow(headers)
    # Write data to CSV file
    for obj in qs:
        row = []
        for field in headers:
            if field in headers:
                val = getattr(obj, field)
                if callable(val):
                    val = val()
                row.append(val)
        writer.writerow(row)
    # Return CSV file to browser as download
    return response

def admin_list_export(request, model_name, app_label, queryset=None, fields=None, list_display=True):
    """
    Put the following line in your urls.py BEFORE your admin include
    (r'^admin/(?P<app_label>[\d\w]+)/(?P<model_name>[\d\w]+)/csv/', 'util.csv_view.admin_list_export'),
    """
    if not request.user.is_staff:
        return HttpResponseForbidden()
    if not queryset:
        model = get_model(app_label, model_name)
        queryset = model.objects.all()
        filters = dict()
        for key, value in request.GET.items():
            if key not in ('ot', 'o'):
                filters[str(key)] = str(value)
        if len(filters):
            queryset = queryset.filter(**filters)

    if not fields and list_display:
        from django.contrib import admin
        ld = admin.site._registry[queryset.model].list_display
        if ld and len(ld) > 0:
            fields = ld

    '''
    if not fields:
        if list_display and len(queryset.model._meta.admin.list_display) > 1:
            fields = queryset.model._meta.admin.list_display
        else:
            fields = None
    '''
    return export(queryset, fields)
    """
    Create your own change_list.html for your admin view and put something like this in it:
    {% block object-tools %}
    <ul class="object-tools">
        <li><a href="csv/{%if request.GET%}?{{request.GET.urlencode}}{%endif%}" class="addlink">Export to CSV</a></li>
    {% if has_add_permission %}
        <li><a href="add/{% if is_popup %}?_popup=1{% endif %}" class="addlink">{% blocktrans with cl.opts.verbose_name|escape as name %}Add {{ name }}{% endblocktrans %}</a></li>
    {% endif %}
    </ul>
    {% endblock %}
    """
import datetime
from django.http import HttpResponseRedirect  #, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.decorators import login_required

def mail(request, app_label, model_name):
    context = { 'app_label':app_label, 'model_name':model_name, }
    return render_to_response('mail.html', context, context_instance=RequestContext(request))

