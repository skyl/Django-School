
from django.http import HttpResponse, HttpResponseServerError
import urllib

class Endpoint:

    default_response_text = 'Nothing to see here'
    verify_url = "https://www.paypal.com/cgi-bin/webscr"

    def do_post(self, url, args):
        return urllib.urlopen(url, urllib.urlencode(args)).read()

    def verify(self, data):
        args = {
            'cmd': '_notify-validate',
        }
        args.update(data)
        return self.do_post(self.verify_url, args) == 'VERIFIED'

    def default_response(self):
        return HttpResponse(self.default_response_text)

    def __call__(self, request):
        r = None
        if request.method == 'POST':
            data = dict(request.POST.items())
            # We need to post that BACK to PayPal to confirm it
            if self.verify(data):
                r = self.process(data)
            else:
                r = self.process_invalid(data)
        if r:
            return r
        else:
            return self.default_response()

    def process(self, data):
        id = int(data['item_number'])
        total=float(data['mc_gross'])

        if data['item_name']=='MealPlan':
            import datetime
            from menu.models import Account, Voucher, Order, DateSet, Lunch
            try:
                a = Account.objects.get(id=id)
                if float(a.total_minus_vouchers()) == total\
                        and data['payment_status']=='Completed'\
                        and data['mc_currency']=='USD':
                    a.paid=True
                    a.save()
                    from payments import Payment
                    Payment.create(profile=a.profile, item_name="MealPlan",\
                            item_number=id, mc_gross=total,\
                            timestamp=datetime.datetime.now())

                else:
                    return HttpResponseServerError('data did not jive')

            except:
                return HttpResponseServerError('No Account Found')

            try:
                today = datetime.date.today()
                dateset = DateSet.objects.get(start_taking_orders__lte=today, end_taking_orders__gte=today)
                lunches = Lunch.objects.filter(date__gte=dateset.start, date__lte=dateset.end)
                orders = Order.objects.filter(lunch__in=lunches, student__user=a.profile)
                for o in orders:
                    o.paid=True
                    o.save()

                vouchers = Voucher.objects.filter(student__user=a.profile)
                for v in vouchers:
                    v.delete()

            except:
                return HttpResponseServerError('No DateSet Found')
        else:
            pass

        return HttpResponse("OK")

    def process_invalid(self, data):
        return HttpResponseServerError("Nope")
'''
class AppEngineEndpoint(Endpoint):
    
    def do_post(self, url, args):
        from google.appengine.api import urlfetch
        return urlfetch.fetch(
            url = url,
            method = urlfetch.POST,
            payload = urllib.urlencode(args)
        ).content

####### Here is the alternate endpoint provided at
#######

import urllib
import urllib2

from django.http import HttpResponse, HttpResponseServerError

PP_URL = "https://www.sandbox.paypal.com/cgi-bin/webscr"
#PP_URL = "https://www.paypal.com/cgi-bin/webscr"

def ipn(request):
  parameters = None

  try:
    if request['payment_status'] == 'Completed':
      if request.POST:
        parameters = request.POST.copy()
      else:
        parameters = request.GET.copy()
    else:
      pass
      #log_error("IPN", "The parameter payment_status was not Completed.")

    if parameters:
      parameters['cmd']='_notify-validate'

      params = urllib.urlencode(parameters)
      req = urllib2.Request(PP_URL, params)
      req.add_header("Content-type", "application/x-www-form-urlencoded")
      response = urllib2.urlopen(req)
      status = response.read()
      if not status == "VERIFIED":
        # print "The request could not be verified, check for fraud." + str(status)
        parameters = None

    if parameters:
    #      reference = parameters['txn_id']
    #      invoice_id = parameters['invoice']
    #      currency = parameters['mc_currency']
    #      amount = parameters['mc_gross1']
    #      fee = parameters['mc_fee']
    #      email = parameters['payer_email']
    #      identifier = parameters['payer_id']

      # DO SOMETHING WITH THE PARAMETERS HERE, STORE THEM, ETC...

      return HttpResponse("Ok")

    except Exception, e:
        print "An exeption was caught: " + str(e)

    return HttpResponseServerError("Error")
'''
