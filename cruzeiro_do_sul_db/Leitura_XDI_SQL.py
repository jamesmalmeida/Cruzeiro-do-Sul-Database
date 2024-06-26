#Nesse script está o loop para realizar a leitura do arquivo XDI e mandar seus metadados para o banco de dados


#Importando bibliotecas
import re
import sqlite3
import os
# Diretório que está seus arquivos
diretorio = "/home/ABTLUS/gustavo23000//Área de Trabalho/Clone_Base_Nova/Cruzeiro-do-Sul-Database/cruzeiro_do_sul_db/dados_campos_novos"
extensao_desejada = ".xdi" 
arquivos_com_extensao = [arquivo for arquivo in os.listdir(diretorio) if arquivo.endswith(extensao_desejada)]
lista_erros = []
lista_fluorescencia = []
# Loop para pegar cada arquivo do diretório, ler e mandar para base
for arquivo in arquivos_com_extensao:
    caminho_arquivo = arquivo
#############################################################################################################
############ Dados da XAS-Data-Library ######################################################################
############ Daqui até proxima marcação é rotina para Dados da Bae XAS ######################################
#############################################################################################################
    # secoes = [
    #     "Element.symbol",
    #     "Element.edge",
    #     "Mono.d_spacing",
    #     "Mono.name",
    #     "Sample.formula",
    #     "Sample.name",
    #     "Sample.prep",
    #     "Sample.temperature",
    #     "Sample.reference",
    #     "Detector.I0",
    #     "Detector.I1",
    #     "Detector.I2",
    #     "Facility.Name",
    #     "Beamline.Name",
    #     "Beamline.name",
    #     "Facility.name",
    #     "Beamline.xray_source",
    #     "Beamline.Storage_Ring_Current",
    #     "Beamline.I0",
    #     "Beamline.I1",
    #     "Scan.start_time",
    #     "Scan.end_time",
    #     "ScanParameters.Start",
    #     "ScanParameters.ScanType",
    #     "ScanParameters.E0",
    #     "ScanParameters.Legend",
    #     "ScanParameters.Region1",
    #     "ScanParameters.Region2",
    #     "ScanParameters.Region3",
    #     "ScanParameters.End"
    #     ]
    # regex = '|'.join(map(re.escape, secoes))

    # with open(caminho_arquivo, 'r') as texto:
    #     linhas = texto.read()
    #     matches = re.findall(f'({regex}):\\s*(.*)', linhas)
    # dicio = {}
    # for match in matches:
    #     secao, valor = match[0], match[1]
    #     secao_primaria, secao_secundaria = secao.split('.')
    #     if secao_primaria not in dicio:
    #         dicio[secao_primaria] = {}
    #     dicio[secao_primaria][secao_secundaria] = valor
        
    # match = re.search(r'#---+', linhas, re.MULTILINE)
    # if match:
    #     tabela_inicio = match.end()
    #     tabela_linhas = linhas[tabela_inicio:].strip().split('\n')
    #     valores_tabela = []
    #     for linha in tabela_linhas:
    #         if re.match(r'(\s+\d+\.\d+\s+){2,4}', linha):
    #             valores_tabela.append([float(valor) for valor in linha.split()])
    # else:
    #     # Se não encontrar o início da tabela, definir valores_tabela como None
    #     valores_tabela = None

    # with open(caminho_arquivo, "r") as arquivo:
    #     texto = arquivo.read()

    # # Encontrar nomes das colunas
    # nomes_colunas = re.findall(r"# Column\.\d+: (\w+)", texto)
    # # Separar as linhas de dados e criar dicionário associando cada valor ao seu respectivo nome de coluna
    # dados = {}
    # linhas = texto.splitlines()
    # match = re.search(r'#---+', texto, re.MULTILINE)
    # for nome in nomes_colunas:
    #     dados[nome] = []
    # if match:
    #     inicio = match.end()
    #     tab_linhas = texto[inicio:].strip().split('\n')
    #     for linha in tab_linhas:
    #         if re.match(r'(\s+\d+\.\d+\s+){2,4}', linha):
    #             valores = linha.split()
    #             for nome,valor in zip(nomes_colunas,valores):
    #                 dados[nome].append(float(valor))


    # try:
    #     energy = dados["energy"]
    # except KeyError:
    #     energy = None
    # try:
    #     i0 = dados["i0"]
    # except KeyError:
    #     i0 = None
    # try:
    #     itrans = dados["itrans"]
    # except KeyError:
    #     itrans = None
    # try:
    #     irefer = dados["irefer"]
    # except KeyError:
    #     irefer = None


    # try:
    #     energy = ",".join(str(element) for element in energy)
    # except TypeError:
    #     pass
    # try:
    #     i0 = ",".join(str(element) for element in i0)
    # except TypeError:
    #     pass
    # try:
    #     itrans = ",".join(str(element) for element in itrans)
    # except TypeError:
    #     pass
    # try:
    #     irefer = ",".join(str(element) for element in irefer)
    # except TypeError:
    #     pass

    # def xas_xanes(energy):
    #     maximo = max(energy)
    #     minimo = min(energy)
    #     num = float(maximo) - float(minimo)
    #     if num > 5 and num < 200:
    #         return 2
    #     else:
    #         return 1

    # energy_l = energy.split(',')
    # tipo = xas_xanes(energy_l)
    # title = "Populando_a_base"
    # # print(i0, arquivo)

    # try:
    #     element_symbol = dicio["Element"]["symbol"]
    # except KeyError:
    #     element_symbol = "Not Informed"

    # try:
    #     element_edge = dicio["Element"]["edge"]
    # except KeyError:
    #     element_edge = "Not Informed"
    # try:
    #     mono_d_spacing = dicio["Mono"]["d_spacing"]
    # except KeyError:
    #     mono_d_spacing = "Not Informed"
    # try:
    #     mono_name = dicio["Mono"]["name"]
    # except KeyError:
    #     mono_name = "Not Informed"
    # try:
    #     sample_formula = dicio["Sample"]["formula"]
    # except KeyError:
    #     sample_formula = "Not Informed"
    # try:
    #     sample_name = dicio["Sample"]["name"]
    # except KeyError:
    #     sample_name = "Not Informed"
    # try:
    #     sample_prep = dicio["Sample"]["prep"]
    # except KeyError:
    #     sample_prep = "Not Informed"
    # try:
    #     sample_temperature = dicio["Sample"]["temperature"]
    # except KeyError:
    #     sample_temperature = "Not Informed"
    # try:
    #     sample_reference = dicio["Sample"]["reference"]
    # except KeyError:
    #     sample_reference = "Not Informed"
    # try:
    #     detector_I0 = dicio["Detector"]["I0"]
    # except KeyError:
    #     detector_I0 = "Not Informed"
    # try:
    #     detector_I1 = dicio["Detector"]["I1"]
    # except KeyError:
    #     detector_I1 = "Not Informed"
    # try:
    #     detector_I2 = dicio["Detector"]["I2"]
    # except KeyError:
    #     detector_I2 = "Not Informed"
    # try:
    #     facility_Name = dicio["Facility"]["name"]
    # except KeyError:
    #     facility_Name = "Not Informed"
    # try:
    #     beamline_xray_source = dicio["Beamline"]["xray_source"]
    # except KeyError:
    #     beamline_xray_source = "Not Informed"
    # try:
    #     beamline_Storage_Ring_Current = dicio["Beamline"]["Storage_Ring_Current"]
    # except KeyError:
    #     beamline_Storage_Ring_Current = "Not Informed"
    # try:
    #     beamline_I0 = dicio["Beamline"]["I0"]
    # except KeyError:
    #     beamline_I0 = "Not Informed"
    # try:
    #     beamline_I1 = dicio["Beamline"]["I1"]
    # except KeyError:
    #     beamline_I1 = "Not Informed"
    # try:
    #     scan_start_time = dicio["Scan"]["start_time"]
    # except KeyError:
    #     scan_start_time = "Not Informed"
    # try:
    #     scan_end_time = dicio["Scan"]["end_time"]
    # except KeyError:
    #     scan_end_time = "Not Informed"
    # try:
    #     scanParameters_Start = dicio["ScanParameters"]["Start"]
    # except KeyError:
    #     scanParameters_Start = "Not Informed"
    # try:
    #     scanParameters_ScanType = dicio["ScanParameters"]["ScanType"]
    # except KeyError:
    #     scanParameters_ScanType = "Not Informed"
    # try:
    #     scanParameters_E0 = dicio["ScanParameters"]["E0"]
    # except KeyError:
    #     scanParameters_E0 = "Not Informed"
    # try:
    #     scanParameters_Legend = dicio["ScanParameters"]["Legend"]
    # except KeyError:
    #     scanParameters_Legend = "Not Informed"
    # try:
    #     scanParameters_Region1 = dicio["ScanParameters"]["Region1"]
    # except KeyError:
    #     scanParameters_Region1 = "Not Informed"
    # try:
    #     scanParameters_Region2 = dicio["ScanParameters"]["Region2"]
    # except KeyError:
    #     scanParameters_Region2 = "Not Informed"
    # try:
    #     scanParameters_Region3 = dicio["ScanParameters"]["Region3"]
    # except KeyError:
    #     scanParameters_Region3 = "Not Informed"
    # try:
    #     scanParameters_End = dicio["ScanParameters"]["End"]
    # except KeyError:
    #     scanParameters_End = "Not Informed"
    # try:
    #     energy = energy
    # except KeyError:
    #     energy = "Not Informed"
    # try:
    #     i0 = i0
    #     # print(i0)
    # except KeyError:
    #     # print(i0)
    #     i0 = "Not Informed"
    # try:
    #     itrans = itrans
    # except KeyError:
    #     itrans = "Not Informed"
    # try:
    #     irefer = irefer
    # except KeyError:
    #     irefer = "Not Informed"
    #     # irefer = irefer if irefer is not None else 'default_value'


    #############################################################################################################
    ############ Dados da XAS-Data-Library ######################################################################
    ############ Fim da Rotina ##################################################################################
    #############################################################################################################





    #############################################################################################################
    ############ Dados da SSHADE ################################################################################
    ############ Início da Rotina ###############################################################################
    #############################################################################################################



    contador = 0
    colunas = []
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
        "ScanParameters.End",
        "Citation.doi",
        "Citation.comments"
        ]
    regex = '|'.join(map(re.escape, secoes))

    with open(caminho_arquivo, 'r') as texto:
        linhas = texto.read()
        matches = re.findall(f'({regex}):\\s*(.*)', linhas)
    dicio = {}
    for match in matches:
        secao, valor = match[0], match[1]

        secao_primaria, secao_secundaria = secao.split('.')
        if secao_primaria not in dicio:
            dicio[secao_primaria] = {}
        dicio[secao_primaria][secao_secundaria] = valor

    match = re.search(r'#---+', linhas, re.MULTILINE)
    if match:
        tabela_inicio = match.end()
        tabela_linhas = linhas[tabela_inicio:].strip().split('\n')
        valores_tabela = []
        for linha in tabela_linhas:
            if re.match(r'\s*\d+\.\d+(?:E[+-]?\d+)?\s*', linha):
                valores_tabela.append([float(valor) for valor in linha.split()])
    else:
        # Se não encontrar o início da tabela, definir valores_tabela como None
        valores_tabela = None

    with open(caminho_arquivo, "r") as arquivo:

        texto = arquivo.read()

    # Encontrar nomes das colunas
    nomes_colunas = re.findall(r"# Column\.\d+: (\w+)", texto)

    # Separar as linhas de dados e criar dicionário associando cada valor ao seu respectivo nome de coluna
    dados = {}
    linhas = texto.splitlines()
    match = re.search(r'#---+', texto, re.MULTILINE)
    for nome in nomes_colunas:
        dados[nome] = []
    if match:
        inicio = match.end()
        tab_linhas = texto[inicio:].strip().split('\n')
        for linha in tab_linhas:
            if re.match(r'\s*\d+\.\d+(?:E[+-]?\d+)?\s*', linha):
                valores = linha.split()
                for nome,valor in zip(nomes_colunas,valores):
                    dados[nome].append(float(valor))

    try:
        energy_sshade = dados["energy"]

    except KeyError:
        energy_sshade = None

    try:
        fluor_sshade = dados['fluorescence_emission']

    except:
        fluor_sshade = None

    try:
        trans_sshade = dados['trasmission']


    except:
        trans_sshade = None
    try:
        raw_sshade = dados['raw']


    except:
        raw_sshade = None

    try:
        normalized_absorbance_sshade = dados['normalized_absorbance']

    except:
        normalized_absorbance_sshade = None

    try:
        energy_db = ",".join(str(element) for element in energy_sshade)
    
    except TypeError:
        pass
    try:
        trans_db = ",".join(str(element) for element in trans_sshade)
    
    except TypeError:
        pass
    try:
        fluor_db = ",".join(str(element) for element in fluor_sshade)
    
    except TypeError:
        pass
    try:
        raw_db = ",".join(str(element) for element in raw_sshade)
    
    except TypeError:
        pass
    
    try:
        normalized_absorbance_sshade_db = ",".join(str(element) for element in normalized_absorbance_sshade)
    
    except TypeError:
        pass
        
    def xas_xanes(energia):
            #print(f"O arquivo {arquivo} possui a energia {energia}") #DEBUG
            try:
                maximo = max(energia)
                minimo = min(energia)
                #print(maximo, minimo) #DEBUG


                num = float(maximo) - float(minimo)
                if num > 5 and num < 200:
                    print(f"O arquivo {caminho_arquivo} é XANES!")
                    return 2
                else:
                    return 1
            except:
                lista_erros.append(caminho_arquivo)
    
    tipo = xas_xanes(energy_sshade)

    title = "Populando_a_base"

    if tipo == 2:
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
            energy = energy_db
        except KeyError:
            energy = "Not Informed"
        try:
            itrans = trans_db

        except KeyError:
            itrans = "Not Informed"
        try:
            i0 = raw_db
        except KeyError:
            i0 = "Not Informed"
        try:
            ifluor = fluor_db
        except:
            ifluor = "Not Informed"
    #############################################################################################################
    ############ Dados da SSHADE ################################################################################
    ############ Fim da Rotina ##################################################################################
    #############################################################################################################


    # Comando SQL para mandar para o banco de dados

    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    # cursor.execute("ALTER TABLE database_experiment")
    # cursor.execute("ALTER COLUMN reference DROP NOT NULL;")

    # cursor.execute("DELETE FROM database_experiment")
    cursor.execute('''INSERT INTO database_experiment (experiment_type, experiment_title, xdi_file, additional_info, doi, user_id,element_symbol, element_edge, mono_d_spacing, mono_name, sample_formula, sample_name, sample_prep, sample_temperature, sample_reference, detector_I0, detector_I1, detector_I2, facility_Name, beamline_xray_source, beamline_Storage_Ring_Current, beamline_I0, beamline_I1, scan_start_time, scan_end_time, scanParameters_Start, scanParameters_ScanType, scanParameters_E0, scanParameters_Legend, scanParameters_Region1, scanParameters_Region2, scanParameters_Region3, scanParameters_End, energy,itrans, i0) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(tipo,title,f"XDIs/{caminho_arquivo}","Not informed", "Not informed", 2,element_symbol,element_edge,mono_d_spacing,mono_name,sample_formula,sample_name,sample_prep,sample_temperature,sample_reference,detector_I0,detector_I1,detector_I2,facility_Name,beamline_xray_source,beamline_Storage_Ring_Current,beamline_I0,beamline_I1,scan_start_time,scan_end_time,scanParameters_Start,scanParameters_ScanType,scanParameters_E0,scanParameters_Legend,scanParameters_Region1,scanParameters_Region2,scanParameters_Region3,scanParameters_End,energy,itrans,i0))
    
    connection.commit()
    connection.close()


######################## CUIDADO #################################
# Deletar dados da base  


# connection = sqlite3.connect('db.sqlite3')
# cursor = connection.cursor()
# cursor.execute("DELETE FROM database_experiment")
# connection.commit()
# connection.close()




