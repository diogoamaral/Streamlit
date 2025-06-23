# app.py
# © 2025 Águia Sistemas. Todos os direitos reservados.
# Desenvolvido por Diogo Cezar Amaral - Extrator de Movimentos Refeição por Data

import streamlit as st
import pandas as pd
# from io import BytesIO

# Function to filter data and return CSV content with original formatting
def filter_data_and_get_csv(df, start_date_str, end_date_str):
    # Convert date strings from DD/MM/YYYY to AAMMDD for filtering
    def ddmmyyyy_to_aammdd(date_str):
        day, month, year = date_str.split('/')
        return f'{year[2:]}{month}{day}'

    start_date_aammdd = ddmmyyyy_to_aammdd(start_date_str)
    end_date_aammdd = ddmmyyyy_to_aammdd(end_date_str)

    # Filter the DataFrame based on the date range in 'AAMMDD' format
    filtered_df = df[
        (df.iloc[:, 2] >= start_date_aammdd) &
        (df.iloc[:, 2] <= end_date_aammdd)
    ].copy()

    csv_output = filtered_df.to_csv(index=False, header=False, sep=';')
    return csv_output

# Streamlit app
st.set_page_config(layout="wide", page_title="Extrator Movimento Refeição")

st.title('Extrator de Movimentos Refeição por Data')

st.write(
    """
    Este aplicativo permite que você carregue um arquivo CSV do refeitório e filtre os dados por data.
    O arquivo deve estar no formato correto para que o filtro funcione corretamente.
    """
)

# File uploader
uploaded_file = st.file_uploader('Carregue seu arquivo CSV', type='csv')

if uploaded_file is not None:
    # Read the CSV file into a DataFrame without header
    df = pd.read_csv(uploaded_file, header=None, dtype=str)

    # Date input fields
    start_date_input = st.date_input('Data de Início', format="DD/MM/YYYY")
    end_date_input = st.date_input('Data de Fim', format="DD/MM/YYYY")

    if start_date_input and end_date_input:
        # Convert date inputs to strings
        start_date_str = start_date_input.strftime('%d/%m/%Y')
        end_date_str = end_date_input.strftime('%d/%m/%Y')

        # Filter data and prepare CSV for download
        csv_output = filter_data_and_get_csv(df.copy(), start_date_str, end_date_str)

        # Download button
        st.download_button(
            label="Baixar CSV Filtrado",
            data=csv_output,
            file_name="refeitorio_filtrado.txt",
            mime="text/csv"
        )        
else:
    st.text('Por favor, carregue um arquivo CSV para continuar.')

# Footer
st.markdown(
    "<hr style='margin-top:3em'>"
    "<center><small>© 2025 Águia Sistemas. Todos os direitos reservados.</small></center>",
    unsafe_allow_html=True
)