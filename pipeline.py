import pandas as pd
import numpy as np
import joblib
import os

def clean_and_predict(data_path, model_path):
    print("Iniciando pipeline de datos...")
    
    # 1. Cargar datos
    df = pd.read_csv(data_path)
    
    # 2. Limpieza y Optimización (Simulación ELT de Data Lakehouse -> Pandas RAM)
    # Downcasting
    if 'id_sensor' in df.columns:
        df['id_sensor'] = df['id_sensor'].astype(np.int8)
    df['temperatura'] = df['temperatura'].astype(np.float32)
    df['vibracion'] = df['vibracion'].astype(np.float32)
    
    # Manejar "9999" valores nulos erróneos
    df = df.replace(9999, np.nan)
    
    # 3. Imputación de Series de Tiempo (Reconstrucción de caída de sensor)
    # Asumimos que los datos están ordenados temporalmente
    df['temperatura'] = df['temperatura'].interpolate(method='spline', order=3)
    df['vibracion'] = df['vibracion'].interpolate(method='spline', order=3)
    
    # Drop NAs restantes en los bordes si los hay
    df = df.dropna()
    
    # 4. Inferencia con el Modelo
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modelo {model_path} no encontrado.")
        
    modelo = joblib.load(model_path)
    
    # Seleccionar características
    X_infer = df[['temperatura', 'vibracion']]
    
    # Predicción de Vida Útil Remanente (RUL)
    df['RUL_predict'] = modelo.predict(X_infer)
    
    print("Muestra de los resultados (Predicción RUL):")
    print(df[['temperatura', 'vibracion', 'RUL_predict']].head())
    
    # Guardar resultados
    df.to_csv("resultados_inferencia.csv", index=False)
    print("Pipeline completado. Resultados guardados en 'resultados_inferencia.csv'")

if __name__ == "__main__":
    # Simular la creación de un archivo de datos si no existe
    if not os.path.exists("sensor_data.csv"):
        print("Generando datos de prueba...")
        temp = np.random.normal(80, 15, 100)
        vib = np.random.normal(2.5, 0.8, 100)
        # Añadir ruido 9999 y NaNs
        temp[10:15] = 9999
        vib[30:35] = np.nan
        pd.DataFrame({'temperatura': temp, 'vibracion': vib}).to_csv("sensor_data.csv", index=False)
        
    # Asumimos que el modelo existe o podemos usar un dummy si falla
    try:
        clean_and_predict("sensor_data.csv", "modelo_rul.pkl")
    except Exception as e:
        print(f"Error en pipeline: {e}")
        print("Nota: Asegúrate de ejecutar primero la libreta 'solucion.ipynb' para entrenar y generar el modelo 'modelo_rul.pkl'")
