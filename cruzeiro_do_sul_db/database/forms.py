from django import forms
from .models import User, Experiment
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=250,required=True,help_text='Enter your e-mail.')
    first_name = forms.CharField(max_length=100,required=True,help_text='Enter your first name.')
    last_name = forms.CharField(max_length=100,required=True,help_text='Enter your last name.')
    web_page = forms.CharField(max_length=300,required=False,help_text='Enter the URL of your academic web page. Ex: Google Scholar, ORCID, etc.')
    country = forms.CharField(max_length=150,required=True,help_text='Enter your current country.')
    state = forms.CharField(max_length=150,required=True,help_text='Enter your current state/province.')
    city = forms.CharField(max_length=150,required=True,help_text='Enter your current city.')

    class Meta:
        model = User
        fields = ["email","first_name","last_name","web_page","country","state","city","password1","password2"]

class UserChangeForm(UserChangeForm):
    first_name = forms.CharField(max_length=100,required=True,help_text='Enter your first name.')
    last_name = forms.CharField(max_length=100,required=True,help_text='Enter your last name.')
    web_page = forms.CharField(max_length=300,required=False,help_text='Enter the URL of your academic web page. Ex: Google Scholar, ORCID, etc.')
    country = forms.CharField(max_length=150,required=True,help_text='Enter your current country.')
    state = forms.CharField(max_length=150,required=True,help_text='Enter your current state/province.')
    city = forms.CharField(max_length=150,required=True,help_text='Enter your current city.')
    
    class Meta:
        model = User
        fields = ["first_name","last_name","web_page","country","state","city","password"]

class AddExperiment(forms.ModelForm):

    class Meta:
        model = Experiment
        fields = '__all__'
    
    def clean(self):
        experiment_type = self.cleaned_data['experiment_type']
        # XRD experiments:
        if experiment_type == '4':
            if self.cleaned_data['sample_crystal_system'] == None:
                self._errors['sample_crystal_system'] = self.error_class(["Sample crystal system information is required for XRD experiments."])
            if self.cleaned_data['measurement_wavelength'] == None:
                self._errors['measurement_wavelength'] = self.error_class(["Measurement wavelength information is required for XRD experiments."])
            if self.cleaned_data['diffraction_radiation_type'] == None:
                self._errors['diffraction_radiation_type'] = self.error_class(["Diffraction radiation type information is required for XRD experiments."])
            if self.cleaned_data['space_group'] == None:
                self._errors['space_group'] = self.error_class(["Crystalline space group information is required for XRD experiments."])
            if self.cleaned_data['a'] == None:
                self._errors['a'] = self.error_class(["Crystalline a parameter is required for XRD experiments."])
            if self.cleaned_data['b'] == None:
                self._errors['b'] = self.error_class(["Crystalline b parameter is required for XRD experiments."])
            if self.cleaned_data['c'] == None:
                self._errors['c'] = self.error_class(["Crystalline c parameter is required for XRD experiments."])
            if self.cleaned_data['alpha'] == None:
                self._errors['alpha'] = self.error_class(["Crystalline alpha parameter is required for XRD experiments."])
            if self.cleaned_data['beta'] == None:
                self._errors['beta'] = self.error_class(["Crystalline beta parameter is required for XRD experiments."])
            if self.cleaned_data['gama'] == None:
                self._errors['gama'] = self.error_class(["Crystalline gamma parameter is required for XRD experiments."])
            if self.cleaned_data['min_2_theta'] == None:
                self._errors['min_2_theta'] = self.error_class(["Minimum 2 theta information is required for XRD experiments."])
            if self.cleaned_data['max_2_theta'] == None:
                self._errors['max_2_theta'] = self.error_class(["Maximum 2 theta information is required for XRD experiments."])
            if self.cleaned_data['step'] == None:
                self._errors['step'] = self.error_class(["2 theta step information is required for XRD experiments."])
            if self.cleaned_data['diffraction_2_theta'] == None:
                self._errors['diffraction_2_theta'] = self.error_class(["Diffraction 2 theta file is required for XRD experiments."])
            if self.cleaned_data['diffraction_intensity'] == None:
                self._errors['diffraction_intensity'] = self.error_class(["Diffraction intensity file is required for XRD experiments."])
        # XAS experiments:
        elif experiment_type == '1' or experiment_type == '2' or experiment_type == '3':
            spectrum_measurement_mode = self.cleaned_data['spectrum_measurement_mode']
            if self.cleaned_data['mono_d_spacing'] == None:
                self._errors['mono_d_spacing'] = self.error_class(["Monochromator d-spacing information is required for XAS, XANES and EXAFS experiments."])
            if self.cleaned_data['element'] == None:
                self._errors['element'] = self.error_class(["Absorbing element information is required for XAS, XANES and EXAFS experiments."])
            if self.cleaned_data['spectrum_data_type'] == None:
                self._errors['spectrum_data_type'] = self.error_class(["Spectrum data type information is required for XAS, XANES and EXAFS experiments."])
            if self.cleaned_data['spectrum_energy'] == None:
                self._errors['spectrum_energy'] = self.error_class(["Spectrum energy file is required for XAS, XANES and EXAFS experiments."])
            if spectrum_measurement_mode == None:
                self._errors['spectrum_measurement_mode'] = self.error_class(["Spectrum measurement mode information is required for XAS, XANES and EXAFS experiments."])
            if spectrum_measurement_mode == 't':
                if self.cleaned_data['spectrum_data_type'] == 'r':
                    if self.cleaned_data['spectrum_i0'] == None:
                        self._errors['spectrum_i0'] = self.error_class(["Spectrum i0 file is required for XAS, XANES and EXAFS transmission raw data."])
                    if self.cleaned_data['spectrum_itrans'] == None:
                        self._errors['spectrum_itrans'] = self.error_class(["Spectrum itrans file is required for XAS, XANES and EXAFS transmission raw data."])
                if self.cleaned_data['spectrum_data_type'] == 'm':
                    if self.cleaned_data['spectrum_mutrans'] == None:
                        self._errors['spectrum_mutrans'] = self.error_class(["Spectrum mutrans file is required for XAS, XANES and EXAFS transmission mu coefficients data."])
                if self.cleaned_data['spectrum_data_type'] == 'n':
                    if self.cleaned_data['spectrum_normtrans'] == None:
                        self._errors['spectrum_normtrans'] = self.error_class(["Spectrum normtrans file is required for XAS, XANES and EXAFS transmission normalized mu coefficients data."])
            if spectrum_measurement_mode == 'f':
                if self.cleaned_data['spectrum_data_type'] == 'r':
                    if self.cleaned_data['spectrum_i0'] == None:
                        self._errors['spectrum_i0'] = self.error_class(["Spectrum i0 file is required for XAS, XANES and EXAFS fluorescence raw data."])
                    if self.cleaned_data['spectrum_ifluor'] == None:
                        self._errors['spectrum_ifluor'] = self.error_class(["Spectrum ifluor file is required for XAS, XANES and EXAFS fluorescence raw data."])
                if self.cleaned_data['spectrum_data_type'] == 'm':
                    if self.cleaned_data['spectrum_mufluor'] == None:
                        self._errors['spectrum_mufluor'] = self.error_class(["Spectrum mufluor file is required for XAS, XANES and EXAFS fluorescence mu coefficients data."])
                if self.cleaned_data['spectrum_data_type'] == 'n':
                    if self.cleaned_data['spectrum_normfluor'] == None:
                        self._errors['spectrum_normfluor'] = self.error_class(["Spectrum normfluor file is required for XAS, XANES and EXAFS fluorescence normalized mu coefficients data."])
        # XRD + XAS experiments:
        else:
            if self.cleaned_data['sample_crystal_system'] == None:
                self._errors['sample_crystal_system'] = self.error_class(["Sample crystal system information is required for XRD experiments."])
            if self.cleaned_data['measurement_wavelength'] == None:
                self._errors['measurement_wavelength'] = self.error_class(["Measurement wavelength information is required for XRD experiments."])
            if self.cleaned_data['diffraction_radiation_type'] == None:
                self._errors['diffraction_radiation_type'] = self.error_class(["Diffraction radiation type information is required for XRD experiments."])
            if self.cleaned_data['space_group'] == None:
                self._errors['space_group'] = self.error_class(["Crystalline space group information is required for XRD experiments."])
            if self.cleaned_data['a'] == None:
                self._errors['a'] = self.error_class(["Crystalline a parameter is required for XRD experiments."])
            if self.cleaned_data['b'] == None:
                self._errors['b'] = self.error_class(["Crystalline b parameter is required for XRD experiments."])
            if self.cleaned_data['c'] == None:
                self._errors['c'] = self.error_class(["Crystalline c parameter is required for XRD experiments."])
            if self.cleaned_data['alpha'] == None:
                self._errors['alpha'] = self.error_class(["Crystalline alpha parameter is required for XRD experiments."])
            if self.cleaned_data['beta'] == None:
                self._errors['beta'] = self.error_class(["Crystalline beta parameter is required for XRD experiments."])
            if self.cleaned_data['gama'] == None:
                self._errors['gama'] = self.error_class(["Crystalline gamma parameter is required for XRD experiments."])
            if self.cleaned_data['min_2_theta'] == None:
                self._errors['min_2_theta'] = self.error_class(["Minimum 2 theta information is required for XRD experiments."])
            if self.cleaned_data['max_2_theta'] == None:
                self._errors['max_2_theta'] = self.error_class(["Maximum 2 theta information is required for XRD experiments."])
            if self.cleaned_data['step'] == None:
                self._errors['step'] = self.error_class(["2 theta step information is required for XRD experiments."])
            if self.cleaned_data['diffraction_2_theta'] == None:
                self._errors['diffraction_2_theta'] = self.error_class(["Diffraction 2 theta file is required for XRD experiments."])
            if self.cleaned_data['diffraction_intensity'] == None:
                self._errors['diffraction_intensity'] = self.error_class(["Diffraction intensity file is required for XRD experiments."])
            
            spectrum_measurement_mode = self.cleaned_data['spectrum_measurement_mode']
            if self.cleaned_data['mono_d_spacing'] == None:
                self._errors['mono_d_spacing'] = self.error_class(["Monochromator d-spacing information is required for XAS, XANES and EXAFS experiments."])
            if self.cleaned_data['element'] == None:
                self._errors['element'] = self.error_class(["Absorbing element information is required for XAS, XANES and EXAFS experiments."])
            if self.cleaned_data['spectrum_data_type'] == None:
                self._errors['spectrum_data_type'] = self.error_class(["Spectrum data type information is required for XAS, XANES and EXAFS experiments."])
            if self.cleaned_data['spectrum_energy'] == None:
                self._errors['spectrum_energy'] = self.error_class(["Spectrum energy file is required for XAS, XANES and EXAFS experiments."])
            if spectrum_measurement_mode == None:
                self._errors['spectrum_measurement_mode'] = self.error_class(["Spectrum measurement mode information is required for XAS, XANES and EXAFS experiments."])
            if spectrum_measurement_mode == 't':
                if self.cleaned_data['spectrum_data_type'] == 'r':
                    if self.cleaned_data['spectrum_i0'] == None:
                        self._errors['spectrum_i0'] = self.error_class(["Spectrum i0 file is required for XAS, XANES and EXAFS transmission raw data."])
                    if self.cleaned_data['spectrum_itrans'] == None:
                        self._errors['spectrum_itrans'] = self.error_class(["Spectrum itrans file is required for XAS, XANES and EXAFS transmission raw data."])
                if self.cleaned_data['spectrum_data_type'] == 'm':
                    if self.cleaned_data['spectrum_mutrans'] == None:
                        self._errors['spectrum_mutrans'] = self.error_class(["Spectrum mutrans file is required for XAS, XANES and EXAFS transmission mu coefficients data."])
                if self.cleaned_data['spectrum_data_type'] == 'n':
                    if self.cleaned_data['spectrum_normtrans'] == None:
                        self._errors['spectrum_normtrans'] = self.error_class(["Spectrum normtrans file is required for XAS, XANES and EXAFS transmission normalized mu coefficients data."])
            if spectrum_measurement_mode == 'f':
                if self.cleaned_data['spectrum_data_type'] == 'r':
                    if self.cleaned_data['spectrum_i0'] == None:
                        self._errors['spectrum_i0'] = self.error_class(["Spectrum i0 file is required for XAS, XANES and EXAFS fluorescence raw data."])
                    if self.cleaned_data['spectrum_ifluor'] == None:
                        self._errors['spectrum_ifluor'] = self.error_class(["Spectrum ifluor file is required for XAS, XANES and EXAFS fluorescence raw data."])
                if self.cleaned_data['spectrum_data_type'] == 'm':
                    if self.cleaned_data['spectrum_mufluor'] == None:
                        self._errors['spectrum_mufluor'] = self.error_class(["Spectrum mufluor file is required for XAS, XANES and EXAFS fluorescence mu coefficients data."])
                if self.cleaned_data['spectrum_data_type'] == 'n':
                    if self.cleaned_data['spectrum_normfluor'] == None:
                        self._errors['spectrum_normfluor'] = self.error_class(["Spectrum normfluor file is required for XAS, XANES and EXAFS fluorescence normalized mu coefficients data."])
        return self.cleaned_data