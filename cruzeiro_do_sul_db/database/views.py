from django.shortcuts import render, redirect
from django.http import FileResponse
from django.urls import reverse_lazy
from django.conf import settings
from .forms import UserCreationForm, UserChangeForm, AddExperiment, UploadFileForm, UploadXDIForm
from .forms import RegisterForm

from .models import Experiment, Beamline, Facility, User, Element, Normalization, Comparison, XDIFile
from .normalization import read_file
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView, ListView
from django.db.models import Q 
from functools import reduce
import operator
import plotly.offline as opy
import plotly.graph_objs as go
import plotly.express as px

import tempfile
import os
import re
from io import StringIO
from chardet import detect
from .ga_combinator import ga
import pandas as pd
import numpy as np
from lmfit.models import LinearModel
from .forms import UploadFileForm
from numpy import diff
from scipy.interpolate import interp1d
from django.http import HttpResponse
import mimetypes
import shlex

from django.core.files.storage import FileSystemStorage
from datetime import datetime

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
        'num_experiments'          : num_experiments,
        'num_experiments_xas'      : num_experimets_xas,
        'num_experiments_xanes'    : num_experiments_xanes,
        'num_experiments_exafs'    : num_experiments_exafs,
        'num_experiments_xrd'      : num_experiments_xrd,
        'num_experiments_xas_xrd'  : num_experiments_xas_xrd,
        'num_experiments_xanes_xrd': num_experiments_xanes_xrd,
        'num_experiments_exafs_xrd': num_experiments_exafs_xrd,
        'num_beamlines'            : num_beamlines,
        'num_facilities'           : num_facilities,
        'num_users'                : num_users,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def experiment_list(request):
    list = Experiment.objects.all().order_by("experiment_title")
    page = request.GET.get('page',1)
   
    # Number of paginations:
    paginator = Paginator(list, len(list)) if len(list) > 0 else  Paginator(list,1)

    
    try:
        experiments = paginator.page(page)
    except PageNotAnInteger:
        experiments = paginator.page(1)
    except EmptyPage:
        #experiments.paginator.page(paginator.num_pages)
        experiments = paginator.page(1)
    return render(request, 'experiment_list.html', {'experiments': experiments})

def user_data_list(request):
    list = Experiment.objects.filter(user__id__exact=request.user.id)
    page = request.GET.get('page', 1)
    # Number of paginations:
    paginator = Paginator(list, len(list)) if len(list) > 0 else  Paginator(list,1)

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
        Q(element_symbol__icontains=absorbing_element) &
        Q(element_edge__icontains=edge) &
        Q(experiment_type__icontains=data_type) &
        Q(sample_formula__icontains=absorbing_element)
        |
        reduce(operator.and_, (Q(element_symbol__icontains=x) for x in composition)   )
    )
    # Number of paginations:
    paginator = Paginator(list, len(list)) if len(list) > 0 else  Paginator(list,1)
    
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


def add_experiment_detail(field_name, field, informed_fields,   not_informed_fields):
    """
    Helper funcion to separate informed and not informed fields for more conside rendering
    field_name: name of the field to be shown in the page
    field: attribute to 
    """
    if (field == 'Not Informed') or (field == 'none' ):
        not_informed_fields[field_name]=field
    else:
        informed_fields[field_name]=field

def make_energy_itrans_plot(list_of_tuples):
   
    df = pd.DataFrame(list_of_tuples, columns =['energy', 'itrans', 'i0'])
    df['energy']=df['energy'].astype('float64')       
    df['itrans']= df['itrans'].astype('float64')   
    df['ratio']=np.log(df['i0'].div(df['itrans'])) 
    
    fig = px.line(df, x="energy", y='ratio', title='',
                  labels={
                     "energy": "Energy [eV]",
                     "ratio": "I0 / I-trans"
                 },
                  )
    plt_div = opy.plot(fig, output_type='div')
    
    return plt_div

def experiment_detail(request, pk):
    experiment = Experiment.objects.get(pk=int(pk))
    
    informed_dic = {}
    not_informed_dic = {}
    
    add_experiment_detail('Experiment type',                  experiment.TYPES[int(experiment.experiment_type)-1][1]      , informed_dic,  not_informed_dic   )
    add_experiment_detail('Element symbol',                   experiment.element_symbol                 , informed_dic,  not_informed_dic   )    
    add_experiment_detail('Element edge',                     experiment.element_edge                   , informed_dic,  not_informed_dic   )
    add_experiment_detail('Mono name',                        experiment.mono_name                      , informed_dic,  not_informed_dic   )
    add_experiment_detail('Mono D-spacing',                   experiment.mono_d_spacing                 , informed_dic,  not_informed_dic   )
    add_experiment_detail('Sample formula',                   experiment.sample_formula                 , informed_dic,  not_informed_dic   )
    add_experiment_detail('Sample name',                      experiment.sample_name                    , informed_dic,  not_informed_dic   )
    add_experiment_detail('Sample preparation',               experiment.sample_prep                    , informed_dic,  not_informed_dic   )
    add_experiment_detail('Sample temperature',               experiment.sample_temperature             , informed_dic,  not_informed_dic   )
    add_experiment_detail('Sample reference',                 experiment.sample_reference               , informed_dic,  not_informed_dic   )
    add_experiment_detail('Facility name',                    experiment.facility_Name                  , informed_dic,  not_informed_dic   )
    add_experiment_detail('Beamline name',                    experiment.facility_Name                  , informed_dic,  not_informed_dic   )     
    add_experiment_detail('Beamline X-ray source',            experiment.beamline_xray_source           , informed_dic,  not_informed_dic   )
    add_experiment_detail('Beamline storage ring current',    experiment.beamline_Storage_Ring_Current  , informed_dic,  not_informed_dic   )
    add_experiment_detail('Beamline I0',                      experiment.beamline_I0                    , informed_dic,  not_informed_dic   )
    add_experiment_detail('Beamline I1',                      experiment.beamline_I1                    , informed_dic,  not_informed_dic   )
    add_experiment_detail('Detector I0',                      experiment.detector_I0                    , informed_dic,  not_informed_dic   )
    add_experiment_detail('Detector I1',                      experiment.detector_I1                    , informed_dic,  not_informed_dic   )
    add_experiment_detail('Detector I2',                      experiment.detector_I2                    , informed_dic,  not_informed_dic   )
    add_experiment_detail('Scan start time',                  experiment.scan_start_time                , informed_dic,  not_informed_dic   )
    add_experiment_detail('Scan end time',                    experiment.scan_end_time                  , informed_dic,  not_informed_dic   )
    add_experiment_detail('Scan parameters start',            experiment.scanParameters_Start           , informed_dic,  not_informed_dic   )
    add_experiment_detail('Scan parameters scan type',        experiment.scanParameters_ScanType        , informed_dic,  not_informed_dic   )
    add_experiment_detail('Scan parameters E0',               experiment.scanParameters_E0              , informed_dic,  not_informed_dic   )
    add_experiment_detail('Scan parameters legend',           experiment.scanParameters_Legend          , informed_dic,  not_informed_dic   )
    add_experiment_detail('Scan parameters region1',          experiment.scanParameters_Region1         , informed_dic,  not_informed_dic   )
    add_experiment_detail('Scan parameters region2',          experiment.scanParameters_Region2         , informed_dic,  not_informed_dic   )
    add_experiment_detail('Scan parameters region3',          experiment.scanParameters_Region3         , informed_dic,  not_informed_dic   )
    add_experiment_detail('Scan parameters end',              experiment.scanParameters_End             , informed_dic,  not_informed_dic   )
    add_experiment_detail('Data licence',                     "Not Informed"                            , informed_dic,  not_informed_dic   )                                                                              
       
    
    if experiment.i0 != None and "Not Informed" in experiment.i0:
        table = list( zip( 
            experiment.energy.split(","),
            experiment.itrans.split(","),
            experiment.i0.split(",")  
            ) 
        )
    else:
        table = list( zip( 
            experiment.energy.split(","),
            experiment.itrans.split(","),
        ) )
    
    
    graph=make_plot(table)

    return render(request, 'experiment_detail.html',{
        'experiment': experiment,
        'energy_itrans_i0_table': energy_itrans_i0_table,
        'informed_fields': informed_dic,
        'not_informed_fields': not_informed_dic,
        'graph':graph
        })

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


def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'registration/signup.html', {'form': form})    
   
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('login')
        else:
            #return render(request, 'usuario/register.html', {'form': form})
            return render(request, 'registration/signup.html', form)  

class SignUpView(CreateView):
    #form_class = UserCreationForm
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class ChangeAccountView(UpdateView):
    model = User
    fields = ["first_name","last_name","web_page","country","state","city"]
    success_url = reverse_lazy("index")
    template_name = "registration/change_account.html"

# class AddExperiment(CreateView):
#     form_class = AddExperiment
#     template_name = "add_experiment.html"
#     success_url = reverse_lazy('user-data')

#     def form_valid(self, form):
#         instance = form.save(commit=False)
#         instance.user = self.request.user
#         instance.save()
#         return super().form_valid(form)

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
    
class AddNormalization(CreateView):
    model = Normalization
    fields = '__all__'
    template_name = "normalization_data.html"
    success_url = reverse_lazy('plotly_chart')
    
def download_file(caminho_arquivo):
    
    with open(caminho_arquivo, 'rb') as file:
        file_content = file.read()
    
    content_type, _ = mimetypes.guess_type(caminho_arquivo)
    if content_type is None:
        content_type = 'text/plain'
    
    response = HttpResponse(file_content, content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename=dado_normalizado.txt'
    
    return response
       
def normalize_file(request):
    # Essa é a função que está sendo utilizada na aba de normalização
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            # Verifique o tipo de arquivo, se necessário
            if file.name.endswith('.txt') or file.name.endswith('.csv'):
                # Lê o arquivo com pandas
                try:
                    with open(os.path.join('db_xanes', str(file)), "rb") as fl:
                        result = detect(fl.read())
                        encoding = result["encoding"]

                    with open(os.path.join('db_xanes', str(file)), "r", encoding=encoding) as f:
                        data = f.read()
                    data_io = StringIO(data)
                    df = pd.read_csv(data_io, sep="\t", header=0)

                except:
                    with open(os.path.join('db_xanes', str(file)), "rb") as fl:
                        result = detect(fl.read())
                        encoding = result["encoding"]

                    with open(os.path.join('db_xanes', str(file)), "r", encoding=encoding) as f:
                        data = f.read()
                    data = re.sub(r"\s{2,}", " ", data)
                    data_io = StringIO(data)
                    df = pd.read_csv(data_io, sep=" ", header=0)

                # Exclue as colunas vazias
                df = df.dropna(axis=1)        

                # Definição do intervalo da faixa inicial (restrição)

                background = df[0:20]

                # Tratamento dos dados usando um fit de modelo linear

                modelo_linear = LinearModel()
                dados_x = background.iloc[:, 0].values
                dados_y = background.iloc[:, 1].values

                params_linear = modelo_linear.guess(dados_y, x=dados_x)

                resultado_fit = modelo_linear.fit(dados_y, params_linear, x=dados_x)

                # Extrapolação para todo o intervalo do espectro

                xwide = df.iloc[:, 0]
                predicted_faixa_inicial = modelo_linear.eval(resultado_fit.params, x=xwide)

                # Ajuste da faixa final XANES utilizando fit linear

                resultados = []
                slope_min = 1000

                # Loop para definir o intervalo de pontos na faixa final

                for npt in range(-20, -100, -1):
                    np_init = npt
                    np_end = -1
                    final_medida = df.iloc[np_init:np_end]
                    faixa_final = df[np_init:np_end]
                    modelo_linear = LinearModel()
                    dados_x = faixa_final.iloc[:, 0].values
                    dados_y = faixa_final.iloc[:, 1].values

                    params_linear = modelo_linear.guess(dados_y, x=dados_x)
                    resultado_fit = modelo_linear.fit(dados_y, params_linear, x=dados_x)

                    resultados.append([npt, resultado_fit.best_values['slope']])

                    # Identificação do menor valor dentro do intervalo de fit

                    if abs(resultado_fit.best_values['slope']) < slope_min:
                        slope_min = abs(resultado_fit.best_values['slope'])
                        npt_min = npt

                # Aplicação do fit linear

                final_medida = df.iloc[npt_min:np_end]
                faixa_final = df[npt_min:np_end]
                modelo_linear = LinearModel()
                dados_x = faixa_final.iloc[:, 0].values
                dados_y = faixa_final.iloc[:, 1].values

                params_linear = modelo_linear.guess(dados_y, x=dados_x)
                resultado_fit_final = modelo_linear.fit(dados_y, params_linear, x=dados_x)

                # Extrapolação do fit no intervalo da faixa final para todo o intervalo do espectro

                xwide = df.iloc[:, 0]
                predicted_faixa_final = modelo_linear.eval(resultado_fit_final.params, x=xwide)

                absorcao = df.iloc[:, 1]
                nova_curva = absorcao - predicted_faixa_inicial

                # Ajuste final para todos os dados de absorção do espectro

                fit_final = absorcao/predicted_faixa_final

                # Derivada para encontrar o ponto E0

                x = [df.iloc[:, 0]]
                y =  [df.iloc[:, 1]]
                dydx = diff(y)/diff(x)

                E0 = np.amax(dydx[0])
                local = np.argmax(dydx[0])
                E0x = x[0][local]

                dydx = diff(fit_final)/diff(xwide)

                E0 = np.amax(dydx)
                local = np.argmax(dydx)
                E0x = xwide[local]

                # Interpolação para obter o ponto na extrapolação da pré-borda e pós-borda referente ao E0

                f = interp1d(xwide, predicted_faixa_inicial)
                ponto_borda_inicial = f(E0x)
                g = interp1d(xwide, predicted_faixa_final)
                ponto_borda_final = g(E0x)

                # Normalização dos dados de absorção de raio x pela diferença do edge jump

                edge_jump = abs(ponto_borda_final - ponto_borda_inicial)
                
                absorcao_normalizada = []

                normalizado = absorcao/edge_jump
                
                absorcao_normalizada.append(normalizado)
                
                pasta_destino = "./normalization"
                os.makedirs(pasta_destino, exist_ok=True)
                
                file_name, ext = os.path.splitext(str(file))

                nome_arquivo = f"{file_name}_normalizado.txt"
                
                caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
                
                with open(caminho_arquivo, "w") as arquivo:
                    # Escreve o cabeçalho das colunas
                    arquivo.write("Energia\tAbsorção\n")            
                    for i in range(0,len(xwide)):
                        arquivo.write(f"{xwide.iloc[i]}\t{normalizado[i]}\n")
                        
                df = pd.read_csv(caminho_arquivo, delimiter='\t', encoding='latin1')  # Leia o arquivo em um DataFrame pandas
        
                data_reference = go.Scatter(x=df.iloc[:,0], y=df.iloc[:,1], mode='lines',name=nome_arquivo.replace(".txt", ""), line=dict(color=request.POST.get('line_color', '#0000FF')))
                fig = go.Figure(data=go.Scatter(x=df.iloc[:,0], y=df.iloc[:,1], mode='lines', ))
            
                title = request.POST.get('title', 'Gráfico Plotly')
                bg_color = request.POST.get('bg_color', 'white')
                grid_color = request.POST.get('grid_color', 'lightgray')
                line_color = request.POST.get('line_color', 'blue')
                xaxis_title = request.POST.get('xaxis_title', 'Eixo X')
                yaxis_title = request.POST.get('yaxis_title', 'Eixo Y')
                
                fig.update_layout(
                    title=title,
                    plot_bgcolor=bg_color,
                    xaxis_title = xaxis_title,
                    yaxis_title = yaxis_title,
                    xaxis=dict(gridcolor=grid_color),
                    yaxis=dict(gridcolor=grid_color)
                )
                
                fig.update_traces(line=dict(color=line_color))
            
                plot_div = fig.to_html(full_html=False)
                             
                #return download_file(caminho_arquivo)
                # Se habilitada faz o download, mas não gera o gráfico
                                      
            #return render(request, 'plotly_chart.html', {'plot_div': plot_div})
            return render(request, 'plotly_chart.html', {
                'plot_div': plot_div,
                'title': title,
                'bg_color': bg_color,
                'grid_color': grid_color,
                'line_color': line_color,
                'xaxis_title': xaxis_title,
                'yaxis_title': yaxis_title
            })
            

            '''

            # Obtem a lista de tuplas de duas listas e mescle-as usando o zip

            for i in range(len(xwide)):
                print(xwide.iloc[i], normalizado[i])

                lista_de_tuplas = zip(xwide.iloc[i], normalizado[i])

            # converte uma lista de tuplas num DataFrame
                df_normalized = pd.DataFrame(lista_de_tuplas, columns=['Energia', 'Absorção'])

            # Faça algo com o DataFrame normalizado (por exemplo, salvá-lo em um arquivo ou exibi-lo na página)
            return render(request, 'result.html', {'df_normalized': df_normalized})

        for i in range(0,len(xwide)):
            #print(xwide.iloc[i],normalizado[i])
            arquivo.write(f"{xwide.iloc[i]}\t{normalizado[i]}\n")
            '''
            if os.path.exists(caminho_arquivo):
                return download_file(caminho_arquivo) # ao rodar o código não passa por esse if
            
        else:
            return render(request, 'error.html', {'error_message': 'Formato de arquivo inválido. Por favor, envie um arquivo .txt ou .csv.'})
            
    return render(request, 'normalization_data.html')


def handle_uploaded_file(uploaded_file): # Para poder ler o arquivo na função read_file
    path = default_storage.save('temp/' + uploaded_file.name, ContentFile(uploaded_file.read()))
    temp_file_path = os.path.join(default_storage.location, path)
    df, header = read_file(temp_file_path)
    os.remove(temp_file_path)
    return (df, header)

# element_s = dicio["Element"]["symbol"], element_e = dicio["Element"]["edge"]

def handle_uploaded_file_xdi(user_id, PostedDataForm, xdi_file):
    path = default_storage.save('XDIs/' + xdi_file.name, ContentFile(xdi_file.read()))
    xdi_filePath = path

    caminho_arquivo = path
    dicio, valores_tabela, energy, i0, itrans, irefer = parse_xdi_content(caminho_arquivo)

    try:
        experiment_title = PostedDataForm['experiment_title']
    except KeyError:
        experiment_title = "Not Informed"
    try:
        experiment_type = PostedDataForm['experiment_type']
    except KeyError:
        experiment_type = "Not Informed"

    try:
        doi = PostedDataForm['doi']
    except KeyError:
        doi = "Not Informed"

    try:
        additional_info = PostedDataForm['additional_info']
    except KeyError:
        additional_info = "Not Informed"

    try:
        element_symbol = dicio["Element"]["symbol"]
    except KeyError:
        element_symbol = "Not Informed"

    try:
        element_edge = dicio["Element"]["edge"]
    except KeyError:
        element_edge = "Not Informed"

    try:
        mono_d_spacing = dicio["Mono"]["d_spacing"]
    except KeyError:
        mono_d_spacing = "Not Informed"

    try:
        mono_name = dicio["Mono"]["name"]
    except KeyError:
        mono_name = "Not Informed"

    try:
        sample_formula = dicio["Sample"]["formula"]
    except KeyError:
        sample_formula = "Not Informed"

    try:
        sample_name = dicio["Sample"]["name"]
    except KeyError:
        sample_name = "Not Informed"

    try:
        sample_prep = dicio["Sample"]["prep"]
    except KeyError:
        sample_prep = "Not Informed"

    try:
        sample_temperature = dicio["Sample"]["temperature"]
    except KeyError:
        sample_temperature = "Not Informed"

    try:
        sample_reference = dicio["Sample"]["reference"]
    except KeyError:
        sample_reference = "Not Informed"

    try:
        detector_I0 = dicio["Detector"]["I0"]
    except KeyError:
        detector_I0 = "Not Informed"

    try:
        detector_I1 = dicio["Detector"]["I1"]
    except KeyError:
        detector_I1 = "Not Informed"

    try:
        detector_I2 = dicio["Detector"]["I2"]
    except KeyError:
        detector_I2 = "Not Informed"
    try:
        facility_Name = dicio["Facility"]["name"]
    except KeyError:
        facility_Name = "Not Informed"

    try:
        beamline_xray_source = dicio["Beamline"]["xray_source"]
    except KeyError:
        beamline_xray_source = "Not Informed"

    try:
        beamline_Storage_Ring_Current = dicio["Beamline"]["Storage_Ring_Current"]
    except KeyError:
        beamline_Storage_Ring_Current = "Not Informed"

    try:
        beamline_I0 = dicio["Beamline"]["I0"]
    except KeyError:
        beamline_I0 = "Not Informed"

    try:
        beamline_I1 = dicio["Beamline"]["I1"]
    except KeyError:
        beamline_I1 = "Not Informed"

    try:
        scan_start_time = dicio["Scan"]["start_time"]
    except KeyError:
        scan_start_time = "Not Informed"

    try:
        scan_end_time = dicio["Scan"]["end_time"]
    except KeyError:
        scan_end_time = "Not Informed"

    try:
        scanParameters_Start = dicio["ScanParameters"]["Start"]
    except KeyError:
        scanParameters_Start = "Not Informed"

    try:
        scanParameters_ScanType = dicio["ScanParameters"]["ScanType"]
    except KeyError:
        scanParameters_ScanType = "Not Informed"

    try:
        scanParameters_E0 = dicio["ScanParameters"]["E0"]
    except KeyError:
        scanParameters_E0 = "Not Informed"

    try:
        scanParameters_Legend = dicio["ScanParameters"]["Legend"]
    except KeyError:
        scanParameters_Legend = "Not Informed"

    try:
        scanParameters_Region1 = dicio["ScanParameters"]["Region1"]
    except KeyError:
        scanParameters_Region1 = "Not Informed"

    try:
        scanParameters_Region2 = dicio["ScanParameters"]["Region2"]
    except KeyError:
        scanParameters_Region2 = "Not Informed"

    try:
        scanParameters_Region3 = dicio["ScanParameters"]["Region3"]
    except KeyError:
        scanParameters_Region3 = "Not Informed"

    try:
        scanParameters_End = dicio["ScanParameters"]["End"]
    except KeyError:
        scanParameters_End = "Not Informed"
    try:
        energy = energy
    except KeyError:
        energy = "Not Informed"
    try:
        i0 = i0
    except KeyError:
        i0 = "Not Informed"
    try:
        itrans = itrans
    except KeyError:
        itrans = "Not Informed"
    # try:
    #     irefer = irefer
    # except KeyError:
    #     irefer = "Not Informed"

    
    Experiment.objects.create(
        user_id                       = user_id,
        xdi_file                      = xdi_filePath,
        experiment_title              = experiment_title,
        experiment_type               = experiment_type,
        doi                           = doi,
        additional_info               = additional_info,
        element_symbol                = element_symbol,
        element_edge                  = element_edge,
        mono_d_spacing                = mono_d_spacing,
        mono_name                     = mono_name,
        sample_formula                = sample_formula,
        sample_name                   = sample_name,
        sample_prep                   = sample_prep,
        sample_temperature            = sample_temperature,
        sample_reference              = sample_reference,
        detector_I0                   = detector_I0,
        detector_I1                   = detector_I0,
        detector_I2                   = detector_I0,
        facility_Name                 = facility_Name,
        beamline_xray_source          = beamline_xray_source,
        beamline_Storage_Ring_Current = beamline_Storage_Ring_Current,
        beamline_I0                   = beamline_I0,
        beamline_I1                   = beamline_I0,
        scan_start_time               = scan_start_time,
        scan_end_time                 = scan_end_time,
        scanParameters_Start          = scanParameters_Start,
        scanParameters_ScanType       = scanParameters_ScanType,
        scanParameters_E0             = scanParameters_E0,
        scanParameters_Legend         = scanParameters_Legend,
        scanParameters_Region1        = scanParameters_Region1,
        scanParameters_Region2        = scanParameters_Region1,
        scanParameters_Region3        = scanParameters_Region1,
        scanParameters_End            = scanParameters_End,
        energy = energy,
        i0 = i0,
        itrans = itrans,
        # reference = irefer

        )

def AddExperiment(request):
    if request.method == 'POST':
        form = UploadXDIForm(request.POST, request.FILES)
        handle_uploaded_file_xdi(request.user.id, request.POST, request.FILES['xdi_file'])
        return redirect('user-data')
    else:
        form = UploadXDIForm()
    return render(request, 'upload_xdi.html', {'form': form})

def parse_xdi_content(caminho_arquivo):
    secoes = [
    "Element.symbol",
    "Element.edge",
    "Mono.d_spacing",
    "Mono.name",
    "Sample.formula",
    "Sample.name",
    "Sample.prep",
    "Sample.temperature",
    "Sample.reference",
    "Detector.I0",
    "Detector.I1",
    "Detector.I2",
    "Facility.Name",
    "Beamline.Name",
    "Beamline.name",
    "Facility.name",
    "Beamline.xray_source",
    "Beamline.Storage_Ring_Current",
    "Beamline.I0",
    "Beamline.I1",
    "Scan.start_time",
    "Scan.end_time",
    "ScanParameters.Start",
    "ScanParameters.ScanType",
    "ScanParameters.E0",
    "ScanParameters.Legend",
    "ScanParameters.Region1",
    "ScanParameters.Region2",
    "ScanParameters.Region3",
    "ScanParameters.End"
    ]
    regex = '|'.join(map(re.escape, secoes))
    with open(caminho_arquivo, 'r') as texto:
        linhas = texto.read()
        matches = re.findall(f'({regex}):\\s*(.*)', linhas)

    valores = {}
    for match in matches:
        secao, valor = match[0], match[1]
        secao_primaria, secao_secundaria = secao.split('.')
        if secao_primaria not in valores:
            valores[secao_primaria] = {}
        valores[secao_primaria][secao_secundaria] = valor
    match = re.search(r'#---+', linhas, re.MULTILINE)
    if match:
        tabela_inicio = match.end()
        tabela_linhas = linhas[tabela_inicio:].strip().split('\n')

        valores_tabela = []
        for linha in tabela_linhas:
            if re.match(r'(\s+\d+\.\d+\s+){2,4}', linha):
                valores_tabela.append([float(valor) for valor in linha.split()])
    else:
        # Se não encontrar o início da tabela, definir valores_tabela como None
        valores_tabela = None

    energy = []
    i0 = []
    itrans = []
    irefer = []

    # Abrindo o arquivo e lendo seu conteúdo
    with open(caminho_arquivo, 'r') as arquivo:
        # Iterando sobre as linhas do arquivo
        for linha in arquivo:
            # Ignorando as linhas que começam com #
            if linha.startswith('#'):
                continue
            # Dividindo a linha em valores individuais
            val_lin = re.findall(r'\S+', linha)
            # Verificando se a linha contém os valores esperados
            if len(val_lin) >= 4:
                # Extraindo os valores de cada coluna e armazenando nas listas correspondentes
                energy.append(float(val_lin[0]))
                i0.append(float(val_lin[1]))
                itrans.append(float(val_lin[2]))
                irefer.append(float(val_lin[3]))
    return valores, valores_tabela, energy, i0 ,itrans, irefer

def spectra_comparison(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            print("file",file)
            if not (file.name.endswith('.xdi')): # Verificando o tipo de arquivo
                raise TypeError('File must be .xdi')
            
            abs_element = 'Fe'#str(request.POST.get('abs_element')) #Por que está dando errado?
            edge = str(request.POST.get('edge'))

            header, df = handle_uploaded_file(file)

            try:
                n_materials = int(request.POST.get('num_materials'))
                ga_combinator_dic = ga(n_materials, abs_element, edge, df)
            except Exception as e:
                print(f'Error while running ga_combinator.py: {e}')

            #plot
            array_with_max_fitness = ga_combinator_dic['array_with_max_fitness']
            target_spectrum = ga_combinator_dic['target_spectrum']
            funcs_keys_with_max_fitness = ga_combinator_dic['funcs_keys_with_max_fitness']
            spectra = ga_combinator_dic['spectra']
            coeffs_with_max_fitness = ga_combinator_dic['coeffs_with_max_fitness']
            gen = ga_combinator_dic['gen']
            best_result = ga_combinator_dic['best_result']
            domain = ga_combinator_dic['domain']

            title = request.POST.get('title', 'Gráfico Plotly')
            bg_color = request.POST.get('bg_color', 'white')
            grid_color = request.POST.get('grid_color', 'lightgray')
            line_color = request.POST.get('line_color', 'blue')
            xaxis_title = request.POST.get('xaxis_title', 'Eixo X')
            yaxis_title = request.POST.get('yaxis_title', 'Eixo Y')

            fig = go.Figure()

            layout = go.Layout(
                title=f'{title} | Generation {gen + 1} | Best Result = {best_result[2:]}',
                showlegend=True,
                plot_bgcolor=bg_color,
                xaxis=dict(gridcolor=grid_color),
                yaxis=dict(gridcolor=grid_color),
                legend=dict(orientation="h"),
                xaxis_title=xaxis_title,
                yaxis_title=yaxis_title
            )

            trace_names = []

            trace = go.Scatter(x=domain, y=array_with_max_fitness, mode='lines', line=dict(width=1.5, dash='dash', color=line_color))
            fig.add_trace(trace)
            trace_names.append('Max fitness')

            trace = go.Scatter(x=domain, y=target_spectrum, mode='lines', line=dict(width=2, color=request.POST.get('line_color_reference')))
            fig.add_trace(trace)
            trace_names.append('Target spectrum')

            for func in range(len(funcs_keys_with_max_fitness)):
                trace = go.Scatter(x=domain, y=spectra[funcs_keys_with_max_fitness[func]] * coeffs_with_max_fitness[func], mode='lines', line=dict(width=0.5, dash='dot'))
                fig.add_trace(trace)
                trace_names.append(funcs_keys_with_max_fitness[func])
   
            for i, name in enumerate(trace_names):
                fig.data[i].name = name

            fig.update_layout(layout)

            fig.update_xaxes(showgrid=True)
            fig.update_yaxes(showgrid=True)

            plot_div = fig.to_html(full_html=False)

        return render(request, 'plotly_chart.html', {
                'plot_div': plot_div,
                'title': title,
                'bg_color': bg_color,
                'grid_color': grid_color,
                'line_color': line_color,
                'xaxis_title': xaxis_title,
                'yaxis_title': yaxis_title
            })

    return render(request, 'comparison_data.html')


def plotly_chart(request):

    # Dados do gráfico
    path = 'C:\JupyterLab\INICIAÇÃO A PESQUISA CIENTÍFICA\Cruzeiro-do-Sul-Database\cruzeiro_do_sul_db\db_xanes'

    def load_graph(file_path):
        with open(file_path, 'r') as file:
            data = file.readlines()[1:]  # Skip the first line
            graph = [list(map(float, value.strip().split())) for value in data]
        return np.array(graph)

    reference_file = file_path #'C:\JupyterLab\INICIAÇÃO A PESQUISA CIENTÍFICA\DADOS NORMALIZADOS\Al2Fe(SiO5)2_py_out_conv.txt_normalizado.txt'

    reference_graph = load_graph(reference_file)

    dados_x = reference_graph[:, 0]
    dados_y = reference_graph[:, 1]


    # Criação do gráfico
    trace = go.Scatter(x=dados_x, y=dados_y, mode='lines')
    data = [trace]
    layout = go.Layout(title='Exemplo de Gráfico Plotly')
    figure = go.Figure(data=data, layout=layout)

    # Geração do código HTML para o gráfico
    div = opy.plot(figure, auto_open=False, output_type='div')

    # Renderização do template com o gráfico
    return render(request, 'plotly_chart.html', {'plot_div': div})
'''

def plot_graph(request):
    if request.method == 'POST':
        file = request.FILES['file']
        # Salve o arquivo temporariamente
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_file:
            temp_file.write(file.read())
            temp_file.flush()
            # Leia o arquivo em um DataFrame pandas
            df = pd.read_csv(temp_file.name, delimiter='\t')  # Altere o delimitador conforme necessário
            # Verifique se as colunas "x" e "y" estão presentes no DataFrame
            if 'Energia' in df.columns and 'Absorção' in df.columns:
                # Crie um gráfico Plotly
                fig = go.Figure(data=go.Scatter(x=df['Energia'], y=df['Absorção'], mode='lines'))
                # Salve o gráfico em um arquivo HTML temporário
                with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as plot_file:
                    fig.write_html(plot_file.name)
                    plot_file.flush()
                    # Obtenha o caminho absoluto do arquivo HTML
                    plot_file_path = os.path.abspath(plot_file.name)
                    # Redirecione para a URL com o gráfico Plotly
                    return redirect('plot_result', plot_file_path=plot_file_path)
            else:
                # Colunas "x" ou "y" não estão presentes no DataFrame
                return render(request, 'upload.html', {'error_message': 'Colunas "x" e "y" não encontradas no arquivo.'})
    else:
        return render(request, 'upload.html')
    '''

def plot_result(request, plot_file_path):
    return render(request, 'plot_result.html', {'plot_file_path': plot_file_path})
