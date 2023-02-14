from django.shortcuts import render
from django.http import FileResponse
from django.urls import reverse_lazy
from .forms import UserCreationForm, UserChangeForm, AddExperiment
from .models import Experiment, Beamline, Facility, User, Element
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView, ListView
from django.db.models import Q 
from functools import reduce
import operator

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

def experiment_list(request):
    list = Experiment.objects.all()
    page = request.GET.get('page', 1)
    # Number of paginations:
    paginator = Paginator(list, 20)
    try:
        experiments = paginator.page(page)
    except PageNotAnInteger:
        experiments = paginator.page(1)
    except EmptyPage:
        experiments.paginator.page(paginator.num_pages)
    return render(request, 'experiment_list.html', {'experiments': experiments})

def user_data_list(request):
    list = Experiment.objects.filter(user__id__exact=request.user.id)
    page = request.GET.get('page', 1)
    # Number of paginations:
    paginator = Paginator(list, 20)
    try:
        experiments = paginator.page(page)
    except PageNotAnInteger:
        experiments = paginator.page(1)
    except EmptyPage:
        experiments.paginator.page(paginator.num_pages)
    return render(request, 'user_data.html', {'experiments': experiments})

def search_result(request):
    absorbing_element = str(request.GET.get("absorbing_element"))
    composition = request.GET.get("composition").split()

    if request.GET.get("edge") == 'Any':
        edge = ''
    else:
        edge = str(request.GET.get("edge"))

    if request.GET.get("data_type") == 'Any':
        data_type = ''
    else:
        data_type = str(request.GET.get("data_type"))
    
    if request.GET.get("measurement") == 'Any':
        measurement = ''
    else:
        measurement = str(request.GET.get("measurement"))

    page = request.GET.get('page', 1)
    
    list = Experiment.objects.filter(
        Q(element__symbol__icontains=absorbing_element) &
        Q(element__edge__icontains=edge) &
        Q(experiment_type__icontains=data_type) &
        Q(spectrum_measurement_mode__icontains=measurement) &
        Q(sample_stoichiometry_iupac__icontains=composition) | reduce(operator.and_, (Q(sample_stoichiometry_iupac__icontains=x) for x in composition))
    )
    # Number of paginations:
    paginator = Paginator(list, 20)
    try:
        experiments = paginator.page(page)
    except PageNotAnInteger:
        experiments = paginator.page(1)
    except EmptyPage:
        experiments.paginator.page(paginator.num_pages)
    return render(request, 'experiment_list.html', {'experiments': experiments})
    

def search_data(request):
    return render(request, 'search_data.html')

def about(request):
    return render(request, 'about.html')

def login(request):
    return render(request, 'registration/login.html')

def signup(request):
    return render(request, 'signup.html')

def experiment_detail(request, pk):
    experiment = Experiment.objects.get(pk=int(pk))
    return render(request, 'experiment_detail.html', {'experiment': experiment})

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

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class ChangeAccountView(UpdateView):
    model = User
    form_class = UserChangeForm
    success_url = reverse_lazy("account")
    template_name = "registration/change_account.html"

class AddExperiment(CreateView):
    form_class = AddExperiment
    template_name = "add_experiment.html"
    success_url = reverse_lazy('user-data')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)

class DeleteExperiment(DeleteView):
    model = Experiment
    template_name = "delete_experiment.html"
    success_url = reverse_lazy('user-data')

class AddElement(CreateView):
    model = Element
    fields = '__all__'
    template_name = "add_element.html"
    success_url = reverse_lazy('add-experiment')

class AddBeamline(CreateView):
    model = Beamline
    fields = '__all__'
    template_name = "add_beamline.html"
    success_url = reverse_lazy('add-experiment')

class AddFacility(CreateView):
    model = Facility
    fields = '__all__'
    template_name = "add_facility.html"
    success_url = reverse_lazy('add-beamline')