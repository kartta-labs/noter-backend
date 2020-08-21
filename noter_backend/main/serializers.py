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
from rest_framework import serializers
from django.contrib.auth.models import User, Group

from main.models import Image, BasicUser, Project, AnnotationsJson


class BasicUserSerializer(serializers.ModelSerializer):
    images_by_user = serializers.PrimaryKeyRelatedField(many=True, queryset=Image.objects.all())
    projects_by_user = serializers.PrimaryKeyRelatedField(many=True, queryset=Project.objects.all())
    annotations_by_user = serializers.PrimaryKeyRelatedField(many=True, queryset=AnnotationsJson.objects.all())

    class Meta:
        model = BasicUser
        fields = ['id', 'display_name', 'email', 'projects_by_user', 'images_by_user', 'annotations_by_user']

def get_or_create_authenticated_user(validated_data):
    email = validated_data.pop("owner_email")
    # owner, created = BasicUser.objects.get_or_create(email=email)
    if not User.objects.filter(email=email).exists():
        user = User.objects.create_user(email, email, email)
        user.save()
    return User.objects.get(email=email)

class ProjectSerializer(serializers.ModelSerializer):
    # images = serializers.PrimaryKeyRelatedField(many=True, queryset=Image.objects.all())
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Project
        fields = ['id', 'name', 'owner', 'labels_json']

    def create(self, validated_data, *args, **kwargs):
        owner = get_or_create_authenticated_user(validated_data)
        return Project.objects.create(owner=owner, **validated_data)


class ImageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    project_id = serializers.ReadOnlyField(source='part_of_project.id')

    class Meta:
        model = Image
        fields = ['id', 'title', 'description', 'owner', 'project_id']

    def create(self, validated_data, *args, **kwargs):
        owner = get_or_create_authenticated_user(validated_data)
        project_id = validated_data.pop("project_id")

        return Image.objects.create(owner=owner, part_of_project=Project.objects.get(id=project_id), **validated_data)


class AnnotationsJsonSerializer(serializers.ModelSerializer):
    #images = serializers.PrimaryKeyRelatedField(many=True, queryset=Image.objects.all())
    owner = serializers.ReadOnlyField(source='owner.email')
    image_id = serializers.ReadOnlyField(source='on_image.id')

    class Meta:
        model = AnnotationsJson
        fields = ['id', 'owner', 'content_json', "image_id"]

    def create(self, validated_data, *args, **kwargs):
        owner = get_or_create_authenticated_user(validated_data)
        image_id = validated_data.pop("image_id")

        return AnnotationsJson.objects.create(owner=owner, on_image=Image.objects.get(id=image_id), **validated_data)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id','name',]

    def create(self, validated_data, *args, **kwargs):
        return Group.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    images_by_user = ImageSerializer(read_only=True, many=True)
    images_by_user_id = serializers.PrimaryKeyRelatedField(write_only=True, source='images_by_user', many=True, queryset=Image.objects.all())

    projects_by_user = ProjectSerializer(read_only=True, many=True)
    projects_by_user_id = serializers.PrimaryKeyRelatedField(write_only=True, source='projects_by_user', many=True, queryset=Project.objects.all())

    annotations_by_user = AnnotationsJsonSerializer(read_only=True, many=True)
    annotations_by_user_id = serializers.PrimaryKeyRelatedField(write_only=True, source='annotations_by_user', many=True, queryset=AnnotationsJson.objects.all())

    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ['email', 'projects_by_user', 'projects_by_user_id', 'images_by_user', 'images_by_user_id', 'annotations_by_user', 'annotations_by_user_id', 'groups',]
