from django.contrib.auth.models import User, Group
from main.serializers import ProjectSerializer
import uuid

user = User.objects.create_user('anonymous@public.user', 'anonymous@public.user', str(uuid.uuid4()))
group = Group.objects.get(id = 1); user.groups.add(group)

# TODO(embeepea): confirm that the following is the correct sequence to
#   initialize the db with a default project:
project = ProjectSerializer(data={
  'name': 'Default Project',
  'labels_json': '{"facade", "window", "door"}'
})
if project.is_valid():
  project.save(owner_email=user.email)
