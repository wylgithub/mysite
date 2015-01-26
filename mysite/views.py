from cStringIO import StringIO
from celery import canvas
__author__ = 'wyl'
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.template import Context
from django.template.loader import get_template

from django.http import HttpResponse
import datetime
from books.models import Publisher
from django.http import Http404

import csv

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

# 日期：2015.1.26DJANGO的十三章训练

def my_image(request):
    image_data = open("/home/wyl/test/test1.png", "rb").read()
    return HttpResponse(image_data, mimetype="image/png")


# Number of unruly passengers each year 1995 - 2005. In a real application
# this would likely come from a database or some other back-end data store.
UNRULY_PASSENGERS = [146,184,235,200,226,251,299,273,281,304,203]


def unruly_passengers_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=unruly.csv'

    # Create the CSV writer using the HttpResponse as the "file."
    writer = csv.writer(response)
    writer.writerow(['Year', 'Unruly Airline Passengers'])
    for (year, num) in zip(range(1995, 2006), UNRULY_PASSENGERS):
        writer.writerow([year, num])

    return response


# 和 CSV 类似，由 Django 动态生成 PDF 文件很简单，因为 ReportLab API 同样可以使用类似文件对象。

def hello_pdf(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    # application/pdf告诉浏览器这是一个pdf文档
    # 使用 ReportLab 的 API 很简单： 只需要将 response 对象作为 canvas.Canvas 的第一个参数传入。
    # 所有后续的 PDF 生成方法需要由 PDF 对象调用（在本例中是 p ），而不是 response 对象。
    #最后需要对 PDF 文件调用 showPage() 和 save() 方法（否则你会得到一个损坏的 PDF 文件）。
    #
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=hello.pdf'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response

# 下面是使用 cStringIO 重写的 Hello World 例子：


def hello_pdf(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=hello.pdf'

    temp = StringIO()
    # Create the PDF object, using the StringIO object as its "file."
    p = canvas.Canvas(temp)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the StringIO buffer and write it to the response.
    response.write(temp.getvalue())
    return response


