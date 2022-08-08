#!/usr/bin/env python
# coding: utf-8

# # Yandex.Music

# # Contents <a id='back'></a>
# 
# * [Introducción](#intro)
# * [Etapa 1. Descripción de los datos](#data_review)
#     * [Conclusions](#data_review_conclusions)
# * [Etapa 2. Data preprocessing](#data_preprocessing)
#     * [2.1 Estilo del encabezado](#header_style)
#     * [2.2 Valores ausentes](#missing_values)
#     * [2.3 Duplicados](#duplicates)
#     * [2.4 Conclusiones](#data_preprocessing_conclusions)
# * [Etapa 3. Prueba de hipótesis](#hypotheses)
#     * [3.1 Hipótesis 1: comparar el comportamiento del usuario en las dos ciudades](#activity)
#     * [3.2 Hipótesis 2: música al principio y al final de la semana](#week)
#     * [3.3 Hipótesis 3: preferencias de género en Springfield y Shelbyville](#genre)
# * [Conclusiones](#end)

# ## Introducción <a id='intro'></a>
# Siempre que investiguemos, necesitamos formular hipótesis que después podamos probar. A veces aceptamos estas hipótesis; otras, las rechazamos. Para tomar las decisiones correctas, una empresa debe ser capaz de entender si está haciendo las suposiciones correctas.
# 
# En este proyecto, compararás las preferencias musicales de las ciudades de Springfield y Shelbyville. Estudiarás datos reales de Yandex.Music para probar las hipótesis de abajo y comparar el comportamiento del usuario de esas dos ciudades.
# 
# ### Objetivo: 
# Prueba tres hipótesis: 
# 1. La actividad de los usuarios difiere según el día de la semana y dependiendo de la ciudad. 
# 2. Los lunes por la mañana, los habitantes de Springfield y Shelbyville escuchan diferentes géneros. Lo mismo ocurre con los viernes por la noche. 
# 3. Los oyentes de Springfield y Shelbyville tienen preferencias distintas. En Springfield prefieren el pop mientras que en Shelbyville hay más aficionados al rap.
# 
# ### Etapas 
# Los datos del comportamiento del usuario se almacenan en el archivo `/datasets/music_project_en.csv`. No hay ninguna información sobre la calidad de los datos así que necesitarás examinarlos antes de probar las hipótesis. 
# 
# Primero, evaluarás la calidad de los datos y verás si los problemas son significativos. Entonces, durante el preprocesamiento de datos, tomarás en cuenta los problemas más críticos.
#  
# Tu proyecto consistirá en tres etapas:
#  1. Descripción de los datos
#  2. Preprocesamiento de datos
#  3. Prueba de hipótesis
#  
# [Volver a Contenidos](#back)

# ## Etapa 1. Descripción de los datos <a id='data_review'></a>
# 
# Abre los datos en Yandex.Music y examínalos.

# Necesitarás `pandas` así que impórtalo.

# In[89]:


import pandas as pd # importando pandas


# Lee el archivo `music_project_en.csv` de la carpeta `/datasets/` y guárdalo en la variable `df`:

# In[90]:


df = pd.read_csv ('/datasets/music_project_en.csv') # leyendo el archivo y almacenándolo en df
df.describe()


# Imprime las 10 primeras filas de la tabla:

# In[91]:


(df.head(10))# obteniendo las 10 primeras filas de la tabla df


# Obtener la información general sobre la tabla con un comando:

# In[92]:


df.info()# obteniendo información general sobre los datos en df


# La tabla contiene siete columnas. Todas almacenan el mismo tipo de datos: objeto.
# 
# De acuerdo con la documentación:
# - `'userID'` — identificador del usuario
# - `'Track'` — título de la pista
# - `'artist'` — nombre del artista
# - `'genre'` — género
# - `'City'` — ciudad del usuario
# - `'time'` — el periodo de tiempo exacto en que se reprodujo la pista
# - `'Day'` — día de la semana
# 
# Podemos ver tres problemas con el estilo en los nombres de las columnas:
# 1. Algunos nombres están en mayúsculas, otros en minúsculas.
# 2. Hay algunos espacios en algunos nombres.
# 3. Claridad, cambiar 'time' por 'total_time' y 'day' por 'day_reproduced' `Detecta el tercer problema tú mismo y descríbelo aquí`.
# 
# El número de valores de las columnas es diferente. Esto significa que los datos contienen valores ausentes.
# 

# ### Conclusiones <a id='data_review_conclusions'></a> 
# 
# Cada fila de la tabla almacena datos de la pista que fue reproducida. Algunas columnas describen la pista en sí: su título, el artista y el género. El resto transmite la información del usuario: la ciudad de la que viene, el tiempo que ha reproducido la pista. 
# 
# Está claro que los datos son suficientes para probar la hipótesis. Sin embargo, hay valores ausentes.
# 
# Para continuar, necesitamos preprocesar los datos.

# [Volver a Contenidos](#back)

# ## Etapa 2. Preprocesamiento de datos <a id='data_preprocessing'></a>
# Corrige el formato en los encabezados de las columnas y ocúpate de los valores ausentes. Después, comprueba si hay duplicados en los datos.

# ### Estilo del encabezado <a id='header_style'></a>
# Imprime el encabezado de la columna:

# In[93]:


(df.columns)# la lista de los nombres de las columnas en la tabla df


# Cambia los nombres de las columnas de acuerdo con las reglas del buen estilo:
# * Si el nombre tiene varias palabras, utiliza snake_case
# * Todos los caracteres deben ser minúsculas
# * Elimina los espacios

# In[94]:


df = df.rename(
    columns={
        '  userID': 'user_id',
        'Track': 'track',
        '  City  ': 'city',
        'time': 'total_time',
        'Day': 'day_reproduced'
    }
)
df.columns# renombra las columnas


# Comprueba el resultado. Imprime los nombres de las columnas una vez más:

# In[95]:


df.columns# comprobando el resultado: la lista de los nombres de las columnas


# [Volver a Contenidos](#back)

# ### Valores ausentes <a id='missing_values'></a>
# Primero encuentra el número de valores ausentes en la tabla. Para ello, utiliza dos métodos pandas:

# In[96]:


(df.isna().sum()) 


(df.isnull().sum()) # calculando valores ausentes


# No todos los valores ausentes afectan a la investigación. Por ejemplo, los valores ausentes en la pista y artista no son cruciales. Simplemente puedes reemplazarlos por marcadores claros.
# 
# Pero los valores ausentes en `'genre'` pueden afectar la comparación entre las preferencias musicales de Springfield y Shelbyville. En la vida real, sería útil saber las razones por las cuales hay datos ausentes e intentar recuperarlos. Pero no tenemos esa oportunidad en este proyecto. Así que tendrás que:
# * Rellenar esos valores ausentes con marcadores
# * Evaluar cuánto podrían afectar los valores ausentes a tus cómputos.

# Reemplazar los valores ausentes en `'track'`, `'artist'`, y `'genre'` con la string `'unknown'`. Para ello, crea la lista `columns_to_replace`, recórrela con un bucle `for` y reemplaza los valores ausentes en cada una de las columnas:

# In[97]:


columns_to_replace = ['track','artist','genre']

for row in columns_to_replace:
    df[columns_to_replace] = df[columns_to_replace].fillna('unknown')
    
df
   
    
    
    
    
    #df['columns_to_replace'] = df['columns_to_replace'].fillna('unknown')
          

# recorriendo los nombres de las columnas y reemplazando los valores ausentes con 'unknown'


# Asegúrate de que la tabla no contiene más valores ausentes. Cuenta de nuevo los valores ausentes.

# [Volver a Contenidos](#back)

# ### Duplicados <a id='duplicates'></a>
# Encuentra el número de duplicados obvios en la tabla utilizando un comando:

# In[98]:


(df.isna().sum()) # contando valores ausentes


# In[99]:


(df.duplicated().sum())# contando duplicado obvios


# Llama al método `pandas` para deshacerte de los duplicados obvios:

# In[100]:


df = df.drop_duplicates().reset_index(drop=True) # eliminando duplicados obvios


# Cuenta los duplicados obvios una vez más para asegurarte de que todos han sido eliminados:

# In[101]:


(df.duplicated().sum())# comprobando duplicados


# Ahora deshazte de los duplicados implícitos en la columna genre. Por ejemplo, el nombre de un género se puede escribir de varias formas. Dichos errores también pueden afectar a resultado.

# Imprime una lista de nombres únicos de géneros, ordenados en orden alfabético. Cómo se hace:
# * Recupera la deseada columna DataFrame 
# * Aplícale un método de orden
# * Para la columna ordenada, llama al método que te devolverá todos los valores de columna únicos

# In[102]:


df.genre.unique()# inspeccionando los nombres de géneros únicos


# Busca en la lista para encontrar duplicados implícitos del género `hiphop`. Estos pueden ser nombres escritos incorrectamente o nombres alternativos para el mismo género.
# 
# Verás los siguientes duplicados implícitos:
# * `hip`
# * `hop`
# * `hip-hop`
# 
# Para deshacerte de ellos, declara la función `replace_wrong_genres()` con dos parámetros: 
# * `wrong_genres=` — la lista de duplicados
# * `correct_genre=` — la string con el valor correcto
# 
# La función debería corregir los nombres en la columna `'genre'` de la tabla `df`, es decir, remplaza cada valor de la lista `wrong_genres` con el valor en `correct_genre`.

# In[103]:


def replace_wrong_genres(wrong_genres, correct_genre):
    for wrong_genre in wrong_genres: 
        df['genre'] = df['genre'].replace(wrong_genre, correct_genre) # función para reemplazar duplicados implícitos


# Llama a `replace_wrong_genres()` y pásale argumentos para que retire los duplicados implícitos (`hip`, `hop` y `hip-hop`) y los reemplace por `hiphop`:

# In[104]:


duplicates = ['hip', 'hop', 'hip-hop'] 
genre = 'hiphop' 
replace_wrong_genres(duplicates, genre)# eliminando duplicados implícitos


# Asegúrate que los nombres duplicados han sido eliminados. Imprime la lista de valores únicos de la columna `'genre'`:

# In[105]:


df.genre# revisando en busca de duplicados implícitos


# [Volver a Contenidos](#back)

# ### Conclusiones <a id='data_preprocessing_conclusions'></a>
# Detectamos tres problemas con los datos:
# 
# - Estilos de encabezados incorrectos
# - Valores ausentes
# - Duplicados obvios e implícitos
# 
# Los encabezados han sido eliminados para conseguir que el procesamiento de la tabla sea más sencillo.
# 
# Todos los valores ausentes han sido reemplazados por `'unknown'`. Pero todavía tenemos que ver si los valores ausentes en `'genre'` afectan a nuestros cálculos.
# 
# La ausencia de duplicados hará que los resultados sean mas precisos y fáciles de entender.
# 
# Ahora ya podemos continuar probando las hipótesis. 

# [Volver a Contenidos](#back)

# ## Etapa 3. Prueba de hipótesis <a id='hypotheses'></a>

# ### Hipótesis 1: comparar el comportamiento del usuario en las dos ciudades <a id='activity'></a>

# De acuerdo con la primera hipótesis, los usuarios de Springfield y Shelbyville escuchan música de forma distinta. Comprueba esto utilizando los datos de tres días de la semana: lunes, miércoles y viernes.
# 
# * Divide a los usuarios en grupos por ciudad.
# * Compara cuántas pistas reprodujo cada grupo el lunes, el miércoles y el viernes.
# 

# Por el bien del ejercicio, realiza cada cálculo de forma separada. 
# 
# Evalúa la actividad del usuario en cada ciudad. Agrupa los datos por ciudad y encuentra el número de canciones reproducidas en cada grupo.
# 
# 

# In[106]:


df.groupby('city')
df.groupby('city').count()# contando las pistas reproducidas en cada ciudad


# Springfield ha reproducido más pistas que Shelbyville. Pero eso no implica que los ciudadanos de Springfield escuchen música más a menudo. Esta ciudad es simplemente más grande y hay más usuarios.
# 
# Ahora agrupa los datos por día de la semana y encuentra el número de pistas reproducidas el lunes, miércoles y viernes.
# 

# In[107]:


df.groupby('day_reproduced')
df.groupby('day_reproduced').count()# calculando las pistas reproducidas en cada uno de los tres días


# El miércoles fue el día más silencioso de todos. Pero si consideramos las dos ciudades por separado podríamos llegar a una conclusión diferente.

# Ya has visto cómo funciona el agrupar por ciudad o día. Ahora escribe la función que agrupará ambos.
# 
# Crea la función `number_tracks()` para calcular el número de canciones reproducidas en un determinado día y ciudad. Requerirá dos parámetros:
# * día de la semana
# * nombre de la ciudad
# 
# En la función, utiliza una variable para almacenar las filas de la tabla original, donde:
#   * el valor de la columna `'day'` es igual al parámetro de día
#   * el valor de la columna `'city'` es igual al parámetro de ciudad
# 
# Aplica un filtrado consecutivo con indexación lógica.
# 
# Después, calcula los valores de la columna `'user_id'` en la tabla resultante. Almacena el resultado en la nueva variable. Recupera esta variable de la función.

# In[108]:


def number_tracks(day, cityr):                                                             # <creando la función number_tracks()> # declararemos la función con dos parámetros: day=, city=.
    track_list = df[(df['day_reproduced'] == day) & (df['city'] == cityr)]  # deja que la variable track_list almacene las filas df en las que
    track_list_count = track_list['user_id'].count()                                                            # el valor en la columna 'day' es igual al parámetro day= y, al mismo tiempo, 
    return track_list_count 
()
                                # declararemos la función con dos parámetros: day=, city=.


# el valor de la columna 'city' es igual al parámetro city= (aplica el filtrado consecutivo 
                                                              # con indexación lógica).
                                                               # deja que la variable track_list_count almacene el número de valores de la columna 'user_id' en track_list
                                                                # (encontrado con el método count()).
     

   # permite que la función devuelva un número: el valor de track_list_count.

# la función cuenta las pistas reproducidas en un cierto día y ciudad.
# primero recupera las filas del día deseado de la tabla,
# después filtra las filas de la ciudad deseada del resultado,
# entonces, encuentra el número de valores de 'user_id' en la tabla filtrada,
# y devuelve ese número.
# para ver lo que devuelve, envuelve la llamada de la función en print().


# Llama a `number_tracks()` seis veces, cambiando los valores de los parámetros, para que recuperes los datos de ambas ciudades para cada uno de los tres días.

# In[109]:


number_tracks('Monday', 'Springfield')# el número de canciones reproducidas en Springfield el lunes


# In[110]:


number_tracks('Monday', 'Shelbyville')# el número de canciones reproducidas en Shelbyville el lunes


# In[111]:


number_tracks('Wednesday', 'Springfield')# el número de canciones reproducidas en Springfield el miércoles


# In[112]:


number_tracks('Wednesday', 'Shelbyville')# el número de canciones reproducidas en Shelbyville el miércoles


# In[113]:


number_tracks('Friday', 'Springfield')# el número de canciones reproducidas en Springfield el viernes


# In[114]:


number_tracks('Friday', 'Shelbyville')# el número de canciones reproducidas en Shelbyville el viernes


# Utiliza `pd.DataFrame` para crear una tabla, donde
# * Los nombres de las columnas son: `['city', 'monday', 'wednesday', 'friday']`
# * Los datos son los resultados que conseguiste de `number_tracks()`

# In[115]:


info = [
    ['springfield', 15740, 11056, 15945],
    ['shelbyville', 5614, 7003, 5895]
]

columnas = ['city', 'monday', 'wednesday', 'friday']

df_tabla = pd.DataFrame(data=info, columns=columnas)
    


# In[116]:


df_tabla# tabla con los resultados


# **Conclusiones**
# 
# Los datos revelan las diferencias en el comportamiento de los usuarios:
# 
# - En Springfield, el número de canciones reproducidas alcanzan el punto máximo los lunes y viernes mientras que los miércoles hay un descenso de la actividad.
# - En Shelbyville, al contario, los usuarios escuchan más música los miércoles. La actividad de los usuarios los lunes y viernes es menor.
# 
# Así que la primera hipótesis parece ser correcta.

# [Volver a Contenidos](#back)

# ### Hipótesis 2: música al principio y al final de la semana <a id='week'></a>

# De acuerdo con la segunda hipótesis, los lunes por la mañana y los viernes por la noche los ciudadanos de Springfield escuchan géneros que difieren de aquellos que los usuarios de Shelbyville disfrutan.

# Obtén tablas (asegúrate de que el nombre de tu tabla combinada encaja con el DataFrame dado en los dos bloques de código de abajo):
# * Para Springfield — `spr_general`
# * Para Shelbyville — `shel_general`

# In[117]:


spr_general = pd.DataFrame(df[df['city'] == 'Springfield'])

spr_general
#obteniendo la tabla spr_general de las filas de df, 
# donde los valores en la columna 'city' es 'Springfield'


# In[118]:


shel_general = pd.DataFrame(df[df['city'] == 'Shelbyville'])

shel_general
# obteniendo shel_general de las filas df,
# donde el valor de la columna 'city' es 'Shelbyville'


# Escribe la función genre_weekday() con cuatro parámetros:
# * Una tabla para los datos (`df`)
# * El día de la semana (`day`)
# * La marca de fecha y hora en formato 'hh:mm' (`time1`)
# * La marca de fecha y hora en formato 'hh:mm' (`time2`)
# 
# La función debería devolver información de los 15 géneros más populares de un día determinado en un período entre dos marcas de fecha y hora.

# In[134]:


def genre_weekday (df, day, time1, time2):
    # declarando la función genre_weekday() con los parámetros day=, time1= y time2=. Debería
# devolver información sobre los géneros más populares de un determinado día a una determinada hora:

# 1) Deja que la variable genre_df almacene las filas que cumplen varias condiciones:
#    - el valor de la columna 'day' es igual al valor del argumento day=
#    - el valor de la columna 'time' es mayor que el valor del argumento time1=
                                                                     #    - el valor en la columna 'time' es menor que el valor del argumento time2=
                                                          #    Utiliza un filtrado consecutivo con indexación lógica.

# 2) Agrupa genre_df por la columna 'genre', toma una de sus columnas, 
#    y utiliza el método count() para encontrar el número de entradas por cada uno de 
#    los géneros representados; almacena los Series resultantes en
#    la variable genre_df_count

# 3) Ordena genre_df_count en orden descendente de frecuencia y guarda el resultado
#    en la variable genre_df_sorted

# 4) Devuelve un objeto Series con los primeros 15 valores de genre_df_sorted - los 15
#    géneros más populares (en un determinado día, en un determinado periodo de tiempo)

# Escribe tu función aquí

    # filtrado consecutivo
    # genre_df solo almacenará aquellas filas df en las que el día sea igual a day=
    genre_df = df[(df['day_reproduced'] == day)] # escribe tu código aquí
 # genre_df solo almacenará aquellas filas df en las que el tiempo sea menos que time2=
    genre_df = genre_df[(genre_df['time'] < time2)] # escribe tu código aquí
# genre_df solo almacenará aquellas filas df en las que el tiempo sea mayor que time1=
    genre_df = genre_df[(genre_df['time'] > time1)] # escribe tu código aquí
# agrupa el DataFrame filtrado por la columna con los nombres de los géneros, toma la columna de género, y encuentra el número de filas por cada género con el método count()
    genre_df_grouped = genre_df.groupby('genre').count()# escribe tu código aquí
# ordenaremos el resultado en orden descendente (por lo que los géneros más populares aparecerán primero en el objeto Series)
    genre_df_sorted = genre_df_grouped.sort_values(by='genre',ascending= False)# escribe tu código aquí
# devolveremos el objeto Series que almacena los 15 géneros más populares en un día determinado en un periodo de tiempo determinado
    return genre_df_sorted[:15]


# Compara los resultados de la función `genre_weekday()`para Springfield y Shelbyville el lunes por la mañana (de 7 a 11) y el viernes por la tarde (de 17:00 a 23:00):

# In[142]:


genre_weekday_df = genre_weekday(spr_general, 'Monday', '7:00:00', '11:00:00')
print(genre_weekday)# llamando a la función para el lunes por la mañana en Springfield (utilizando spr_general en vez de la tabla df)


# In[139]:


# llamando a la función para el lunes por la mañana en Shelbyville (utilizando shel_general en vez de la tabla df)


# In[ ]:


# llamando a la función para el viernes por la tarde en Springfield


# In[ ]:


# llamando a la función para el viernes por la tarde en Shelbyville


# **Conclusión**
# 
# Habiendo comparado los 15 géneros más populares del lunes por la mañana podemos concluir lo siguiente:
# 
# 1. Los usuarios de Springfield y Shelbyville escuchan música similar. Los cinco géneros más populares son los mismos, solo rock y electrónica han intercambiado posiciones.
# 
# 2. En Springfield el número de valores ausentes resultaron ser tan altos que el valor `'unknown'` llegó al décimo. Esto significa que los valores ausentes forman una parte considerable de los datos, lo que podría ser la base de la cuestión sobre la fiabilidad de nuestras conclusiones.
# 
# Para el viernes por la tarde, la situación es similar. Los géneros individuales varían algo pero, en general, los 15 más populares son parecidos en las dos ciudades.
# 
# De esta forma, la segunda hipótesis ha sido parcialmente demostrada:
# * Los usuarios escuchan música similar al principio y al final de la semana.
# * No hay una gran diferencia entre Springfield y Shelbyville. En ambas ciudades, el pop es el género más popular.
# 
# Sin embargo, el número de valores ausentes hace este resultado un tanto cuestionable. En Springfield, hay tantos que afectan a nuestros 15 más populares. De no faltarnos esos valores, las cosas podrían parecer diferentes.

# [Volver a Contenidos](#back)

# ### Hipótesis 3: preferencias de género en Springfield y Shelbyville <a id='genre'></a>
# 
# Hipótesis: Shelbyville ama la música rap. A los ciudadanos de Springfield les gusta más el pop.

# Agrupa la tabla `spr_general` por género y encuentra el número de canciones reproducidas de cada género con el método `count()`. Después, ordena el resultado en orden descendente y guárdalo en `spr_genres`.

# In[ ]:


# en una línea: agrupa la tabla spr_general por la columna 'genre', 
# cuenta los valores 'genre' con count() en la agrupación, 
# ordena el Series resultante en orden descendiente, y almacénalo en spr_genres


# Imprime las 10 primeras filas de `spr_genres`:

# In[ ]:


# imprimiendo las 10 primeras filas de spr_genres


# Ahora haz lo mismo con los datos de Shelbyville.
# 
# Agrupa la tabla `shel_general` por género y encuentra el número de canciones reproducidas de cada género. Después, ordena el resultado en orden descendente y guárdalo en la tabla `shel_genres`:
# 

# In[ ]:


# en una línea: agrupa la tabla shel_general por la columna 'genre', 
# cuenta los valores 'genre' en el agrupamiento con count(), 
# ordena el Series resultante en orden descendente y guárdalo en shel_genres


# Imprime las 10 primeras filas de `shel_genres`:

# In[ ]:


# imprimiendo las 10 primeras filas de shel_genres


# **Conclusión**

# La hipótesis ha sido parcialmente demostrada:
# * La música pop es el género más popular en Springfield, tal como se esperaba.
# * Sin embargo, la música pop ha resultado ser igual de popular en Springfield que en Shelbyville y el rap no estaba entre los 5 más populares en ninguna de las ciudades.
# 

# [Volver a Contenidos](#back)

# # Conclusiones <a id='end'></a>

# Hemos probado las siguientes tres hipótesis:
# 
# 1. La actividad de los usuarios difiere dependiendo del día de la semana y de las distintas ciudades. 
# 2. Los lunes por la mañana los residentes de Springfield y Shelbyville escuchan géneros distintos. Lo mismo ocurre con los viernes por la noche.
# 3. Los oyentes de Springfield y Shelbyville tienen distintas preferencias. En ambas ciudades, Springfield y Shelbyville, se prefiere el pop.
# 
# Tras analizar los datos, concluimos:
# 
# 1. La actividad del usuario en Springfield y Shelbyville depende del día de la semana aunque las ciudades varían de diferentes formas. 
# 
# La primera hipótesis ha sido aceptada completamente.
# 
# 2. Las preferencias musicales no varían significativamente en el transcurso de la semana en Springfield y Shelbyville. Podemos observar pequeñas diferencias en el orden los lunes, pero:
# * En Springfield y Shelbyville la gente lo que más escucha es la música pop.
# 
# Así que no podemos aceptar esta hipótesis. También debemos tener en cuenta que el resultado podría haber sido diferente si no fuera por los valores ausentes.
# 
# 3. Resulta que las preferencias musicales de los usuarios de Springfield y Shelbyville son bastante parecidas.
# 
# La tercera hipótesis es rechazada. Si hay alguna diferencia en las preferencias no se puede observar en los datos.
# 
# ### Nota 
# En los proyectos reales, la investigación supone el estudio de hipótesis estadísticas que es más preciso y cuantitativo. También ten en cuenta que no siempre podemos sacar conclusiones sobre una ciudad entera basándonos en datos de una sola fuente.
# 
# Analizarás el estudio de hipótesis en el sprint de análisis estadístico de datos.

# [Volver a Contenidos](#back)
