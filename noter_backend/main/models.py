import os
import uuid

from django.db import models
from django.conf import settings


class BasicUser(models.Model):
    display_name = models.CharField(max_length=100, blank=True, default="")
    email = models.EmailField(max_length=512, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Project(models.Model):
    name = models.CharField(max_length=100, blank=True, default="")
    labels_json = models.TextField()
    owner = models.ForeignKey("auth.User", related_name="projects_by_user", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


def generate_uuid_filename(instance, filename):
    """
    Generate a uuid filename keeping the file extension.
    """
    extension = filename.split(".")[-1]
    return "{}.{}".format(uuid.uuid4(), extension)


class Image(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey("auth.User", related_name="images_by_user", on_delete=models.CASCADE)
    part_of_project = models.ForeignKey(Project, related_name="images_in_project", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, default="")
    description = models.TextField(blank=True, default="")
    image = models.ImageField("Image", upload_to=generate_uuid_filename)


class AnnotationsJson(models.Model):
    on_image = models.ForeignKey(Image, related_name="annotations_by_image", on_delete=models.SET_NULL, null=True)
    content_json = models.TextField()
    owner = models.ForeignKey("auth.User", related_name="annotations_by_user", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
