from django.http import HttpResponse
from django.shortcuts import render_to_response
from graves.models import Grave, CemeteryBoundary
from django.conf import settings
import json


def data(request, format=None):
    """ returns the data settings in XML for ammap (graves and areas)
    """
    if format == 'json':
        print 'creating json version of data'
        # TODO: need to replace this with a template!
        results =  {
            'areas': [],
            'movies': []
        }

        boundaries = CemeteryBoundary.objects.all()
        for boundary in boundaries:
            new_area = {
                'instanceName': boundary.section,
            }
            results['areas'].append(new_area)

        # for each movie we need zoom_level, title and lat-lng
        graves = Grave.objects.all()
        for grave in graves:
            new_movie = {
                'zoomLevel': 500,  # not sure yet what this needs to be
                'title': grave.name,
                'lat': grave.geom.centroid.y,
                'lon': grave.geom.centroid.x,
            }
            
            results['movies'].append(new_movie)

        json_data = json.dumps(results)
        return HttpResponse(json_data, mimetype='application/json')

    else:
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

