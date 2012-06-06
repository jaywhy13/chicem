from django.http import HttpResponse
from django.shortcuts import render_to_response
from graves.models import Grave, CemeteryBoundary
from django.conf import settings


def data(request):
    """ returns the data settings in XML for ammap (graves and areas)
    """
    graves = Grave.objects.all()
    boundaries = CemeteryBoundary.objects.all()
    swf_location = "ammap.swf"
    return render_to_response("graves/data.xml", locals())


def search(request, query):
    try:
        plot_no = int(query)
        graves = Grave.objects.filter(plot__contains=plot_no)
    except:
        graves = Grave.objects.filter(name__icontains=query)
    return render_to_response("graves/list.html", locals())

