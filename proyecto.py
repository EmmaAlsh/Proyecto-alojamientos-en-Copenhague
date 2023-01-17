# Proyecto de Python (AirBNB en Python + Streamlit) de Programación II.
# Docentes: Prof. Lic. Natalia Colussi y Prof. Damián Marotte.
# Alumnos:
# Guido Julián Montana
# Juliana Altobello

import requests
import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd
import numpy as np
import pydeck as pdk
import csv
import plotly.graph_objs as go

# cargamos los datos:
# Creamos una lista vacía
lista_ubicaciones = []
# Abrimos el csv que vamos a usar y creamos una lista de listas con los datos.
with open("copenhague.csv", encoding="utf8") as datos:
    reader = csv.reader(datos)
    for fila in reader:
        lista_ubicaciones.append(fila)

# Eliminamos la primera fila de lista_ubicaciones
lista_ubicaciones = lista_ubicaciones[1:]


def extraer_latitudes_longitudes(lista):
    """
    Representamos un conjunto de datos de ubicaciones 
    como una lista
    extraer_latitudes_longitudes: List-> Dataframe
    Recibe una lista de ubicaciones y nos devuelve un dataframe 
    de latitudes y longitudes.
    Ejemplos:
    extraer_latitudes_longitudes([
    ['Nrrebro', '55.68641', '12.54741', 
    'Entire home/apt', '717', '2'], 
    ['Indre By', '55.6930710700191', '12.576494184665',
     'Entire home/apt', '2400', '1'], 
    ['Vesterbro-Kongens Enghave', '55.66539', '12.55639',
     'Entire home/apt', '750', '3']]) = pd.DataFrame(np.array
                                        ([55.68641, 12.54741,
                                         55.6930710700191,12.576494184665,
                                         55.66539,12.55639 ]),
                                         columns=['lat', 'lon'])
    extraer_latitudes_longitudes([])=[]
    """
    lista_filtrada = []
    if not (lista):
        return lista_filtrada
    for casa in lista:
        latitud = float(casa[1])
        longitud = float(casa[2])
        lista_coordenada = [latitud, longitud]
        lista_filtrada.append(lista_coordenada)
    return pd.DataFrame(np.array(lista_filtrada),
                        columns=['lat', 'lon'])


def filtrar_por_tipo(lista, tipo):
    """
    Representamos el tipo con string
    tipo : String
    filtrar_por_tipo(): List String -> List
    Recibe una lista de ubicaciones y un tipo hospedaje y nos devuelve 
    la lista de casas filtrada según el tipo de hospedaje.
    Otra opcion: recibe una lista y un barrio y filtra la lista segun el barrio.

    Ejemplos:
    filtrar_por_tipo([], 'Hotel Room') = []

    filtrar_por_tipo([['Amager st', '55.63938', '12.6207', 'Entire home/apt', '2500', '1'],
                        ['Bispebjerg', '55.7266', '12.55303', 'Entire home/apt', '1100', '1'], 
                        ['Vanlse', '55.6901740723575', '12.4621413338818', 'Hotel Room', '640', '2'], 
                        ['Valby', '55.64237', '12.49735', 'Private Room', '1100', '5']], 'Entire home/apt') =
                    [['Amager st', '55.63938', '12.6207', 'Entire home/apt', '2500', '1'],
                    ['Bispebjerg', '55.7266', '12.55303', 'Entire home/apt', '1100', '1']]

    filtrar_por_tipo([['Nrrebro', '55.68641', '12.54741', 'Entire home/apt', '717', '2'],
     ['Indre By', '55.6930710700191', '12.576494184665', 'Private Room', '2400', '1'],
     ['Vesterbro-Kongens Enghave', '55.66539', '12.55639', 'Entire home/apt', '750', '3']],"Private Room")=
     ['Indre By', '55.6930710700191', '12.576494184665', 'Private Room', '2400', '1']

    filtrar_por_tipo([['Nrrebro', '55.68641', '12.54741', 'Entire home/apt', '717', '2'],
     ['Indre By', '55.6930710700191', '12.576494184665', 'Private Room', '2400', '1'],
     ['Vesterbro-Kongens Enghave', '55.66539', '12.55639', 'Entire home/apt', '750', '3']], "Nrrebo")=
     [['Nrrebro', '55.68641', '12.54741', 'Entire home/apt', '717', '2']]

     filtrar_por_tipo([['Nrrebro', '55.68641', '12.54741', 'Entire home/apt', '717', '2'],
     ['Indre By', '55.6930710700191', '12.576494184665', 'Private Room', '2400', '1'],
     ['Vesterbro-Kongens Enghave', '55.66539', '12.55639', 'Entire home/apt', '750', '3']], "Indre By")=
     [['Indre By', '55.6930710700191', '12.576494184665', 'Private Room', '2400', '1']]
    """
    lista_respuesta = []
    for sublista in lista:
        if sublista[3] == tipo or sublista[0] == tipo:
            lista_respuesta.append(sublista)
    return lista_respuesta

def test_filtrar_por_tipo():
    '''
    Función de testing de filtrar_por_tipo
    '''
    assert filtrar_por_tipo([], 'Hotel Room') == []
    assert filtrar_por_tipo([['Amager st', '55.63938', '12.6207', 'Entire home/apt', '2500', '1'],
                             ['Bispebjerg', '55.7266', '12.55303',
                                 'Entire home/apt', '1100', '1'],
                             ['Vanlse', '55.6901740723575',
                                 '12.4621413338818', 'Hotel Room', '640', '2'],
                             ['Valby', '55.64237', '12.49735', 'Private Room', '1100', '5']],
                            'Entire home/apt') == [['Amager st', '55.63938', '12.6207', 'Entire home/apt', '2500', '1'],
                                                   ['Bispebjerg', '55.7266', '12.55303', 'Entire home/apt', '1100', '1']]
    assert filtrar_por_tipo([['Nrrebro', '55.68641', '12.54741', 'Entire home/apt', '717', '2'],
                             ['Indre By', '55.6930710700191',
                                 '12.576494184665', 'Private Room', '2400', '1'],
                             ['Vesterbro-Kongens Enghave', '55.66539', '12.55639', 'Entire home/apt', '750', '3']],
                            "Private Room") == [['Indre By', '55.6930710700191', '12.576494184665', 'Private Room', '2400', '1']]
    assert filtrar_por_tipo([['Nrrebro', '55.68641', '12.54741', 'Entire home/apt', '717', '2'],
                               ['Indre By', '55.6930710700191',
                                   '12.576494184665', 'Private Room', '2400', '1'],
                               ['Vesterbro-Kongens Enghave', '55.66539', '12.55639', 'Entire home/apt', '750', '3']], "Nrrebro") == [
        ['Nrrebro', '55.68641', '12.54741', 'Entire home/apt', '717', '2']]
    assert filtrar_por_tipo([['Nrrebro', '55.68641', '12.54741', 'Entire home/apt', '717', '2'],
                               ['Indre By', '55.6930710700191',
                                   '12.576494184665', 'Private Room', '2400', '1'],
                               ['Vesterbro-Kongens Enghave', '55.66539', '12.55639', 'Entire home/apt', '750', '3']], "Indre By") == [
        ['Indre By', '55.6930710700191', '12.576494184665', 'Private Room', '2400', '1']]


# guardamos en variables el tipo de ubicaciones para ahorar tiempo
# de cálculo
lista_casas_departamentos = filtrar_por_tipo(
    lista_ubicaciones, "Entire home/apt")
lista_habitaciones_privadas = filtrar_por_tipo(
    lista_ubicaciones, "Private room")
lista_hoteles = filtrar_por_tipo(lista_ubicaciones, "Hotel room")


def filtrar_por_estrellas(lista, estrellas):
    """
    Representamos las estrellas con numeros enteros entre 1 y 5
    estrellas: Number
    Recibe una lista y un numero de estrellas, las filtra 
    segun estrellas
    filtrar_por_estrellas(): List Estrellas-> List
    Ejemplos:
    filtrar_por_estrellas([['Nrrebro', '55.68641', '12.54741', 'Entire home/apt', '717', '2'],
     ['Indre By', '55.6930710700191', '12.576494184665', 'Private Room', '2400', '1'],
     ['Vesterbro-Kongens Enghave', '55.66539', '12.55639', 'Entire home/apt', '750', '3']],3)=
     [['Vesterbro-Kongens Enghave', '55.66539', '12.55639', 'Entire home/apt', '750', '3']]
    filtrar_por_estrellas([['Nrrebro', '55.68641', '12.54741', 'Entire home/apt', '717', '2'],
     ['Indre By', '55.6930710700191', '12.576494184665', 'Private Room', '2400', '1'],
     ['Vesterbro-Kongens Enghave', '55.66539', '12.55639', 'Entire home/apt', '750', '3']],1)=
     [['Indre By', '55.6930710700191', '12.576494184665', 'Private Room', '2400', '1']]
    filtrar_por_estrellas([[],[]],3)=[]
    """
    lista_respuesta = []
    for casa in lista:
        if int(casa[5]) == estrellas:
            lista_respuesta.append(casa)

    return lista_respuesta


def test_filtrar_por_estrellas():
    '''
    Función de testing de filtrar_por_estrellas
    '''
    assert filtrar_por_estrellas([['Nrrebro', '55.68641', '12.54741', 'Entire home/apt', '717', '2'],
                                  ['Indre By', '55.6930710700191',
                                      '12.576494184665', 'Private Room', '2400', '1'],
                                  ['Vesterbro-Kongens Enghave', '55.66539', '12.55639', 'Entire home/apt', '750', '3']], 3) == [
        ['Vesterbro-Kongens Enghave', '55.66539', '12.55639', 'Entire home/apt', '750', '3']]
    assert filtrar_por_estrellas([['Nrrebro', '55.68641', '12.54741', 'Entire home/apt', '717', '2'],
                                  ['Indre By', '55.6930710700191',
                                      '12.576494184665', 'Private Room', '2400', '1'],
                                  ['Vesterbro-Kongens Enghave', '55.66539', '12.55639', 'Entire home/apt', '750', '3']], 1) == [
        ['Indre By', '55.6930710700191', '12.576494184665', 'Private Room', '2400', '1']]
    assert filtrar_por_estrellas([], 3) == []



# Creamos el título de la página que aparece en la ventana:
# el wide hace que se vea todo a la izquierda, no en el centro.
st.set_page_config(page_title="Copenhague",
                   page_icon=":two_hearts:", layout="wide")

# Informacion del sidebar contenida en st.container()
with st.container():
    st.sidebar.title("Copenhague")
    st.sidebar.write("---")
    st.sidebar.header("Tipo de Hospedaje")
    st.sidebar.write(
        """
        Los departamentos y casas están marcados con puntos rojos, los hoteles con puntos verdes
            y las habitaciones con circulos azules.
        """
    )
    opciones = ("Copenhague", "Amager st", "Amager Vest", "Bispebjerg",
                "Brnshj-Husum", "Frederiksberg", "Indre By",
                "Nrrebro", "sterbro", "Valby",
                "Vanlse", "Vesterbro-Kongens Enghave")
    select_box = st.sidebar.selectbox("Elige un barrio:", opciones)

    st.sidebar.write(
        """
        Elige el hospedaje que desees:
        """
    )
    checkbox_casas_depas = st.sidebar.checkbox(
        "Casas y Departamentos", value=True)
    checkbox_hoteles = st.sidebar.checkbox("Hoteles", value=True)
    checkbox_privadas = st.sidebar.checkbox("Habitaciones", value=True)
    st.sidebar.write(
        "Use el deslizador para filtrar su busqueda según reviews")
    estrellas = st.sidebar.slider(
        "⭐⠀⠀⠀⠀⠀⠀⭐⠀⠀⠀⠀⠀⭐⠀⠀⠀⠀⠀⠀⭐⠀⠀⠀⠀⠀⭐", 1, 5)
    st.sidebar.write("---")


def load_lottieurl(url):
    '''
    Verifica si la animación se puede usar.
    En el caso de que no se pueda no devuelve nada.
    load_lottieurl: url -> json | none
    '''
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Hacemos una variable con la animación usando la funcion definida anteriormente.
lottie_coding = load_lottieurl(
    "https://assets6.lottiefiles.com/packages/lf20_svy4ivvy.json")

# Creamos un container que contiene dos columnas con el titulo de la ciudad y la animacion
with st.container():
    columna_derecha, columna_izquierda = st.columns(2)
    with columna_derecha:
        st.title("Copenhague")
        st.write("---")
        st.write("Elige en que hospedaje te vas a alojar en tus próximas vacaciones! Contamos con: " +
                 str(len(lista_ubicaciones)) + " ubicaciones!")
        # divide la pantalla con una linea
    with columna_izquierda:
        st_lottie(lottie_coding, height=200, key="map")


def operar_checkbox(capa1, capa2, capa3, casas_check, hoteles_check, privadas_check):
    '''
    Depende el checkbox que esté activado devuelve
    un diccionario compuesto de diferentes campos, entre 
    ellos se encuentran capa1, capa2 y capa3 que representan
    la lista de ubicaciones que se van a mostrar en cada capa
    operar_checkbox(): List List List Boolean Boolean Boolean -> Dict
    Ej: 
    operar_checkbox(lista_casas_departamentos, lista_hoteles, 
                    lista_habitaciones_privadas, True , True, True)=
                    {"capa1":lista_casas_departamentos,
                    "capa2":lista_hoteles, 
                    "capa3": lista_habitaciones_privadas }

    operar_checkbox(lista_casas_departamentos[:4], lista_hoteles[:4], 
                    lista_habitaciones_privadas[:4], True ,False, True)=
                    {"capa1":lista_casas_departamentos[:4],
                     "capa2":[]
                    "capa3": lista_habitaciones_privadas[:4] }

    operar_checkbox(lista_casas_departamentos[:7], lista_hoteles[:4], 
                    lista_habitaciones_privadas[:9], False ,False, False)=
                    {"capa1":[],
                     "capa2":[],
                    "capa3":[] }
    '''
    dict_respuesta = {}
    lista_capa1 = []
    lista_capa2 = []
    lista_capa3 = []
    if casas_check:
        for casa in capa1:
            lista_capa1.append(casa)
    dict_respuesta["capa1"] = lista_capa1

    if hoteles_check:
        for hotel in capa2:
            lista_capa2.append(hotel)
    dict_respuesta["capa2"] = lista_capa2

    if privadas_check:
        for privada in capa3:
            lista_capa3.append(privada)
    dict_respuesta["capa3"] = lista_capa3

    return dict_respuesta


def test_operar_checkbox():
    '''
    Función testing de operar_checkbox
    '''
    assert operar_checkbox(lista_casas_departamentos, lista_hoteles,
                           lista_habitaciones_privadas, True, True, True) == {
        "capa1": lista_casas_departamentos,
        "capa2": lista_hoteles,
        "capa3": lista_habitaciones_privadas}
    assert operar_checkbox(lista_casas_departamentos[:4], lista_hoteles[:4],
                           lista_habitaciones_privadas[:4], True, False, True) == {
        "capa1": lista_casas_departamentos[:4],
        "capa2": [],
        "capa3": lista_habitaciones_privadas[:4]}
    assert operar_checkbox(lista_casas_departamentos[:7], lista_hoteles[:4],
                           lista_habitaciones_privadas[:9], False, False, False) == {
        "capa1": [],
        "capa2": [],
        "capa3": []}


def operar_estrellas(dict_mapa):
    '''
    Recibe un diccionario que contiene las 3 listas que 
    correponden a cada capa, filtra cada una según las estrellas
    elegidas en el slider y devuelve un diccionario de la misma
    forma
    operar_estrellas(): Dict-> Dict
    Ej: No podemos ver que sucede filtrando con valores distintos de 1, se evalúa 
    en función de lo que vale la variable estrellas(por defecto vale 1)
    operar_estrellas({"capa1":lista_casas_departamentos[:7],
                          "capa2":lista_hoteles[:5],
                          "capa3":lista_habitaciones_privadas[:22]})=
                          {"capa1":filtrar_por_estrellas(lista_casas_departamentos[:7],1),
                          "capa2":filtrar_por_estrellas(lista_hoteles[:5],1),
                          "capa3":filtrar_por_estrellas(lista_habitaciones_privadas[:22],1)}
    operar_estrellas({"capa1":[],
                          "capa2":[],
                          "capa3":[]})=
                          {"capa1":[],
                          "capa2":[],
                          "capa3":[]}
    '''
    dict_respuesta = {}
    lista_capa1 = dict_mapa["capa1"]
    lista_capa2 = dict_mapa["capa2"]
    lista_capa3 = dict_mapa["capa3"]

    lista_capa1 = filtrar_por_estrellas(
        lista_capa1, estrellas)
    dict_respuesta["capa1"] = lista_capa1
    lista_capa2 = filtrar_por_estrellas(
        lista_capa2, estrellas)
    dict_respuesta["capa2"] = lista_capa2
    lista_capa3 = filtrar_por_estrellas(
        lista_capa3, estrellas)
    dict_respuesta["capa3"] = lista_capa3

    return dict_respuesta


def test_operar_estrellas():
    '''
    Función de testing de operar_estrellas
    '''
    assert operar_estrellas({"capa1": lista_casas_departamentos[:7],
                             "capa2": lista_hoteles[:5],
                             "capa3": lista_habitaciones_privadas[:22]}) == {
        "capa1": filtrar_por_estrellas(lista_casas_departamentos[:7], 1),
        "capa2": filtrar_por_estrellas(lista_hoteles[:5], 1),
        "capa3": filtrar_por_estrellas(lista_habitaciones_privadas[:22], 1)}
    assert operar_estrellas({"capa1": [],
                             "capa2": [],
                             "capa3": []}) == {
        "capa1": [],
        "capa2": [],
        "capa3": []}


def operar_selectbox(dict_mapa):
    '''
    Recibe un diccionario que contiene las 3 listas que 
    correponden a cada capa, filtra cada una según el barrio
    elegido en el slider y devuelve un diccionario de la misma
    forma, agregandole campos que corresponden a las coordenadas
    del barrio, el zoom del mapa a usar y el tamaño de los puntos
    operar_selectbox(): Dict-> Dict
    Solo podemos ver que pasa en el caso de que el selectbox valga "Copenhague"
    esto se debe a que el valor por defecto del selectbox es "Copenhague"
    Ej: operar_selectbox({"capa1":lista_casas_departamentos[:7],
                          "capa2":lista_hoteles[:5],
                          "capa3":lista_habitaciones_privadas[:22]})=
                          {"capa1":lista_casas_departamentos[:7],,
                          "capa2":lista_hoteles[:5],
                          "capa3":lista_habitaciones_privadas[:22],
                          "coordenadas":(55.67594, 12.56553),
                          "zoom":11,
                          "t_puntos":50}

        operar_selectbox({"capa1":[],
                          "capa2":[],
                          "capa3":[]})={"capa1":[],,
                          "capa2":[]],
                          "capa3":[],}
                          "coordenadas":(55.67594, 12.56553),
                          "zoom":11,
                          "t_puntos":50}

    '''
    dict_respuesta = {}
    lista_capa1 = dict_mapa["capa1"]
    lista_capa2 = dict_mapa["capa2"]
    lista_capa3 = dict_mapa["capa3"]
    dict_respuesta["coordenadas"] = (55.67594, 12.56553)
    dict_respuesta["zoom"] = 11
    dict_respuesta["t_puntos"] = 50

    if (select_box != "Copenhague"):
        lista_capa1 = filtrar_por_tipo(
            lista_capa1, select_box)
        lista_capa2 = filtrar_por_tipo(
            lista_capa2, select_box)
        lista_capa3 = filtrar_por_tipo(
            lista_capa3, select_box)
        if (select_box == "Amager st"):
            dict_respuesta["coordenadas"] = (55.654444, 12.621972)
            dict_respuesta["zoom"] = 12.5
            dict_respuesta["t_puntos"] = 30
        elif(select_box == "Amager Vest"):
            dict_respuesta["coordenadas"] = (55.641024, 12.583738)
            dict_respuesta["zoom"] = 11.8
            dict_respuesta["t_puntos"] = 30
        elif(select_box == "Bispebjerg"):
            dict_respuesta["coordenadas"] = (
                55.71275643259844, 12.535044271848989)
            dict_respuesta["zoom"] = 12.3
            dict_respuesta["t_puntos"] = 30
        elif(select_box == "Brnshj-Husum"):
            dict_respuesta["coordenadas"] = (55.709764, 12.479715)
            dict_respuesta["zoom"] = 12.5
            dict_respuesta["t_puntos"] = 30
        elif(select_box == "Frederiksberg"):
            dict_respuesta["coordenadas"] = (55.680474, 12.524362)
            dict_respuesta["zoom"] = 12.5
            dict_respuesta["t_puntos"] = 30
        elif(select_box == "Indre By"):
            dict_respuesta["coordenadas"] = (
                55.68343893402464, 12.584499592497362)
            dict_respuesta["zoom"] = 12.6
            dict_respuesta["t_puntos"] = 30
        elif(select_box == "Nrrebro"):
            dict_respuesta["coordenadas"] = (55.696185, 12.548947)
            dict_respuesta["zoom"] = 12.8
            dict_respuesta["t_puntos"] = 30
        elif(select_box == "sterbro"):
            dict_respuesta["coordenadas"] = (55.710138, 12.577497)
            dict_respuesta["zoom"] = 12
            dict_respuesta["t_puntos"] = 30
        elif(select_box == "Valby"):
            dict_respuesta["coordenadas"] = (55.659109, 12.516385)
            dict_respuesta["zoom"] = 12.3
            dict_respuesta["t_puntos"] = 30
        elif(select_box == "Vanlse"):
            dict_respuesta["coordenadas"] = (55.688967, 12.489098)
            dict_respuesta["zoom"] = 12.8
            dict_respuesta["t_puntos"] = 30
        elif(select_box == "Vesterbro-Kongens Enghave"):
            dict_respuesta["coordenadas"] = (55.656266, 12.546744)
            dict_respuesta["zoom"] = 12.4
            dict_respuesta["t_puntos"] = 30
    dict_respuesta["capa1"] = lista_capa1
    dict_respuesta["capa2"] = lista_capa2
    dict_respuesta["capa3"] = lista_capa3

    return dict_respuesta


def test_operar_selectbox():
    '''
    Función testing de operar_selectbox
    '''
    assert operar_selectbox({"capa1": lista_casas_departamentos[:7],
                             "capa2": lista_hoteles[:5],
                             "capa3": lista_habitaciones_privadas[:22]}) == {
        "capa1": lista_casas_departamentos[:7],
        "capa2": lista_hoteles[:5],
        "capa3": lista_habitaciones_privadas[:22],
        "coordenadas": (55.67594, 12.56553),
        "zoom": 11,
        "t_puntos": 50}
    assert operar_selectbox({"capa1": [],
                             "capa2": [],
                             "capa3": []}) == {"capa1": [],
                                               "capa2": [],
                                               "capa3": [],
                                               "coordenadas": (55.67594, 12.56553),
                                               "zoom": 11,
                                               "t_puntos": 50}


def actualizar_mapa(dict_mapa):
    """
    Recibe un diccionario y se encarga de dibujar un mapa
    actualizar_mapa(): Dict -> Map
    """
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/violetstarling/cl3nsjvtq005814nv6gc9m5c5',
        initial_view_state=pdk.ViewState(
            latitude=dict_mapa["coordenadas"][0],
            longitude=dict_mapa["coordenadas"][1],
            zoom=dict_mapa["zoom"],
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=extraer_latitudes_longitudes(dict_mapa["capa1"]),
                get_position='[lon, lat]',
                pickable=True,
                # Rojo (casas y departamentos)
                get_fill_color=[193, 18, 31, 255],
                get_radius=dict_mapa["t_puntos"],
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=extraer_latitudes_longitudes(dict_mapa["capa2"]),
                get_position='[lon, lat]',
                pickable=True,
                get_fill_color=[0, 100, 0, 200],  # Verde (habitaciones)
                get_radius=dict_mapa["t_puntos"],
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=extraer_latitudes_longitudes(dict_mapa["capa3"]),
                get_position='[lon, lat]',
                pickable=True,
                get_fill_color=[2, 62, 138, 255],  # Azul (habitaciones)
                get_radius=dict_mapa["t_puntos"],
            ), ]
    ))


# componemos funciones para mostrar los puntos en el mapa
# según lo que seleccionó el usuario
actualizar_mapa(
    operar_selectbox(
        operar_estrellas(
            operar_checkbox(lista_casas_departamentos,
                            lista_hoteles,
                            lista_habitaciones_privadas,
                            checkbox_casas_depas,
                            checkbox_hoteles,
                            checkbox_privadas))))


def promedio(lista):
    '''
    promedio(): List -> Number
    Dada una lista de numeros devuelve el promedio.
    Ejemplos:
    promedio([2, 3, 3, 5, 7, 10]) = 5
    promedio([]) = 0
    promedio([]) = 0
    promedio([0, 23, 0]) = 7
    promedio([0, 0, 0]) = 0
    '''
    suma = 0
    cantidad = 0
    respuesta = 0
    for numero in lista:
        suma += int(numero)
        cantidad += 1
    if cantidad != 0:
        respuesta = suma // cantidad
    return respuesta


def test_promedio():
    '''
    Funcion testing de promedio
    '''
    assert promedio([2, 3, 3, 5, 7, 10]) == 5
    assert promedio([]) == 0
    assert promedio([]) == 0
    assert promedio([0, 23, 0]) == 7
    assert promedio([0, 0, 0]) == 0


def filtrar_por_precio(lista, barrio):
    """
    Representamos los barrios con strings
    barrio = String
    Recibe una lista de casas, y un barrio
    y devuelve una lista con los precios de cada barrio.
    filtrar_por_precio(): List String -> List
    Ejemplos:
    filtrar_por_precio([], "Bispebjerg") = []
    filtrar_por_precio([["Amager st", 55.68641, 12.23441, "Entire home/apt", 717],
                        ["Bispebjerg", 52.1234, 56.56456, "Hotel Room", 234],
                        ["Amager st", 13.2345, 76.4561, "Private Room", 456],
                        ["sterbro", 45.456, 12.456456, "Entire home/apt", 111],
                        ["Amager st", 12.7567, 23.2342, "Entire home/apt", 124]], "Amager st") = [717, 456, 124]
    """
    lista_respuesta = []
    for sublista in lista:
        if sublista[0] == barrio:
            lista_respuesta.append(sublista[4])
    return lista_respuesta


def test_filtrar_por_precio():
    '''
    Funcion testing de filtrar_por_precio
    '''
    assert filtrar_por_precio([], "Bispebjerg") == []
    assert filtrar_por_precio([["Amager st", 55.68641, 12.23441, "Entire home/apt", 717],
                               ["Bispebjerg", 52.1234, 56.56456, "Hotel Room", 234],
                               ["Amager st", 13.2345, 76.4561, "Private Room", 456],
                               ["sterbro", 45.456, 12.456456,
                                   "Entire home/apt", 111],
                               ["Amager st", 12.7567,
                               23.2342, "Entire home/apt", 124]], "Amager st") == [717, 456, 124]


def lista_precios(lista):
    '''
    lista_precios(): List -> Diccionary
    Dada una lista, devuelve un diccionario de los promedios de alquiler
    de cada barrio.
    Ejemplos:
    lista_precios([]) = {'Amager st': 0, 'Amager Vest': 0, 
                         'Bispebjerg': 0, 'Brnshj-Husum': 0, 
                         'Frederiksberg': 0, 'Indre By': 0, 
                         'Nrrebro': 0, 'sterbro': 0, 'Valby': 0, 
                         'Vanlse': 0, 'Vesterbro-Kongens Enghave': 0}
    lista_precios(lista_casas_departamentos) = {'Amager st': 1007, 
                                                'Amager Vest': 1179, 
                                                'Bispebjerg': 917, 
                                                'Brnshj-Husum': 1009, 
                                                'Frederiksberg': 1249, 
                                                'Indre By': 1651, 
                                                'Nrrebro': 980, 
                                                'sterbro': 1137, 
                                                'Valby': 1029, 
                                                'Vanlse': 890, 
                                                'Vesterbro-Kongens Enghave': 1106}
    lista_precios([["Amager st", 55.68641, 12.23441, "Entire home/apt", 717],
                  ["Bispebjerg", 52.1234, 56.56456, "Hotel Room", 234]]) =
                  {'Amager st': 717,
                   'Amager Vest': 0, 
                   'Bispebjerg': 234, 
                   'Brnshj-Husum': 0, 
                   'Frederiksberg': 0, 
                   'Indre By': 0, 
                   'Nrrebro': 0, 
                   'sterbro': 0, 
                   'Valby': 0, 
                   'Vanlse': 0, 
                   'Vesterbro-Kongens Enghave': 0}
    '''
    amager_st_promedio = promedio(filtrar_por_precio(lista, "Amager st"))
    amager_vest_promedio = promedio(filtrar_por_precio(lista, "Amager Vest"))
    bispebjerg_promedio = promedio(filtrar_por_precio(lista, "Bispebjerg"))
    brnshj_husum_promedio = promedio(filtrar_por_precio(lista, "Brnshj-Husum"))
    frederiksberg_promedio = promedio(
        filtrar_por_precio(lista, "Frederiksberg"))
    indre_by_promedio = promedio(filtrar_por_precio(lista, "Indre By"))
    nrrebro_promedio = promedio(filtrar_por_precio(lista, "Nrrebro"))
    sterbro_promedio = promedio(filtrar_por_precio(lista, "sterbro"))
    valby_promedio = promedio(filtrar_por_precio(lista, "Valby"))
    vanlse_promedio = promedio(filtrar_por_precio(lista, "Vanlse"))
    vesterbro_kongens_enghave_promedio = promedio(
        filtrar_por_precio(
            lista, "Vesterbro-Kongens Enghave"))
    diccionario_promedios = {"Amager st": amager_st_promedio,
                             "Amager Vest": amager_vest_promedio,
                             "Bispebjerg": bispebjerg_promedio,
                             "Brnshj-Husum": brnshj_husum_promedio,
                             "Frederiksberg": frederiksberg_promedio,
                             "Indre By": indre_by_promedio,
                             "Nrrebro": nrrebro_promedio,
                             "sterbro": sterbro_promedio,
                             "Valby": valby_promedio,
                             "Vanlse": vanlse_promedio,
                             "Vesterbro-Kongens Enghave": vesterbro_kongens_enghave_promedio}
    return diccionario_promedios


def test_lista_precios():
    '''
    Testing de la funcion test_lista_precios
    '''
    assert lista_precios(lista_casas_departamentos) == {'Amager st': 1007,
                                                        'Amager Vest': 1179,
                                                        'Bispebjerg': 917,
                                                        'Brnshj-Husum': 1009,
                                                        'Frederiksberg': 1249,
                                                        'Indre By': 1651,
                                                        'Nrrebro': 980,
                                                        'sterbro': 1137,
                                                        'Valby': 1029,
                                                        'Vanlse': 890,
                                                        'Vesterbro-Kongens Enghave': 1106}
    assert lista_precios([]) == {'Amager st': 0, 'Amager Vest': 0,
                                 'Bispebjerg': 0, 'Brnshj-Husum': 0,
                                 'Frederiksberg': 0, 'Indre By': 0,
                                 'Nrrebro': 0, 'sterbro': 0, 'Valby': 0,
                                 'Vanlse': 0, 'Vesterbro-Kongens Enghave': 0}
    assert lista_precios([["Amager st", 55.68641, 12.23441, "Entire home/apt", 717],
                         ["Bispebjerg", 52.1234, 56.56456, "Hotel Room", 234]]) == {'Amager st': 717,
                                                                                    'Amager Vest': 0,
                                                                                    'Bispebjerg': 234,
                                                                                    'Brnshj-Husum': 0,
                                                                                    'Frederiksberg': 0,
                                                                                    'Indre By': 0,
                                                                                    'Nrrebro': 0,
                                                                                    'sterbro': 0,
                                                                                    'Valby': 0,
                                                                                    'Vanlse': 0,
                                                                                    'Vesterbro-Kongens Enghave': 0}


def getList(dic):
    '''
    getList(): Dictionary -> List
    Dado un diccionario devuelve una lista con las key 
    del diccionario.
    Ejemplos:
    getList({}) = []
    getList({"Amager st": 142,
             "Amager Vest": 34,
             "Bispebjerg": 124}) == ["Amager st", "Amager Vest", "Bispebjerg"]
    '''
    lista = []
    for key in dic.keys():
        lista.append(key)
    return lista


def test_getList():
    '''
    Funcion de testeo de getList
    '''
    assert getList({}) == []
    assert getList({"Amager st": 142,
                    "Amager Vest": 34,
                    "Bispebjerg": 124}) == ["Amager st", "Amager Vest", "Bispebjerg"]


def getListValue(dic):
    '''
    getListValue(): Dictionary -> List
    Dado un diccionario devuelve una lista con los valores 
    del diccionario.
    Ejemplos:
    getListValue({}) = []
    getListValue({"Amager st": 142,
             "Amager Vest": 34,
             "Bispebjerg": 124}) == [142, 34, 124]
    '''
    lista = []
    for value in dic.values():
        lista.append(value)
    return lista


def test_getListValue():
    '''
    Funcion de testeo de getListValue
    '''
    assert getListValue({}) == []
    assert getListValue({"Amager st": 142,
                         "Amager Vest": 34,
                         "Bispebjerg": 124}) == [142, 34, 124]


def hacer_grafico(lista, color):
    """
    Recibe una lista de ubicaciones y un color, 
    nos devuelve un grafico de barras del precio de cada barrio
    con el color que especificamos
    """
    data = [go.Bar(
        x=getList(lista_precios(lista)),
        y=getListValue(lista_precios(lista)),
        marker_color=color
    )]
    fig = go.Figure(data=data)

    # ajustes de diseño
    fig.update_layout(
        width=350,
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(
            l=10,
            r=50,
            b=100,
            t=0,
            pad=0
        )
    )
    return fig


st.header(
    "A continuación verá el grafico de costos segun tipo de habitación y barrio:")
col1, col2, col3 = st.columns(3)
with col1:
    st.header("Casas:")
    st.plotly_chart(hacer_grafico(lista_casas_departamentos,
                    "rgba(193, 18, 31, 255)"), use_container_width=False)
with col2:
    st.header("Hoteles:")
    st.plotly_chart(hacer_grafico(
        lista_hoteles, "rgba(0,120,0,255)"), use_container_width=False)
with col3:
    st.header("Habitaciones Privadas:")
    st.plotly_chart(hacer_grafico(lista_habitaciones_privadas,
                    "rgba(2, 62, 138, 255)"), use_container_width=False)
