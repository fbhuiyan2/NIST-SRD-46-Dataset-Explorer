import streamlit as st
import pandas as pd

# Load your DataFrame (replace with actual data source)
@st.cache_data
def load_data():
    # Example: Read from CSV (replace with actual file path)
    df = pd.read_csv("db_clean.csv")  
    return df

df_main = load_data()

# Set the app title
st.title('Metal-Ligand Query App')

st.write('Please select search criteria below. Leave blank for no preference.')

# Get unique values for dropdown menus, adding an empty option for 'no preference'
metals = [''] + sorted(df_main['Metal'].unique())
ligand_classes = [''] + sorted(df_main['Ligand_class'].unique())

# User selections
metal_selection = st.selectbox('Select metal:', options=metals)
ligand_class_selection = st.selectbox('Select ligand class:', options=ligand_classes)

# Update ligand options based on selected ligand class
if ligand_class_selection:
    # Filter ligands based on selected ligand class
    available_ligands = df_main[df_main['Ligand_class'] == ligand_class_selection]['Ligand'].unique()
    ligands = [''] + sorted(available_ligands)
    ligand_label = f"Available ligands in ligand class: {ligand_class_selection}"
else:
    # If no ligand class is selected, show all ligands
    ligands = [''] + sorted(df_main['Ligand'].unique())
    ligand_label = "Select ligand:"

ligand_selection = st.selectbox(ligand_label, options=ligands)

# Apply filters based on user selections
filtered_df = df_main.copy()

if metal_selection:
    filtered_df = filtered_df[filtered_df['Metal'] == metal_selection]
if ligand_selection:
    filtered_df = filtered_df[filtered_df['Ligand'] == ligand_selection]
if ligand_class_selection:
    filtered_df = filtered_df[filtered_df['Ligand_class'] == ligand_class_selection]

# Display the filtered DataFrame
if not filtered_df.empty:
    st.write('Filtered Results:')
    st.write(filtered_df)
    # Display total results count
    st.write(f"**Total results found:** {filtered_df.shape[0]}")
    
    # Add a download button for the filtered DataFrame
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='filtered_data.csv',
        mime='text/csv'
    )
else:
    st.write('No results found for the given criteria.')
