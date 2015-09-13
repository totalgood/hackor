from django.contrib import admin
from django.db.models import get_app, get_models

# register all the models this app:
app = get_app('pacs')
for model in get_models(app):
    admin.site.register(model)
