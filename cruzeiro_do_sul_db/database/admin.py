from django.contrib import admin
from .models import Facility, Beamline, Element, Experiment, Report, User

admin.site.site_header = "Cruzeiro do Sul Data Library for XAS & XRD administration"
admin.site.site_title = "Cruzeiro do Sul Data Library for XAS & XRD administration"
admin.site.index_title = ""

class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'state', 'city')

class BeamlineAdmin(admin.ModelAdmin):
    list_display = ('name', 'facility')

class ExperimentAdmin(admin.ModelAdmin):
    list_display = ('experiment_title', 'experiment_type')
    list_filter = ['experiment_type']
    fieldsets = (
        ('Experiment:', {
            'fields': ('experiment_type', 'experiment_title')
        }),
        ('XDI File:', {
            'fields': ('xdi_file', 'data_licence')
        }),
        ('Additional information:', {
            'fields': ('doi', 'additional_info', 'user')
        }),
    )

admin.site.register(User)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(Beamline, BeamlineAdmin)
admin.site.register(Element)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Report)