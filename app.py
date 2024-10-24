import streamlit as st
import pandas as pd
from main import get_columns, query_database

# Streamlit app interface
st.title("FactSheets")

# List of available methods (databases)
methods = {
    'Methods T1.2': 'Methods_T1.2.db',
    'Methods T1.3': 'Methods_T1.3.db',
    'Methods T1.4': 'Methods_T1.4.db',
    'Methods T2.1': 'Methods_T2.1.db',
    'Methods T2.2': 'Methods_T2.2.db',
    'Methods T2.4': 'Methods_T2.4.db'
}

# Step 1: Select Method (Database)
sheet_name = st.selectbox('Select a Method:', list(methods.keys()))

if sheet_name:
    # Query the columns for the selected Method
    columns = get_columns(sheet_name)
    
    if columns:
        # Step 2: Select columns to display
        columns = ['All columns'] + columns
        selected_columns = st.multiselect('Select columns to display:', columns, default=['All columns'])

        # Step 3: Add search input
        search_query = st.text_input('Search for anything in the database:')

        # Query the database with selected columns and search query
        df = query_database(sheet_name, selected_columns, search_query)

        # Display the data
        if df is not None:
            st.dataframe(df)
