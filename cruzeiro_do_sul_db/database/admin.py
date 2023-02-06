from django.contrib import admin
from .models import Address, User, Facility, Beamline, Element, Citation, Experiment, Report

admin.site.site_header = "Cruzeiro do Sul Data Library for XAS & XRD administration"
admin.site.site_title = "Cruzeiro do Sul Data Library for XAS & XRD administration"
admin.site.index_title = ""

class AddressAdmin(admin.ModelAdmin):
    list_display = ('city', 'state', 'country')
    list_filter = ('country', 'state')

class UserAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email')

class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')

class BeamlineAdmin(admin.ModelAdmin):
    list_display = ('name', 'facility')

class ExperimentAdmin(admin.ModelAdmin):
    list_display = ('experiment_title', 'experiment_type', 'measurement_mode', 'beamline')
    list_filter = ['experiment_type']
    fieldsets = (
        ('Experiment:', {
            'fields': ('experiment_type', 'experiment_title')
        }),
        ('Absorbing element:', {
            'fields': ['element']
        }),
        ('Sample:', {
            'fields': ('sample_name', 'stoichiometry_iupac', 'stoichiometry_moiety', 'sample_prep', 'sample_dimensions', 'sample_ph', 'sample_eh', 'sample_volume', 'sample_porosity', 'sample_density', 'sample_concentration', 'sample_resistivity', 'sample_viscosity', 'sample_electric_field', 'sample_magnetic_field', 'sample_magnetic_moment', 'sample_electrochemical_potential', 'sample_opacity', 'sample_purity', 'sample_crystal_system')
        }),
        ('Crystalline:', {
            'fields': ('space_group', 'z', 'a', 'b', 'c', 'alpha', 'beta', 'gama')
        }),
        ('Powder parameters:', {
            'fields': ('min_2_theta', 'max_2_theta', 'step')
        }),
        ('Measurement conditions:', {
            'fields': ('measurement_temperature', 'measurement_pressure', 'measurement_current', 'wavelength', 'diff_radiation_type')
        }),
        ('Scan:', {
            'fields': ('start_time', 'end_time', 'edge_energy', 'os', 'software')
        }),
        ('Beamline:', {
            'fields': ['beamline']
        }),
        ('Monochromator:', {
            'fields': ('mono_name', 'mono_d_spacing')
        }),
        ('Detector:', {
            'fields': ('detector_i0', 'detector_it')
        }),
        ('Spectrum data:', {
            'fields': ('measurement_mode', 'data_type', 'spectrum_energy', 'spectrum_i0', 'spectrum_itrans', 'spectrum_mutrans', 'spectrum_normtrans', 'norm_info', 'reference')
        }),
        ('Diffraction data:', {
            'fields': ('diffraction_2_theta', 'diffraction_intensity')
        }),
        ('Additional data:', {
            'fields': ('cif_file', 'data_licence')
        }),
        ('Additional information:', {
            'fields': ('user', 'citation', 'additional_info')
        }),
    )

admin.site.register(Address, AddressAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(Beamline, BeamlineAdmin)
admin.site.register(Element)
admin.site.register(Citation)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Report)