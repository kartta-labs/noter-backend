from django.db import models, migrations
import uuid
from django.contrib.auth.hashers import make_password

PUBLIC_ID = 1
def apply_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    public_group = Group()
    public_group.name = "public"
    public_group.id = PUBLIC_ID
    public_group.save()


def revert_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(id=PUBLIC_ID).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200821_0710'),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration)
    ]