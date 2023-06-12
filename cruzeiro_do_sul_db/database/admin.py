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
    list_display = ('experiment_title', 'experiment_type', 'spectrum_measurement_mode', 'beamline')
    list_filter = ['experiment_type']
    fieldsets = (
        ('Experiment:', {
            'fields': ('experiment_type', 'experiment_title')
        }),
        ('Absorbing element:', {
            'fields': ['element']
        }),
        ('Sample:', {
            'fields': ('sample_name', 'sample_stoichiometry_iupac', 'sample_stoichiometry_moiety', 'sample_prep', 'sample_dimensions', 'sample_ph', 'sample_eh', 'sample_volume', 'sample_porosity', 'sample_density', 'sample_concentration', 'sample_resistivity', 'sample_viscosity', 'sample_electric_field', 'sample_magnetic_field', 'sample_magnetic_moment', 'sample_electrochemical_potential', 'sample_opacity', 'sample_purity', 'sample_crystal_system')
        }),
        ('Crystalline:', {
            'fields': ('space_group', 'z', 'a', 'b', 'c', 'alpha', 'beta', 'gama')
        }),
        ('Powder parameters:', {
            'fields': ('min_2_theta', 'max_2_theta', 'step')
        }),
        ('Measurement conditions:', {
            'fields': ('measurement_temperature', 'measurement_pressure', 'measurement_current', 'measurement_wavelength', 'diffraction_radiation_type')
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
            'fields': ('detector_i0', 'detector_it', 'detector_if')
        }),
        ('Spectrum data:', {
            'fields': ('spectrum_measurement_mode', 'spectrum_data_type', 'spectrum_energy', 'spectrum_i0', 'spectrum_itrans', 'spectrum_ifluor', 'spectrum_mutrans', 'spectrum_mufluor', 'spectrum_normtrans', 'spectrum_normfluor', 'spectrum_norm_info', 'reference')
        }),
        ('Diffraction data:', {
            'fields': ('diffraction_2_theta', 'diffraction_intensity')
        }),
        ('Additional data:', {
            'fields': ('cif_file', 'data_licence')
        }),
        ('Additional information:', {
            'fields': ('citation', 'doi', 'additional_info', 'user')
        }),
    )

admin.site.register(User)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(Beamline, BeamlineAdmin)
admin.site.register(Element)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Report)