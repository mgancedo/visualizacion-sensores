import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

st.set_page_config(layout="wide")
st.title("📊 Visualización de Sensores CNC")

# 📁 Cargar todos los archivos .feat de la carpeta 'data'
DATA_FOLDER = 'data'
if not os.path.exists(DATA_FOLDER):
    st.warning(f"📁 Crea una carpeta llamada `{DATA_FOLDER}` y sube tus archivos `.feat` allí.")
else:
    files = [f for f in os.listdir(DATA_FOLDER) if f.endswith('.feat')]
    if not files:
        st.warning("🔍 No hay archivos .feat en la carpeta.")
    else:
        # 🧩 Cargar y concatenar todos los archivos
        dfs = []
        for file in files:
            df = pd.read_feather(os.path.join(DATA_FOLDER, file))
            dfs.append(df)
        df_all = pd.concat(dfs)
        df_all['DateTime'] = pd.to_datetime(df_all['DateTime'])

        # 📅 Selección de día
        min_date = df_all['DateTime'].dt.date.min()
        max_date = df_all['DateTime'].dt.date.max()
        selected_date = st.date_input("Selecciona una fecha", value=min_date, min_value=min_date, max_value=max_date)

        df_day = df_all[df_all['DateTime'].dt.date == selected_date]

        if df_day.empty:
            st.error("⚠️ No hay datos para la fecha seleccionada.")
        else:
            # ✅ Selección de variables
            st.sidebar.header("📌 Variables a visualizar")
            selected_group = st.sidebar.radio("Selecciona un grupo:", [
                "Temperaturas 1 y 2",
                "Motor Temperature Spindle",
                "Spindle Power and Torque",
                "Commanded y Actual Spindle Speed"
            ])

            groups = {
                "Temperaturas 1 y 2": ['UI2748-01_Temperature_Sensor_1', 'UI2748-01_Temperature_Sensor_2'],
                "Motor Temperature Spindle": ['UI2748-01_Motor_Temperature'],
                "Spindle Power and Torque": ['UI2748-01_Spindle_Torque', 'UI2748-01_Spindle_Power'],
                "Commanded y Actual Spindle Speed": ['UI2748-01_Commanded_Spindle_Speed', 'UI2748-01_Actual_Spindle_Speed']
            }

            selected_tags = groups[selected_group]
            df_plot = df_day[df_day['TagName'].isin(selected_tags)]

            # 📈 Graficar
            st.subheader(f"📅 Datos de {selected_date.strftime('%Y-%m-%d')}")
            fig, ax = plt.subplots(figsize=(14, 5))
            for tag in selected_tags:
                sub_df = df_plot[df_plot['TagName'] == tag]
                ax.plot(sub_df['DateTime'], sub_df['Value'], label=tag)
            ax.set_title("Evolución de variables seleccionadas")
            ax.set_xlabel("Hora")
            ax.set_ylabel("Valor")
            ax.legend()
            st.pyplot(fig)
