# 
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

rm main/migrations/0*
rm db.sqlite3
./manage.py makemigrations  --settings=noter_backend.dev_settings
./manage.py migrate --settings=noter_backend.dev_settings
./manage.py shell --settings=noter_backend.dev_settings -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'dontusethispassword')"
