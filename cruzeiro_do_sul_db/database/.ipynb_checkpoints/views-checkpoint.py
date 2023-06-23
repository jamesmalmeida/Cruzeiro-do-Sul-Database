from django.shortcuts import render, redirect
from django.http import FileResponse
from django.urls import reverse_lazy
from .forms import UserCreationForm, UserChangeForm, AddExperiment
from .models import Experiment, Beamline, Facility, User, Element, Normalization, Comparison, normalization_function
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView, ListView
from django.db.models import Q 
from functools import reduce
import operator
import plotly.offline as opy
import plotly.graph_objs as go
import tempfile
import os
import pandas as pd
import numpy as np
from lmfit.models import LinearModel
from .forms import FileUploadForm
from numpy import diff
from scipy.interpolate import interp1d
from django.http import HttpResponse
import mimetypes

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
    fields = ["first_name","last_name","web_page","country","state","city"]
    success_url = reverse_lazy("index")
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
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            # Verifique o tipo de arquivo, se necessário
            if file.name.endswith('.txt') or file.name.endswith('.csv'):
                # Lê o arquivo com pandas
                df = pd.read_csv(file, sep=' ', header=0)

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
                
                pasta_destino = "C:\JupyterLab\INICIAÇÃO A PESQUISA CIENTÍFICA\Cruzeiro-do-Sul-Database\cruzeiro_do_sul_db\\normalization"
                os.makedirs(pasta_destino, exist_ok=True)
                
                nome_arquivo = f"{file}_normalizado.txt"
                
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

def normalize(df, file):
    # Lê o arquivo com pandas
    #df = pd.read_csv(file, sep=' ', header=0)

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

    pasta_destino = "C:\JupyterLab\INICIAÇÃO A PESQUISA CIENTÍFICA\Cruzeiro-do-Sul-Database\cruzeiro_do_sul_db\\normalization"
    os.makedirs(pasta_destino, exist_ok=True)

    nome_arquivo = f"{file}_normalizado.txt"#_normalizado.txt"

    caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)

    with open(caminho_arquivo, "w") as arquivo:
        # Escreve o cabeçalho das colunas
        arquivo.write("Energy\tAbsorption\n")            
        for i in range(0,len(xwide)):
            arquivo.write(f"{xwide.iloc[i]}\t{normalizado[i]}\n")
    return caminho_arquivo

def spectra_comparison(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            print("file",file)
            # Verifique o tipo de arquivo, se necessário
            #if file.name.endswith('.txt') or file.name.endswith('.csv'):
            
            folder_path = 'C:\JupyterLab\INICIAÇÃO A PESQUISA CIENTÍFICA\Cruzeiro-do-Sul-Database\cruzeiro_do_sul_db\\normalization'
            
            file_path = os.path.join(folder_path, str(f"{file}_normalizado.txt"))
            
            df_nao_normalizado = pd.read_csv(file, sep=' ', header=0)
            df = pd.read_csv(normalize(df_nao_normalizado, str(file)), sep='\t')
            def load_graph(file_path):
                with open(file_path, 'r') as file:
                    data = file.readlines()[1:]  # Skip the first line
                    graph = [list(map(float, value.strip().split())) for value in data]
                return np.array(graph)

            def calculate_rmse(graph1, graph2):
                interpolated_graph2 = interp1d(graph2[:, 0], graph2[:, 1], kind='linear', fill_value='extrapolate')
                interpolated_values = interpolated_graph2(graph1[:, 0])
                return np.sqrt(np.sum((graph1[:, 1] - interpolated_values) ** 2))


                fig = go.Figure(data=go.Scatter(x=df.iloc[:,0], y=df.iloc[:,1], mode='lines'))

                title = request.POST.get('title', 'Gráfico Plotly')
                bg_color = request.POST.get('bg_color', 'white')
                grid_color = request.POST.get('grid_color', 'lightgray')
                line_color = request.POST.get('line_color', 'blue')
                xaxis_title = request.POST.get('xaxis_title', 'Eixo X')
                yaxis_title = request.POST.get('yaxis_title', 'Eixo Y')

                fig.update_layout(
                    title=title,
                    showlegend=legend,
                    plot_bgcolor=bg_color,
                    xaxis=dict(gridcolor=grid_color),
                    yaxis=dict(gridcolor=grid_color)
                )

                fig.update_traces(line=dict(color=line_color))

                plot_div = fig.to_html(full_html=False)

            #def plot_graphs(reference_graph, matching_graph):
                #plt.plot(reference_graph[:, 0], reference_graph[:, 1], label='Reference Graph')
                #plt.plot(matching_graph[:, 0], matching_graph[:, 1], label='Matching Graph')
                #plt.legend()
                #plt.xlabel('X-axis')
                #plt.ylabel('Y-axis')
                #plt.title('Comparison of Graphs')
                #plt.show()
                

            reference_file = file_path#df
            folder_path = 'C:\JupyterLab\INICIAÇÃO A PESQUISA CIENTÍFICA\Cruzeiro-do-Sul-Database\cruzeiro_do_sul_db\db_xanes'

            reference_graph = load_graph(reference_file)
            lowest_rmse = float('inf')
            matching_graph = None
            current_file = ""

            # Define the x-axis range to compare
            range_start = reference_graph[0,0]
            range_end = reference_graph[-1,0]

            for file_name in os.listdir(folder_path):
                if file_name.endswith('.txt'):
                    file_path = os.path.join(folder_path, file_name)
                    current_graph = load_graph(file_path)

                    # Filter graphs based on x-axis range
                    mask = (range_start <= current_graph[:, 0]) & (current_graph[:, 0] <= range_end)
                    current_graph = current_graph[mask]
                    #print(current_graph)

                    if current_graph.shape[0] > 0:  # Check if filtered graph has at least one data point
                        current_rmse = calculate_rmse(reference_graph, current_graph)
                        if current_rmse < lowest_rmse:
                            lowest_rmse = current_rmse
                            matching_graph = current_graph
                            current_file = file_name
            #else:
            #    return render(request, 'error.html', {'error_message': 'Formato de arquivo inválido. Por favor, envie um arquivo .txt ou .csv.'})
            
            
            print("current_file", str(current_file))
            
            path_match = os.path.join(folder_path, str(current_file))
            
            df_match = pd.read_csv(path_match, delimiter='\t', encoding='latin1')
            
            data_reference = go.Scatter(x=df.iloc[:,0], y=df.iloc[:,1], mode='lines', name=str(file).replace(".txt", ""), line=dict(color=request.POST.get('line_color_reference', '#0000FF')))
            data_matching = go.Scatter(x=df_match.iloc[:,0], y=df_match.iloc[:,1], mode='markers',name=current_file.replace(".txt", ""), line=dict(color=request.POST.get('line_color_similar', '#0000FF')))
            
            fig = go.Figure(data=[data_reference, data_matching])
            
            #fig = go.Figure(data=go.Scatter(x=df.iloc[:,0], y=df.iloc[:,1], mode='lines'))
            #fig = go.Figure(data=go.Scatter(x=df_match.iloc[:,0], y=df_match.iloc[:,1]))

            
            title = request.POST.get('title', 'Gráfico Plotly')
            bg_color = request.POST.get('bg_color', 'white')
            grid_color = request.POST.get('grid_color', 'lightgray')
            #line_color_reference = request.POST.get('line_color_reference', 'blue')
            #line_color_similar = request.POST.get('line_color_similar', 'blue')
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

            #fig.update_traces(line=dict(color=line_color_reference))
            #fig.update_traces(line=dict(color=line_color_similar))

            plot_div = fig.to_html(full_html=False)

            return render(request, 'plotly_chart.html', {
                'plot_div': plot_div,
                'title': title,
                'bg_color': bg_color,
                'grid_color': grid_color,
                #'line_color_reference': line_color_reference,
                #'line_color_similar': line_color_similar,
                'xaxis_title': xaxis_title,
                'yaxis_title': yaxis_title
            })
        
            '''
            
            plot_div = fig.to_html(full_html=False)
            return render(request, 'plotly_chart.html', {'plot_div': plot_div})
            
            '''

            if matching_graph is None:
                print("No matching graph found!")
            else:
                print(f"Matching graph found with RMSE: {lowest_rmse}")
                print(f"Espectros similares: {reference_file}, {current_file}")
                #plot_graphs(reference_graph, matching_graph)

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
