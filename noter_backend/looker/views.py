"""
Copyright 2020 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from noter_backend.settings import lookup_endpoints

from django.shortcuts import render
import os
import json
from django.http import Http404
import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from django.contrib.auth.models import User, Group
from guardian.shortcuts import assign_perm, remove_perm

from main.models import Image, Project, AnnotationsJson
from noter_backend.generate_signed_urls import generate_signed_url
from main.permissions import IsOwnerAndReadOnlyOrRefuse, IsOwnerOrReadOnly, IsReadOnlyAndHasAccessOrRefuse, IsReadOnlyAndPublicOrRefuse, IsOwnerOrRefuse
from main.serializers import ImageSerializer, UserSerializer, BasicUserSerializer, ProjectSerializer, AnnotationsJsonSerializer, GroupSerializer


class LookUp(APIView):
  def post(self, request, format=None):
    if 'footprint' not in request.data:
      return Response(status=status.HTTP_400_BAD_REQUEST)
    if not lookup_endpoints['endpoints']:
      return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
  
    response = Response(status.HTTP_200_OK)
    response.data = {'candidates':[]}
    payload = {'footprint': request.data['footprint']}
    for endpoint in lookup_endpoints['endpoints']:
      # TODO: Send requests in parallel and wait for all.
      records = requests.get(endpoint, params=payload)
      if records.status_code == status.HTTP_200_OK:
        try:
          response.data['candidates'].append({'from':endpoint , 'items':records.json()['data']})
        except Exception as e:
          pass
    response['Content-Type'] = 'application/json'
    return response

class LookAround(APIView):
  def get_bbox(self, coordinates):
    bbox = {'lonMin':180, 'lonMax':-180, 'latMin':90, 'latMax':-90}
    lon = 0; lon_min = 180; lon_max = -180
    lat = 0; lat_min = 90; lat_max = -90
    for coordinate in coordinates:
      lon = coordinate[0]
      lat = coordinate[1]

      lon_min = lon_min if lon_min < lon else lon
      lon_max = lon_max if lon_max > lon else lon
      lat_min = lat_min if lat_min < lat else lat
      lat_max = lat_max if lat_max > lat else lat

    # TODO(sasantv): A better approach is to expand the bbox in meters.
    EXPANSION_IN_DEGREES = 0.001
    lon_min -= EXPANSION_IN_DEGREES
    lon_max += EXPANSION_IN_DEGREES
    lat_min -= EXPANSION_IN_DEGREES
    lat_max += EXPANSION_IN_DEGREES
    return ','.join(str(x) for x in [lon_min,lat_min,lon_max,lat_max])

  def fetch_relations_with_noter_tag(self, bbox):
    headers = {'Accept':'application/json'}
    payload = {'bbox': bbox}
    editor_map_endpoint = os.environ.get('KARTTA_EDITOR_URL').strip('/') + '/api/0.6/map'
    records = requests.get(editor_map_endpoint, params=payload, headers=headers)
    if records.status_code != status.HTTP_200_OK:
      return None, records.status_code
    relations = []
    records = records.json()
    for element in records['elements']:
      if element['type'] == 'relation' and 'noter_image_id' in element['tags']:
        relations.append(element)
    return relations, status.HTTP_200_OK

  def get(self, request, format=None):
    if 'footprint' in request.query_params:
      footprint = json.loads(request.query_params['footprint'])
    elif 'footprint' in request.data:
      footprint = json.loads(request.data['footprint'])
    else:
      return Response(status=status.HTTP_400_BAD_REQUEST)

    if ('geometry' not in footprint
        or 'coordinates' not in footprint['geometry']
        or len(footprint['geometry']['coordinates']) < 1
        or len(footprint['geometry']['coordinates'][0]) < 1):
      return Response(status=status.HTTP_400_BAD_REQUEST)

    bbox = self.get_bbox(footprint['geometry']['coordinates'][0])
    relations, status_code = self.fetch_relations_with_noter_tag(bbox)
    if status_code != status.HTTP_200_OK:
      return Response(status_code)
    response = Response(status.HTTP_200_OK)
    response['Content-Type'] = 'application/json'
    response.data = {'data':[]}
    response.data['data'].append({"relations":relations})
    return response
