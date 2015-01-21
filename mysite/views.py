from django.template import loader, RequestContext
from django.shortcuts import render_to_response
from django.template import RequestContext


__author__ = 'wyl'

from django.template import Context,Template
from django.template.loader import get_template

from django.http import Http404, HttpResponse
import datetime

def hello(request):
    return HttpResponse("Hello world")

# def current_datetime.html(request):
#     now = datetime.datetime.now()
#     html = "<html><body>It is now %s.</body></html>" % now
#     return HttpResponse(html)

# def current_datetime.html(request):
#     now = datetime.datetime.now()
#     t = Template("<html><body>It is now {{ current_date }}.</body></html>")
#     html = t.render(Context({'current_date': now}))
#     return HttpResponse(html)


# def current_datetime.html(request):
#     now = datetime.datetime.now()
#     # Simple way of using templates from the filesystem.
#     # This is BAD because it doesn't account for missing files!
#     fp = open('/home/djangouser/templates/mytemplate.html')
#     t = Template(fp.read())
#     fp.close()
#     html = t.render(Context({'current_date': now}))
#     return HttpResponse(html)

# test1
def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))


# # test2
# def search_form(request):
#     return render_to_response('search_form.html')


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

# date:2015.1.20
# def view_1(request):
#     t = loader.get_template('template1.html')
#     c = Context({
#         'app': 'My app',
#         'user': request.user,
#         'ip_address': request.META['REMOTE_ADDR'],
#         'message': 'I am view 1.'
#         })
#     return t.render(c)
#
#
# def view_2(request):
#     # ...
#     t = loader.get_template('template2.html')
#     c = Context({
#         'app': 'My app',
#         'user': request.user,
#         'ip_address': request.META['REMOTE_ADDR'],
#         'message': 'I am the second view.'
#     })
#     return t.render(c)
#
#
#

#
# def custom_proc(request):
#     "A context processor that provides 'app', 'user' and 'ip_address'."
#     return {
#         'app': 'My app',
#         'user': request.user,
#         'ip_address': request.META['REMOTE_ADDR']
#     }
#
#
# def view_1(request):
#     # ...
#     t = loader.get_template('template1.html')
#     c = RequestContext(request, {'message': 'I am view 1.'},
#             processors = [custom_proc])
#     return t.render(c)
#
#
# def view_2(request):
#     # ...
#     t = loader.get_template('template2.html')
#     c = RequestContext(request, {'message': 'I am the second view.'},
#             processors = [custom_proc])
#     return t.render(c)


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
    # ...
    return render_to_response('template2.html',
        {'message': 'I am the second view.'},
        context_instance=RequestContext(request, processors=[custom_proc]))