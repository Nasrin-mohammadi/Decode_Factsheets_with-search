import sqlite3
import pandas as pd

# List of database file names, corresponding to your sheets
databases = {
    'Methods T1.2': 'Methods_T1.2.db',
    'Methods T1.3': 'Methods_T1.3.db',
    'Methods T1.4': 'Methods_T1.4.db',
    'Methods T2.1': 'Methods_T2.1.db',
    'Methods T2.2': 'Methods_T2.2.db',
    'Methods T2.4': 'Methods_T2.4.db'
}

def get_columns(sheet_name):
    """ Get the columns of a specific table. """
    db_name = databases.get(sheet_name)
    if not db_name:
        return None
    
    # Open a connection to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Query just the first row to get column names
    cursor.execute(f'SELECT * FROM "{sheet_name}" LIMIT 1')
    columns = [description[0] for description in cursor.description]

    # Close the connection
    conn.close()

    return columns

def query_database(sheet_name, selected_columns=None, search_query=None):
    """ Query the database for all data or specific columns. """
    db_name = databases.get(sheet_name)
    if not db_name:
        return None
    
    # Open a connection to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Start building the query
    query = f'SELECT * FROM "{sheet_name}"'
    params = []

    # Add search condition if search_query is provided
    if search_query:
        search_conditions = []
        for col in selected_columns:
            if col != 'All columns':  # Skip the 'All columns' option
                search_conditions.append(f'"{col}" LIKE ?')  # Use parameterized queries to prevent SQL injection
                params.append(f'%{search_query}%')  # Wildcard search
        
        # Combine conditions with OR
        if search_conditions:
            query += ' WHERE ' + ' OR '.join(search_conditions)

    cursor.execute(query, params)

    # Fetch all results
    rows = cursor.fetchall()

    # Get the column names
    columns = [description[0] for description in cursor.description]

    # Convert the results to a DataFrame for better display
    df = pd.DataFrame(rows, columns=columns)

    # Filter based on selected columns
    if selected_columns and 'All columns' not in selected_columns:
        df = df[selected_columns]

    # Close the connection
    conn.close()

    return df
