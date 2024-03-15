import pandas as pd
import pickle
from lmfit.models import LinearModel
from scipy.optimize import curve_fit
import os

def normalize(df, n=15, polyfit_start=0.5, polyfit_end=0.01):
    """
    Normalize a XANES/EXAFS DataFrame.

    Parameters:
    df (DataFrame): DataFrame containing XANES/EXAFS data to be normalized.
    n (int): Pre-edge range for normalization. Default is 15.
    polyfit_start (float): Starting point (0 to 1) for polynomial fitting. Default is 0.5.
    polyfit_end (float): Ending point (0 to 1) for polynomial fitting. Default is 0.01.

    Raises:
    ValueError: If polyfit_start is not greater than polyfit_end.

    Returns:
    DataFrame: Normalized DataFrame with added 'norm' column.
    """
    norm_df = df.copy()

    print(debug_1)
    
    if polyfit_end >= polyfit_start:
        raise ValueError("POLYFIT_START MUST BE HIGHER THAN POLYFIT END.")
    
    energy = df["energy eV"]
    if (df["i0"] < df["itrans"]).any():
        i0 = df["itrans"]
        itrans = df["i0"]
    else:
        i0 = df["i0"]
        itrans = df["itrans"]
    
    y = itrans / i0

    y = y.astype(float)
    energy = energy.astype(float)

    fit_model = LinearModel()
    params_linear = fit_model.guess(y[0:n], x=energy[0:n])
    resultado_fit = fit_model.fit(y[0:n], params_linear, x=energy[0:n])
    predicted = fit_model.eval(resultado_fit.params, x=energy)
    pre_edge_norm = y - predicted

    def polynomial(x, a, b, c):  # Polynomial to fit
        return a * x**2 + b * x + c

    n_data = len(energy)
    start = n_data - int(n_data * polyfit_start)
    end = n_data - int(n_data * polyfit_end)

    params, covariance = curve_fit(polynomial, energy[start:end], pre_edge_norm[start:end])

    a, b, c = params

    polynomial_values = polynomial(energy, a, b, c)

    norm = pre_edge_norm / polynomial_values

    norm_exafs = norm.reset_index(drop=True)

    serie_norm = norm_exafs.squeeze()

    norm_df["norm"] = serie_norm

    return norm_df


def read_file(file, **kwargs):
    """
    Read and normalize data from a XDI file.

    Parameters:
    file (str): Path to the XDI file to be read.
    **kwargs: Additional keyword arguments to be passed to the normalize function.

    Raises:
    TypeError: If the file is not a .xdi file.

    Returns:
    tuple: A tuple containing the header as a dictionary and the normalized DataFrame.
    """
    if not (file.endswith(".xdi")):
        raise TypeError("File must be .xdi")

    with open(file, "r") as fl:
        header = {}
        values = []
        reading_header = True
        n_columns = 0

        for line in fl:
            line = line.strip()

            if reading_header:
                if line.startswith("#"):
                    partes = line[1:].split(":", 1)
                    if len(partes) == 2:
                        chave = partes[0].strip()
                        valor = partes[1].strip()
                        if "Column." in line:
                            n_columns += 1
                        if "Note" not in line:
                            header[chave] = valor
                else:
                    reading_header = False
                    continue

            if not reading_header and line:
                values.append(line.split())

    colunas = []
    for i in range(n_columns):
        colunas.append(header[f"Column.{i+1}"])

    try:
        df = pd.DataFrame(values, columns=colunas)
    except:
        raise ValueError('Dataframe must have ["energy eV", "norm"] as columns')

    for i in df:
        for u in range(len(df[i])):
            df[i][u] = float(df[i][u])

    filename = str(file).split("/")[-1]
    element = header['Element.symbol']

    df_norm = normalize(df, **kwargs)

    pickle_path = f"./norm_pkl_files/{element}/"
    try:
        os.makedirs(pickle_path, exist_ok=True)
    except Exception as e:
        print(f"Erro ao criar diretório: {e}")


    with open(pickle_path + filename[:-4] + "_norm.pickle", "wb") as handle:
        pickle.dump((header, df_norm), handle, protocol=pickle.HIGHEST_PROTOCOL)

    return (header, df_norm)