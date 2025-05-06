# Visualización de Sensores CNC

Aplicación Streamlit para visualizar variables críticas de sensores en un centro de mecanizado CNC a partir de archivos `.feat`.

## Funcionalidades

- Carga automática de todos los archivos `.feat` desde la carpeta `data/`
- Selector de fecha
- Visualización de grupos de variables: temperaturas, potencia, velocidad, etc.

## Requisitos

- Python 3.8+
- Streamlit
- pandas
- matplotlib
- pyarrow

## Ejecución local

```bash
streamlit run app.py
