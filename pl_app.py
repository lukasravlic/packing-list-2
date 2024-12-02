import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Data Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar para seleccionar la marca
with st.sidebar:
    st.header("Seleccione la Marca")
    brand = st.selectbox(
        "Elija la marca para procesar los datos:",
        options=["Maruti Suzuki"],  # Se pueden agregar más marcas en el futuro
    )

# Título principal
st.title("Data Analysis Dashboard - Maruti Suzuki")
st.markdown("---")

# Subir y procesar archivos
st.subheader("Suba sus archivos Excel")

uploaded_files = st.file_uploader(
    "Cargue archivos Excel (.xlsx)",
    type="xlsx",
    accept_multiple_files=True
)

if uploaded_files:
    data_frames = []
    for uploaded_file in uploaded_files:
        try:
            # Leer cada archivo Excel con header=1
            df = pd.read_excel(uploaded_file, engine="openpyxl", header=1)

            # Eliminar la primera fila después del header
            df = df.iloc[1:, :]  # Esto elimina la fila en el índice 0

            data_frames.append(df)

            # Mostrar vista previa
            st.write(f"Archivo cargado: **{uploaded_file.name}**:")
            #st.dataframe(df.head())  # Mostrar las primeras filas del archivo
        except Exception as e:
            st.error(f"Error al leer el archivo {uploaded_file.name}: {e}")

    # Combinar todos los archivos cargados
    if data_frames:
        combined_data = pd.concat(data_frames, ignore_index=True)
        st.success("Archivos combinados exitosamente.")

        combined_data = combined_data[
            ['Cod. Material de Proveedor despachado', 'Cantidad solicitada', 'Nro. De Orden – Prefijo']]

        # Inputs para agregar nuevas columnas
        st.subheader("Ingrese datos para agregar nuevas columnas")

        # Campo de texto para nueva columna
        new_column_text = st.text_input("DT", value="Numero de DT")

        # Dropdown para "Tipo de Contenedor"
        container_type = st.selectbox(
            "Seleccione el tipo de contenedor",
            options=["40HC", "4'STD", "Tipo 3", "Tipo 4"]
        )

        # Campo de texto para "Contenedor"
        container = st.text_input("Ingrese el nombre del contenedor", value="Contenedor por defecto")

        if new_column_text and container_type and container:
            # Agregar las nuevas columnas al DataFrame
            combined_data["DT"] = new_column_text
            combined_data["Tipo de Contenedor"] = container_type
            combined_data["Contenedor"] = container

            # Mostrar tabla con las nuevas columnas
            st.subheader("Tabla Combinada con Nuevas Columnas")
            st.dataframe(combined_data)

            # Botón para descargar la tabla combinada
            csv_data = combined_data.to_csv(index=False)
            st.download_button(
                label="Descargar tabla combinada como CSV",
                data=csv_data,
                file_name="datos_combinados.csv",
                mime="text/csv"
            )
else:
    st.warning("Por favor, suba uno o más archivos Excel para continuar.")
