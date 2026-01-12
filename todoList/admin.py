from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateFilter
from unfold.contrib.import_export.forms import (ExportForm, ImportForm,
                                                SelectableFieldsExportForm)
from unfold.forms import (AdminPasswordChangeForm, UserChangeForm,
                          UserCreationForm)

from todoList.models import TODO, Profile, lang
from simple_history.admin import SimpleHistoryAdmin
from modeltranslation.admin import TabbedTranslationAdmin
from modeltranslation.admin import TranslationAdmin
from guardian.admin import GuardedModelAdmin
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
from django_celery_beat.admin import PeriodicTaskAdmin as BasePeriodicTaskAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponseRedirect
from celery import current_app as celery_app
from modeltranslation.admin import TranslationAdmin

admin.site.unregister(PeriodicTask)
class PeriodicTaskAdmin(ModelAdmin, BasePeriodicTaskAdmin):
    list_display = ('name', 'enabled', 'last_run_at', 'total_run_count', 'scheduler', 'one_off')
    list_filter = ('enabled', 'task')
    list_per_page = 10
    search_fields = ('name', 'task', 'enabled', 'last_run_at', 'total_run_count')
    actions = ['delete_selected', 'run_task_action']

    
    @admin.action(description='Delete selected tasks')
    def delete_selected(self, request, queryset):
        queryset.delete()
        self.message_user(request, 'Tasks deleted')
    
    @admin.action(description='Run selected tasks')
    def run_task_action(self, request, queryset):
        results = []
        for task in queryset:
            task_func_name = task.task
            try:
                task_func = celery_app.tasks.get(task_func_name)
                
                if task_func:
                    task_func.apply_async() #apply_async() method is used to run the task asynchronously
                    results.append(f'Task {task.name} executed.')
                else:
                    results.append(f'Task {task.name} could not be found.')
            except Exception as e:
                results.append(f'Error executing task {task.name}: {str(e)}')

        for result in results:
            self.message_user(request, result)

    
admin.site.register(PeriodicTask, PeriodicTaskAdmin)




admin.site.unregister(User)    

class UserAdmin(BaseUserAdmin, ModelAdmin, ImportExportModelAdmin, GuardedModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    import_form_class = ImportForm
    export_form_class = ExportForm


admin.site.register(User, UserAdmin)   


class TODOAdmin(ModelAdmin, TabbedTranslationAdmin, SimpleHistoryAdmin, ImportExportModelAdmin):
    list_display = ('title','title_de', 'description','description_de', 'status', 'date', 'user')
    list_filter = ('status', ("date", RangeDateFilter))
    list_filter_submit = True
    search_fields = ('title', 'description', 'status', 'date', 'user')
    list_per_page = 10
    actions = ['mark_completed', 'mark_pending', 'delete_selected']
    import_form_class = ImportForm
    export_form_class = ExportForm
    
    
    selectable_fields_export_form_class = SelectableFieldsExportForm
    @admin.action(description='Mark as completed')
    def mark_completed(self, request, queryset):
        queryset.update(status='c')
        self.message_user(request, 'Task marked as completed')

    @admin.action(description='Mark as pending')
    def mark_pending(self, request, queryset):
        queryset.update(status='p')
        self.message_user(request, 'Task marked as pending')

    @admin.action(description='Delete selected tasks')
    def delete_selected(self, request, queryset):
        queryset.delete()
        self.message_user(request, 'Tasks deleted')


class profileAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ('user', 'phone_number')
    list_per_page = 10
    actions = ['delete_selected']
    import_form_class = ImportForm
    export_form_class = ExportForm

    @admin.action(description='Delete selected profiles')
    def delete_selected(self, request, queryset):
        queryset.delete()
        self.message_user(request, 'Profiles deleted')

class langAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ('language', 'user')
    list_per_page = 10
    actions = ['delete_selected']
    import_form_class = ImportForm
    export_form_class = ExportForm

    @admin.action(description='Delete selected languages')
    def delete_selected(self, request, queryset):
        queryset.delete()
        self.message_user(request, 'Languages deleted')
    
admin.site.register(TODO, TODOAdmin)

admin.site.register(Profile, profileAdmin)

admin.site.register(lang, langAdmin)