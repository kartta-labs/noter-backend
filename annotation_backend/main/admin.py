from django.contrib import admin
from main.models import BasicUser, Image, Project, AnnotationsJson

admin.site.register(BasicUser)
admin.site.register(Image)
admin.site.register(Project)
admin.site.register(AnnotationsJson)