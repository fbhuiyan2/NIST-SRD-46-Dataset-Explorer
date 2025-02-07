import streamlit as st
import pandas as pd

def get_filtered_df(df_main):
    filtered_df = df_main.copy()

    if metal_selection:
        filtered_df = filtered_df[filtered_df['Metal'] == metal_selection]


    if ligand_class_selection:
        filtered_df = filtered_df[
            filtered_df['Ligand_class'].isin(ligand_class_selection)
        ]

    if ligand_selection:
        filtered_df = filtered_df[filtered_df['Ligand'].isin(ligand_selection)]

    return filtered_df

# Load dataset with caching
@st.cache_data
def load_data():
    df = pd.read_csv("db_clean_gzip_compressed", compression='gzip')  
    return df

df_main = load_data()

# App title and description
st.title('🔍 Metal-Ligand Query App')
st.markdown("**Data Source: National Institute of Standards and Technology (NIST)**")
st.write("Filter the dataset by selecting metals, ligand classes, and ligands. Leave blank for no preference.")

# Sidebar with dataset info
with st.sidebar:
    st.subheader("Dataset Overview")
    st.write(f"📌 Total entries: {df_main.shape[0]}")
    st.write(f"🧪 Unique metals: {df_main['Metal'].nunique()}")
    st.write(f"🔗 Unique ligands: {df_main['Ligand'].nunique()}")
    st.write(f"🛠️ Unique ligand classes: {df_main['Ligand_class'].nunique()}")

# Search criteria
col1, col2, col3 = st.columns(3)

with col1:
    metal_selection = st.selectbox('Select metal:', options=[''] + sorted(df_main['Metal'].unique()))

with col2:
    if metal_selection:
        ligand_class_options = sorted(df_main[df_main['Metal'] == metal_selection]['Ligand_class'].unique())
    else:
        ligand_class_options = sorted(df_main['Ligand_class'].unique())
        
    ligand_class_selection = st.multiselect('Select ligand class(es):', options=sorted(ligand_class_options))

# Update available ligands based on ligand class selection
if ligand_class_selection:
    ligand_options = sorted(df_main[df_main['Ligand_class'].isin(ligand_class_selection)]['Ligand'].unique())
    if metal_selection:
        ligand_options = sorted(df_main[(df_main['Metal'] == metal_selection) & (df_main['Ligand_class'].isin(ligand_class_selection))]['Ligand'].unique())
else:
    if metal_selection:
        ligand_options = sorted(df_main[df_main['Metal'] == metal_selection]['Ligand'].unique())
    else:
        ligand_options = sorted(df_main['Ligand'].unique())

with col3:
    ligand_selection = st.multiselect('Select ligand(s):', options=sorted(ligand_options))

# Apply filters
filtered_df = get_filtered_df(df_main)

# Display results
st.subheader("🔎 Filtered Results")
if not filtered_df.empty:
    st.write(f"✅ **Total results found:** {filtered_df.shape[0]}")
    
    # Display results in an expandable container
    with st.expander("📄 View Filtered Data"):
        st.dataframe(filtered_df)

    # Bar chart visualization (if relevant)
    st.subheader("📊 Data Distribution")
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.markdown("<p style='text-align: center; color: white;'>Ligand class(es)</p>", unsafe_allow_html=True)
        st.bar_chart(filtered_df['Ligand_class'].value_counts(), use_container_width=True, y_label = "Count")

    with col_chart2:
        st.markdown("<p style='text-align: center; color: white;'>Ligand(s)</p>", unsafe_allow_html=True)
        st.bar_chart(filtered_df['Ligand'].value_counts(), use_container_width=True, y_label = "Count")

    # Download option
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="⬇️ Download results as CSV",
        data=csv,
        file_name='filtered_data.csv',
        mime='text/csv'
    )
else:
    st.warning("⚠️ No results found. Try adjusting the filters.")



