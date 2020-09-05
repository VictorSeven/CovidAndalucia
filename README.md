# CovidAndalucia
Weekly updated data about the coronavirus pandemic in Andalusia (Spain), with special focus in my city, Granada. Code is commented in English. Technical reports may appear [in my personal page.](https://victorseven.github.io/technical/)



## Intención

La idea de este repositorio es actualizar semanalmente los datos de la pandemia de Covid19 en Andalucía, usando los datos de la Junta. Por otro lado, mi interés principal es analizar la situación en Granada, aunque según vaya produciendo el código no descarto aplicar los análisis también a otras provincias. 

Todas las semanas escribiré un pequeño informe actualizado en mi [página personal](https://victorseven.github.io/articles/), tanto a nivel divulgativo, como uno más técnico, en caso de que fuera necesario.

## Metodología

Los datos son los ofrecidos semanalmente por la [Junta de Andalucía](https://www.juntadeandalucia.es/institutodeestadisticaycartografia/badea/informe/anual?CodOper=b3_2314&idNode=42348) . Para procesarlos, hago lo siguiente:

1. Descargar el fichero de Calc de la serie completa. Rellenar los campos sin definir con 0 (podría poner un `-1` para luego sustituir por `NaN`, pero no creo que sea necesario).
2. Copiar y pegar la tabla de datos (incluyendo cabecera) en un editor de texto plano (Gedit o Notepad).
3. Utilizar el script de Python para generar el archivo `data/datos_andalucia_ultimo.csv`. Este después ya puede analizarse. 

El `csv`  se puede cargar en un DataFrame de `pandas`. Tiene las columnas del dataset de la Junta, donde los espacios se han sustituido por barras bajas, es decir, `Fecha, Territorio, Confirmados_PCR, Confirmados_PCR_14_días, Confirmados_PCR_7_días, Total_confirmados, Hospitalizados, Total_UCI, Fallecidos, Curados`. 

Las gráficas calculan una media deslizante usando la función pre-asignada de Pandas para ello, `rolling`. Es posible definir los días que se utilizan. Para los fits, la función puede tomar cualquier método, y utiliza el paquete LmFit (que es una generalización de las rutinas de SciPy) para realizar calcular el mejor fit.

El error de los fit lo realizo de dos formas:

- Mediante el método integrado en LmFit, que mediante un test F de Fischer calcula la banda de confianza al 95% (es decir, la banda en la que el ajuste realizado se encuentra con un 95% de confianza).
- Usando el método _inocente_ de asumir que la mayor parte del error de los ajustes vendrán dados por el error en la tasa de crecimiento de la exponencial, y generando una banda al 95% de confianza con el error calculado de esta tasa de crecimiento de la exponencial. 

El segundo método siempre da unas bandas de error mayores. Ambas bandas están representadas alrededor del fit. 

## Colaboración y uso de datos

El código y los CSV aquí generados son libres, con la licencia GNU GPL 3. Puedes utilizarlos para jugar o realizar tus propios ajustes, siempre y cuando enlaces este repositorio -y, en caso de uses el código como base para construir otra cosa, lo liberes también.

Estoy encantado de recibir comentario o crítica sobre los procedimientos que he empleado. Cabe destacar que aunque mi investigación en general se centra en sistemas complejos no soy especialista en epidemiología, de modo que todas las aportaciones son bienvenidas.

## ¿Necesitas más?

Si te interesa el análisis de los datos de coronavirus en España, te recomiendo seguir el repositorio de [EsCovid19Data](https://github.com/montera34/escovid19data), y también cuentas de Twitter como la de [Saúl Arés](https://twitter.com/omeuxeito) o [Miguel Ángel Reinoso.](https://twitter.com/mianrey)