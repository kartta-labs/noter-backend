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
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from main import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('api/v0.1/images/', views.ImageList.as_view()),
    path('api/v0.1/images/<int:pk>/', views.ImageDetail.as_view()),
    path('api/v0.1/projects/', views.ProjectList.as_view()),
    path('api/v0.1/projects/<int:pk>/', views.ProjectDetail.as_view()),
    path('api/v0.1/annotations/', views.AnnotationsJsonList.as_view()),
    path('api/v0.1/annotations/<int:pk>/', views.AnnotationsJsonDetail.as_view()),
    path('api/v0.1/users/', views.UserList.as_view()),
    path('api/v0.1/users/<int:pk>/', views.UserDetail.as_view()),
    path('api/v0.1/whoami/', views.WhoAmI.as_view()),
    path('api/v0.1/whatdoihave/', views.WhatDoIHave.as_view()),
    path('admin/', admin.site.urls),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)