from django.contrib import admin
from django.apps import apps
from django import forms

excluded_models = []
unsearchable_field_types = ['ForeignKey', 'OneToOneField', 'TimeField', 'DateTimeField', 'DateField', 'AutoField']
unsearchable_field_names = ['id', 'pk', 'primary_key']
search_related_id = False
search_related_pk = True

apps_to_admin = ['pacs']
link_suffix = '____'

# register some admin interface managers for each app in the app_names list
for app_name in apps_to_admin:
    app = apps.get_app_config(app_name)
    for model_name, Model in app.models.iteritems():
        if model_name in excluded_models:
            continue

        model_admin_name = model_name + 'Admin'
        if model_admin_name in globals():
            ModelAdmin = globals()[model_admin_name]
        else:
            # FIXME: need a class factory rather than this class statement multiple times in a loop
            class ModelAdmin(admin.ModelAdmin):
                pass

        if len(ModelAdmin.list_display) <= 1 or ModelAdmin.list_display[0] == '__str__':
            list_display = []
            for field in Model._meta.fields:
                if field.get_internal_type() == 'ForeignKey':
                    list_display += [field.name + link_suffix]
                elif field.get_internal_type() == 'OneToOneField':
                    list_display += [field.name + link_suffix]
                else:
                    list_display += [field.name]
            # Can do this for any OneToOneFields?
            ModelAdmin.list_display = list_display

        if ModelAdmin.search_fields == ():
            search_fields = [field.name for field in Model._meta.fields
                             if field.get_internal_type() not in unsearchable_field_types
                             and field.name not in unsearchable_field_names]

            for field in Model._meta.fields:
                if field.get_internal_type() == 'ForeignKey':
                    if search_related_id and 'id' in field.related.model._meta.get_all_field_names():
                        search_fields.append(field.name + '__id')
                    if search_related_pk and 'pk' in field.related.model._meta.get_all_field_names():
                        search_fields.append(field.name + '__pk')
                    if 'name' in [rel_field.name for rel_field in field.rel.to._meta.fields]:
                        search_fields.append(field.name + '__name')
            ModelAdmin.search_fields = search_fields

        if not ModelAdmin.date_hierarchy:
            for field in Model._meta.fields:
                if field.get_internal_type() in ('DateTimeField', 'DateField'):
                    ModelAdmin.date_hierarchy = field.name
                    break

        form_name = '%sForm' % Model._meta.object_name
        if ModelAdmin.form == forms.ModelForm and form_name in globals():
            ModelAdmin.form = globals()[form_name]

        try:
            admin.site.register(Model, ModelAdmin)
        except:
            pass
