from django.contrib.auth.models import User, Group
import uuid

user = User.objects.create_user('anonymous@public.user', 'anonymous@public.user', str(uuid.uuid4()))
group = Group.objects.get(id = 1); user.groups.add(group)