import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.graph_objects as go

# Load the dataset from the CSV file
DS_job_salaries_data = pd.read_csv('ds_job_salaries_cleaned.csv')

st.set_page_config(layout="wide")
st.markdown("### 📌 Above by Abhinav Rai")
st.title("📊 Data Science Job Salary Analysis")

# SECTION 1
st.header("🔍 Section 1: Job Roles and Experience Level")

st.markdown("""
**Key Insights:**
- Most Data Science jobs require Senior-level/Expert experience level.
- The most common job titles are Data Scientist, Data Engineer, Data Analyst, and Machine Learning Engineer.
""")

# Chart 1 - Company Size vs Experience Level
st.subheader("Company Size vs Experience Level")
size_level_pivot = pd.crosstab(DS_job_salaries_data['company_size'], DS_job_salaries_data['experience_level'])
fig, ax = plt.subplots(figsize=(16, 6))
size_level_pivot.plot.bar(ax=ax)
for container in ax.containers:
    ax.bar_label(container)
st.pyplot(fig)

# Chart 2 - Top Roles by Salary and Openings
st.subheader("Top Roles by Salary and Openings")
top_ds_roles = DS_job_salaries_data.groupby('job_title')['salary_in_usd'].mean().sort_values(ascending=False).head(10)
top_dr = DS_job_salaries_data['job_title'].value_counts().head(10)

fig, axes = plt.subplots(1, 2, figsize=(20, 7))
sns.barplot(y=top_ds_roles.index, x=top_ds_roles, palette='viridis', ax=axes[0])
axes[0].set_title("Top Roles by Mean Salary")
sns.barplot(x=top_dr, y=top_dr.index, palette='plasma', ax=axes[1])
axes[1].set_title("Top 10 Roles by Openings")
st.pyplot(fig)

# SECTION 2
st.header("🌍 Section 2: Geography and Salaries")

st.markdown("""
**Key Insights:**
- Most Data Science employees and companies are based in the United States.
- Russia offers the highest average salary, followed closely by the U.S.
""")

# Chart 1 - Employee Residence
st.subheader("Employee Residence with >10 Employees")
residence_count = DS_job_salaries_data['employee_residence'].value_counts()
filtered_residence_count = residence_count[residence_count > 10]
fig, ax = plt.subplots(figsize=(16, 6))
filtered_residence_count.sort_values().plot(kind='barh', color='lightgreen', edgecolor='black', ax=ax)
ax.set_title('Employee Residence')
st.pyplot(fig)

# Chart 2 - Salary by Company Location
st.subheader("Salary by Company Location")
fig, ax = plt.subplots(figsize=(16, 6))
sns.lineplot(y='salary_in_usd', x='company_location', data=DS_job_salaries_data, ax=ax)
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
st.pyplot(fig)

# SECTION 3
st.header("📈 Section 3: Yearly Growth Trends")

st.markdown("""
**Key Insights:**
- Salary and job count have increased steadily over the years.
""")

col5, col6 = st.columns(2)

with col5:
    st.subheader("Salary Distribution by Year")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.kdeplot(data=DS_job_salaries_data, x='salary_in_usd', hue='work_year', fill=True, ax=ax)
    st.pyplot(fig)

with col6:
    st.subheader("Remote Ratio by Work Year")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.countplot(x='job_type', data=DS_job_salaries_data, hue='work_year', ax=ax)
    for container in ax.containers:
        ax.bar_label(container)
    st.pyplot(fig)

# SECTION 4
st.header("💼 Section 4: Employment Type & Company Size Impact")

st.markdown("""
**Key Insights:**
- Most positions are full-time.
- Medium and large companies pay significantly more than small-sized companies.
""")

col7, col8 = st.columns(2)

with col7:
    st.subheader("Employment Type Distribution")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.countplot(x='employment_type', data=DS_job_salaries_data, ax=ax)
    for container in ax.containers:
        ax.bar_label(container)
    st.pyplot(fig)

with col8:
    st.subheader("Mean Salary vs Company Size")
    mean_s_cmp_size = DS_job_salaries_data.groupby('company_size')['salary_in_usd'].mean().sort_values()
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    sns.barplot(x=mean_s_cmp_size.index, y=mean_s_cmp_size, hue=mean_s_cmp_size.index,
                palette={'Small': 'red', 'Medium': 'brown', 'Large': 'blue'}, ax=axes[0])
    axes[0].set_title("Mean Salary by Company Size")

    sns.boxenplot(data=DS_job_salaries_data, x='company_size', y='salary_in_usd', hue='company_size',
                  palette={'Small': 'red', 'Medium': 'brown', 'Large': 'blue'}, ax=axes[1])
    axes[1].set_title("Company Size vs Salary Distribution")
    st.pyplot(fig)

# SECTION 5
st.header("Section 5: USA Average Salary Indicator")

st.markdown("""
**Key Insight:**
- The average salary for Data Science jobs in the U.S. is very competitive.
""")

# Gauge chart
us_avg_salary = DS_job_salaries_data[DS_job_salaries_data['company_location'] == 'United States']['salary_in_usd'].mean()
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=us_avg_salary,
    title={'text': "Avg Salary in United States (USD)", 'font': {'color': "white"}},
    gauge={
        'axis': {'range': [0, DS_job_salaries_data['salary_in_usd'].max()], 'tickcolor': "white"},
        'bar': {'color': "deepskyblue"},
        'bgcolor': "gray",
        'borderwidth': 2,
        'bordercolor': "white",
        'steps': [
            {'range': [0, us_avg_salary], 'color': 'lightgray'},
            {'range': [us_avg_salary, DS_job_salaries_data['salary_in_usd'].max()], 'color': 'lightgray'}
        ],
    },
    number={'font': {'color': 'white'}}
))
fig.update_layout(paper_bgcolor="gray", plot_bgcolor="gray")
st.plotly_chart(fig, use_container_width=True)
