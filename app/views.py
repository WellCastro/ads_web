# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
import logging

from django.views import generic

log = logging.getLogger(__name__)
URL = "http://45.55.190.255:8001/api/property"


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


class Index(generic.TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context["properties"] = get_all()
        context["cities"] = count_city()

        return context


class Api(generic.TemplateView):
    template_name = "doc.html"
