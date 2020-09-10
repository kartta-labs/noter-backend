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
  def get(self, request, format=None):
    if 'footprint' not in request.data:
      return Response(status=status.HTTP_400_BAD_REQUEST)
    if not lookup_endpoints['endpoints']:
      return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
  
    response = Response(status.HTTP_200_OK)
    response.data = []
    payload = {'footprint': request.data['footprint']}
    for endpoint in lookup_endpoints['endpoints']:
      # TODO: Send requests in parallel and wait for all.
      records = requests.get(endpoint, params=payload)
      if records.status_code == status.HTTP_200_OK:
        try:
          response.data.append(records.json()['data'])
        except:
          pass
    response['Content-Type'] = 'application/json'
    return response
