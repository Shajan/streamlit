import streamlit as st
from st_aggrid import AgGrid # pip install streamlit-aggrid

import pandas as pd

# Create a sample dataframe
data = {
    'Column A': [1, 2, 3, 4, 5],
    'Column B': ['A', 'B', 'C', 'D', 'E'],
    'Column C': [True, False, True, False, True]
}
df = pd.DataFrame(data)

# Title for the Streamlit app
st.title('Streamlit Ag-Grid Example')

# Display the dataframe as an interactive AgGrid
AgGrid(df)

