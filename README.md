# 🏭 Proyecto: Migración de Data Swamp a Data Lakehouse y Análisis Predictivo (RUL)

Este proyecto simula el proceso de modernización de arquitectura de datos para una fábrica ensambladora de vehículos. Pasamos de un "Data Swamp" (archivos CSV sucios procesados en memoria RAM) a un paradigma **ELT** preparado para un entorno distribuido, acompañado de un modelo de Machine Learning empaquetado en Docker.

## 📂 ¿Qué hace cada archivo?

1. **`solucion.ipynb` (El Cuaderno de Diseño y Entrenamiento):**
   - **Diagrama ELT:** Explica y justifica gráficamente el cambio de arquitectura (por qué ETL con Python tradicional falla por memoria y por qué usar un Lakehouse es escalable).
   - **Optimización de Dtypes:** Genera millones de filas para demostrar cómo convertir tipos de datos (`float64` a `float32`, e `int64` a enteros de 8 bits) reduce drásticamente el consumo de memoria.
   - **Imputación Spline:** Reconstruye matemáticamente datos faltantes (`NaN`) de sensores caídos sin usar el relleno con ceros, respetando la tendencia de la curva.
   - **Modelo de ML:** Entrena una Regresión Lineal Múltiple que toma la *Vibración* y *Temperatura* para predecir la Vida Útil Remanente (RUL) del motor. Exporta este "cerebro" al archivo `modelo_rul.pkl`.

2. **`pipeline.py` (El Código de Producción):**
   Es el script automatizado. Una vez que probamos las matemáticas en el cuaderno, este script hace el trabajo en la vida real. Lee datos nuevos (simulados), aplica la limpieza (elimina valores "9999", interpola faltantes), carga el `modelo_rul.pkl` y genera predicciones guardándolas en un CSV final.

3. **`Dockerfile` y `requirements.txt` (La Infraestructura):**
   El `Dockerfile` es la receta de construcción. Toma un sistema operativo Linux ultraligero, le instala Python y las librerías exactas (`requirements.txt` como `pandas`, `scikit-learn`), y copia el `pipeline.py` adentro. Esto garantiza que el código nunca falle por falta de librerías.

## 🐳 ¿Qué es Docker y qué significa el punto `.` al construir?
**Docker** resuelve el famoso problema de *"En mi máquina sí funciona"*. Lo que hace es empaquetar tu código, tus librerías y un mini-sistema operativo en una "caja" sellada (contenedor) que funciona idéntico en cualquier PC del mundo.

Cuando ejecutamos el comando `docker build -t motor-rul-pipeline .`:
- El **punto (`.`) al final** significa: *"Busca el archivo `Dockerfile` en esta misma carpeta exacta en la que estoy posicionado ahora, e incluye todo lo que hay aquí para construir la imagen"*.

---

## 🚀 Instrucciones de Uso (Para probar el proyecto)

Sigue estos pasos para ejecutar el proyecto en tu entorno local:

### Paso 1: Entrenar el modelo (Entorno de Análisis)
1. Clona este repositorio: `git clone https://github.com/FerGuzman65/ProyectoBD.git`
2. Entra a la carpeta del proyecto en tu terminal: `cd ProyectoBD`
3. Abre el archivo **`solucion.ipynb`** en tu editor preferido (Visual Studio Code, Jupyter Lab, etc).
4. Ejecuta todas las celdas de arriba hacia abajo. Esto probará la teoría y generará automáticamente el archivo `modelo_rul.pkl`.

### Paso 2: Desplegar en Producción con Docker
Asegúrate de tener [Docker Desktop](https://www.docker.com/products/docker-desktop) instalado y corriendo en tu computadora.

1. Abre una terminal dentro de la carpeta del proyecto.
2. Construye la imagen de Docker ejecutando:
   ```bash
   docker build -t motor-rul-pipeline .
   ```
3. Ejecuta el contenedor para ver la magia en vivo:
   ```bash
   docker run motor-rul-pipeline
   ```
   *(Verás en la terminal cómo se simula la caída de sensores, cómo se limpian los datos y finalmente se imprimen las predicciones de Vida Útil Remanente de los motores).*
