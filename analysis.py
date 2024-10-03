import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv('data/uk_expenditure.csv', skip_blank_lines=True)
    df = df.replace({'z': pd.NA, '': pd.NA})
    numeric_cols = ['t_expenditure_millions', 't_expenditure_real_terms_millions', 'pt_expenditure_of_gdp']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df['time_period'] = df['time_period'].astype(str)
    df['year'] = df['time_period'].str[:4].astype(int)
    return df

# Load data
df = load_data()

# Streamlit app layout
st.title("UK Education Expenditure Analysis (2015-2023)")

# Display the first few rows of the data
st.write("First few rows of the data:")
st.write(df.head())

# Sidebar for user input
st.sidebar.header("User Input Features")
education_function = st.sidebar.selectbox("Select Education Function", df['education_function'].unique())
expenditure_type = st.sidebar.selectbox("Select Expenditure Type", df['expenditure_type'].unique())
expenditure_level = st.sidebar.selectbox("Select Expenditure Level", df['expenditure_level'].unique())

# Filter data based on user input
filtered_data = df[
    (df['education_function'] == education_function) &
    (df['expenditure_type'] == expenditure_type) &
    (df['expenditure_level'] == expenditure_level)
]

# Display filtered data
st.subheader("Filtered Data")
st.write(filtered_data)

# Total expenditure over the years
st.subheader("Total Expenditure Over Time")
total_expenditure = filtered_data.groupby('year')['t_expenditure_millions'].sum().reset_index()
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.lineplot(data=total_expenditure, x='year', y='t_expenditure_millions', marker='o', ax=ax1)
ax1.set_title(f'Total {expenditure_type} Expenditure for {education_function} Over Time')
ax1.set_xlabel('Year')
ax1.set_ylabel('Expenditure (Millions)')
plt.xticks(rotation=45)
st.pyplot(fig1)
plt.close(fig1)  # Close the figure after rendering

# Expenditure breakdown by type
st.subheader("Expenditure Breakdown by Type")
expenditure_breakdown = filtered_data.groupby(['year', 'expenditure_type'])['t_expenditure_millions'].sum().reset_index()
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(data=expenditure_breakdown, x='year', y='t_expenditure_millions', hue='expenditure_type', ax=ax2)
ax2.set_title(f'Expenditure Breakdown for {education_function} by Type Over Time')
ax2.set_xlabel('Year')
ax2.set_ylabel('Expenditure (Millions)')
plt.xticks(rotation=45)
st.pyplot(fig2)
plt.close(fig2)  # Close the figure after rendering

# Insights
st.subheader("Insights")
if not filtered_data.empty:
    latest_year = filtered_data['year'].max()
    latest_data = filtered_data[filtered_data['year'] == latest_year]
    total_expenditure_latest = latest_data['t_expenditure_millions'].sum()
    st.write(f"In the most recent year ({latest_year}), the total {expenditure_type.lower()} expenditure for {education_function} at the {expenditure_level.lower()} level was **£{total_expenditure_latest:,.2f} million**.")
else:
    st.write("No data available for the selected filters.")