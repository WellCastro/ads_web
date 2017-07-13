# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
import json
import logging

from django.views import generic
from django.conf import settings
from django.shortcuts import HttpResponse

log = logging.getLogger(__name__)
URL = "http://localhost:8001/api/property"


def get_all():
    # get in API properties
    result = None
    try:
        r = requests.get(URL + '/list/all')
        result = r.json()
    except Exception, e:
        log.error('GET error: %r' % e)

    return result


def count_city():
    qs = get_all()
    labels = []

    if qs:
        city_list = []
        city_set = set()

        for i in list(qs['results']):
            value = i.get('city')
            city_list.append(value)
            city_set.add(value)

        for i in city_set:
            labels.append({
                          "city": i.encode("utf-8"),
                          "count": city_list.count(i)
                          })

    return labels


def post_table(data):
    try:
        requests.post(URL + '/add/', data=data)
    except Exception, e:
        log.error('POST error: %r' % data)
        pass


def populate_table():
    path = settings.BASE_DIR + "/utils/seed.json"
    json_file = None
    try:
        with open(path) as json_data:
            json_file = json.load(json_data)
    except Exception, e:
        print e
        pass

    for j in json_file:
        body = {"title": j.get('title'),
                "state": j.get('location').get('city').get('state'),
                "city": j.get('location').get('city').get('name'),
                "name": j.get('location').get('name'),
                "id_json": j.get('id'),
                "purpose": j.get('purpose'),
                "listing_type": j.get('listingType'),
                "published_on": j.get('published_on')}
        post_table(body)


class Index(generic.TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context["properties"] = get_all()
        context["cities"] = count_city()

        return context


class Api(generic.TemplateView):
    template_name = "doc.html"


def reset(request):

    if request.method == 'GET':
        try:
            response_data = {}
            Property.objects.all().delete()
            populate_table()
            response_data['status'] = 'ok'
        except Exception, e:
            print e

    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )
