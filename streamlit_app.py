import streamlit as st
import pandas as pd

# Load dataset with caching
@st.cache_data
def load_data():
    df = pd.read_csv("db_clean_gzip_compressed", compression='gzip')  
    return df

df_main = load_data()

# App title and description
st.title('🔍 Metal-Ligand Query App')
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
    metal_selection = st.multiselect('Select metal(s):', options=sorted(df_main['Metal'].unique()))

with col2:
    ligand_class_selection = st.selectbox('Select ligand class:', options=[''] + sorted(df_main['Ligand_class'].unique()))

# Update available ligands based on ligand class selection
if ligand_class_selection:
    available_ligands = df_main[df_main['Ligand_class'] == ligand_class_selection]['Ligand'].unique()
else:
    available_ligands = df_main['Ligand'].unique()

with col3:
    ligand_selection = st.multiselect('Select ligand(s):', options=sorted(available_ligands))

# Apply filters
filtered_df = df_main.copy()

if metal_selection:
    filtered_df = filtered_df[filtered_df['Metal'].isin(metal_selection)]
if ligand_selection:
    filtered_df = filtered_df[filtered_df['Ligand'].isin(ligand_selection)]
if ligand_class_selection:
    filtered_df = filtered_df[filtered_df['Ligand_class'] == ligand_class_selection]

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
        st.bar_chart(filtered_df['Metal'].value_counts())

    with col_chart2:
        st.bar_chart(filtered_df['Ligand'].value_counts())

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

# Reset Filters Button
if st.button("🔄 Clear Filters"):
    st.experimental_rerun()

