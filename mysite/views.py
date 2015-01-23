__author__ = 'wyl'

from django.template import loader, RequestContext, TemplateDoesNotExist
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.template import Context,Template
from django.template.loader import get_template

from django.http import HttpResponse
import datetime
from books.models import Publisher
from django.http import Http404
from django.template import TemplateDoesNotExist

def printInfo(request):
    info = Publisher.objects.all().order_by('city')

    return render_to_response('showdb_info.html', {
        'info': info,
        'total_count': len(info),
    })


def hello(request):
    return HttpResponse("Hello world")


def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))




def current_datetime(request):
    now = datetime.datetime.now()
    t = get_template('current_datetime.html')
    html = t.render(Context({'current_datetime': now}))
    return HttpResponse(html)


def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)


def custom_proc(request):
    "A context processor that provides 'app', 'user' and 'ip_address'."
    return {
        'app': 'My app',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR']
    }


def view_1(request):
    # ...
    return render_to_response('template1.html',
        {'message': 'I am view 1.'},
        context_instance=RequestContext(request, processors=[custom_proc]))


def view_2(request):

    return render_to_response('template2.html',
        {'message': 'I am the second view.'},
        context_instance=RequestContext(request, processors=[custom_proc]))

# def about_pages(request, page):
#     try:
#         return direct_to_template(request, template="about/%s.html" % page)
#     except TemplateDoesNotExist:
#         raise Http404()

#
# def author_detail(request, author_id):
#     # Delegate to the generic view and get an HttpResponse.
#     response = Publisher.object_detail(
#         request,
#         queryset = Publisher.objects.all(),
#         object_id = author_id,
#     )
#      now = datetime.datetime.now()
#     Publisher.objects.filter(id=author_id).update(last_accessed=now)
#
#     return response