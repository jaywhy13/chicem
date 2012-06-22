from django.http import HttpResponse
from django.shortcuts import render_to_response
from graves.models import Grave, CemeteryBoundary
from django.conf import settings
import json


def data(request, format=None):
    """ returns the data settings in XML for ammap (graves and areas)
    """
    if format == 'json':
        #print 'creating json version of data'
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
                'id': grave.pk,
                # 'zoomLevel': 500,  # not sure yet what this needs to be
                'title': grave.name,
                'lat': grave.geom.centroid.y,
                'lon': grave.geom.centroid.x,
                'plot' : grave.plot,
                'died' : grave.get_year_of_death(),
                'date': grave.get_life_duration(),
                'section' : grave.section,
            }

            results['movies'].append(new_movie)

        json_data = json.dumps(results)
        return HttpResponse(json_data, mimetype='application/json')

    else:
        graves = Grave.objects.all()
        boundaries = CemeteryBoundary.objects.all()
        swf_location = "ammap.swf"
        return render_to_response("graves/data.xml", locals())

def sections(request):
    sections = CemeteryBoundary.objects.all().order_by('section')
    return render_to_response("graves/sections.html", locals())

def sections_coords(request):
    all_sections = CemeteryBoundary.objects.all()
    sections = []
    for section in all_sections:
        coords = []
        for (lon, lat) in section.geom.coords[0][0]:
            coords.append((lat, lon))

        section_obj = {
            "section_name" : section.section,
            "coords" : coords,
            "color": section.color,
            }
        sections.append(section_obj)
    sections_json = json.dumps(sections)
    return HttpResponse(sections_json, mimetype='application/json')
    


def search(request, query):
    if query == '':
        return HttpResponse('[]', mimetype='application/json')
    try:
        plot_no = int(query)
        graves = Grave.objects.filter(plot__contains=plot_no)
    except:
        graves = Grave.objects.filter(name__icontains=query)

    format = request.GET.get('format', 'html')

    if format is 'json':
        # do json stuff
        # print 'doing json stuff'
        results = []
        for grave in graves:
            # print grave.id
            # print grave.get_life_duration()
            search_result = {
                'id': grave.pk,
                'plot': grave.plot,
                'name': grave.name,
                'date': grave.get_life_duration(),
            }
            results.append(search_result)

        json_data = json.dumps(results)
        return HttpResponse(json_data, mimetype='application/json')
    else:
        return render_to_response("graves/list.html", locals())

