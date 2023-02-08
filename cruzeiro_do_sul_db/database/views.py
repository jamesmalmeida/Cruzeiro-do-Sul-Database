from django.shortcuts import render
from django.views import generic
from django.http import FileResponse
from .models import Experiment, Beamline, Facility, User

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_experiments = Experiment.objects.all().count()
    num_beamlines = Beamline.objects.all().count()
    num_facilities = Facility.objects.all().count()
    num_users = User.objects.all().count()

    # Available experiments (type = XAS):
    num_experimets_xas = Experiment.objects.filter(experiment_type__exact='1').count()
    # Available experiments (type = XANES):
    num_experiments_xanes = Experiment.objects.filter(experiment_type__exact='2').count()
    # Available experiments (type = EXAFS):
    num_experiments_exafs = Experiment.objects.filter(experiment_type__exact='3').count()
    # Available experiments (type = XRD):
    num_experiments_xrd = Experiment.objects.filter(experiment_type__exact='4').count()
    # Available experiments (type = XAS + XRD):
    num_experiments_xas_xrd = Experiment.objects.filter(experiment_type__exact='5').count()
    # Available experiments (type = XANES + XRD):
    num_experiments_xanes_xrd = Experiment.objects.filter(experiment_type__exact='6').count()
    # Available experiments (type = EXAFS + XRD):
    num_experiments_exafs_xrd = Experiment.objects.filter(experiment_type__exact='7').count()

    context = {
        'num_experiments': num_experiments,
        'num_experiments_xas': num_experimets_xas,
        'num_experiments_xanes': num_experiments_xanes,
        'num_experiments_exafs': num_experiments_exafs,
        'num_experiments_xrd': num_experiments_xrd,
        'num_experiments_xas_xrd': num_experiments_xas_xrd,
        'num_experiments_xanes_xrd': num_experiments_xanes_xrd,
        'num_experiments_exafs_xrd': num_experiments_exafs_xrd,
        'num_beamlines': num_beamlines,
        'num_facilities': num_facilities,
        'num_users': num_users,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def search_xas(request):
    return render(request, 'search_xas.html')

def search_xrd(request):
    return render(request, 'search_xrd.html')

def about(request):
    return render(request, 'about.html')

def login(request):
    return render(request, 'login.html')

def create_account(request):
    return render(request, 'create_account.html')

def upload_data(request):
    return render(request, 'upload_data.html')

class ExperimentListView(generic.ListView):
    model = Experiment
    paginate_by = 6

class ExperimentDetailView(generic.DetailView):
    model = Experiment

def file_response(request, pk, string):
    
    experiment = Experiment.objects.get(pk=int(pk))

    if string == 'energy':
        return FileResponse(experiment.spectrum_energy, as_attachment=True)
    elif string == 'i0':
        return FileResponse(experiment.spectrum_i0, as_attachment=True)
    elif string == 'itrans':
        return FileResponse(experiment.spectrum_itrans, as_attachment=True)
    elif string == 'ifluor':
        return FileResponse(experiment.spectrum_ifluor, as_attachment=True)
    elif string == 'mutrans':
        return FileResponse(experiment.spectrum_mutrans, as_attachment=True)
    elif string == 'mufluor':
        return FileResponse(experiment.spectrum_mufluor, as_attachment=True)
    elif string == 'normtrans':
        return FileResponse(experiment.spectrum_normtrans, as_attachment=True)
    elif string == 'normfluor':
        return FileResponse(experiment.spectrum_normfluor, as_attachment=True)
    elif string == 'xrd_2_theta':
        return FileResponse(experiment.diffraction_2_theta, as_attachment=True)
    elif string == 'xrd_intensity':
        return FileResponse(experiment.diffraction_intensity, as_attachment=True)
    elif string == 'cif':
        return FileResponse(experiment.cif_file, as_attachment=True)
    else:
        return