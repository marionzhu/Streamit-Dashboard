import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import plotly.express as px
from streamlit.components.v1 import html

# Set the title and icon of the app
st.set_page_config(
    page_title="Welcome to the Data World",
    page_icon="🌍",
    layout="wide"
)

# set header 
st.header('Welcome to the Data World ! 🌍')
st.markdown('Are you trying to search for a job in data field after graduation?')

# Header Styling
st.markdown(
    """
    <style> 
        h2 {
            color: #8dd3c7;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# set sidebar
sidebar = st.sidebar.selectbox('Navigation Page', ('Overview', 'Jobs by Categrory',\
                                                    'Jobs by Country', 'About Dataset'))

# load data
# @st.cache
df = pd.read_csv('/Users/zhusijie/Desktop/R/R project/jobs_in_data.csv')

# overview
if sidebar == 'Overview':
    st.subheader('Overview')
    st.markdown('This data exploration provides insights into the data science job market. Consider these findings alongside your skills, interests, and career goals to make informed decisions.')
    st.header(' ')

# Metrics
    html(
    """
<div id="numbers">
    <div>
        <label>Total Number of Jobs</label>
        <div><span class="counter">93</span>55</div>
    </div>
    <div>
        <label>Unique Job Titles</label>
        <div><span class="counter">125</span></div>
    </div>
    <div>
        <label>Companies Locations</label>
        <div><span class="counter">70</span></div>
    </div> 
</div>
    <style>
    body{
        font-family:sans-serif;
    }
    div#numbers{
        display:flex;
        gap:20px;
        justify-content: space-between; 
    }
    div#numbers > div{
        font-size:20px;
        color:white;
        background:#8dd3c7;
        padding:20px;
        flex-basis:320px;
        text-align:center;
    }
    div#numbers > div>label{
        font-size: 16px;
        font-weight: bold;
    }
    div#numbers > div > div{
        font-size:54px;
        font-weight:700;
    }
    </style>
    <script type="text/javascript">
    console.log("test")
        document.querySelectorAll(".counter").forEach(node=>{
            let limit=parseInt(node.textContent);
            let currentValue=0;
            if(limit<0 || isNaN(limit)){
                return
            }
            let stop=setInterval(()=>{
                currentValue++;
                node.textContent=currentValue;
                if(currentValue>=limit){
                    clearInterval(stop)
                }
            },2000/limit)
        })    
    </script>
    """
)

    st.header(' ')

# top 10 salary figure
    top_salary = df.groupby('job_title')['salary_in_usd'].mean().round().reset_index(name='salary').sort_values(by= 'salary',ascending = False).head(10)

    fig1 = px.bar(top_salary, y='job_title', x='salary', orientation = 'h', text_auto = True, color_discrete_sequence=px.colors.qualitative.Set3)
    fig1.update_layout(
    title='Top 10 Jobs by Salary',  # Add title here
    xaxis_title=None,  # Removes the x-axis label
    yaxis_title=None   # Removes the y-axis label
    )
    fig1.update_yaxes(categoryorder='total ascending')

# top 10 job number figure
    top_number = df.groupby('job_title').size().reset_index(name='nb_jobs').sort_values(by='nb_jobs', ascending=False).head(10)
    fig2 = px.bar(top_number, y = 'job_title', x='nb_jobs', orientation= 'h', text_auto = True, color_discrete_sequence=px.colors.qualitative.Set3)
    fig2.update_layout(
    title='Top 10 Jobs by Job Number', 
    xaxis_title=None,  
    yaxis_title=None   
    )
    fig2.update_yaxes(categoryorder='total ascending')

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)


# jobs by experience level
    experience = df.groupby('experience_level').agg({'job_title':'count', 'salary_in_usd':'mean'})\
        .round().rename(columns = {'job_title':'job numbers', 'salary_in_usd':'average salary'})
    experience.reset_index(inplace = True)  

    fig3 = px.pie(experience, values='job numbers', names='experience_level', color='experience_level',
             color_discrete_map={'Entry-level':'lightcyan',
                                 'Executive':'#5c9b90',
                                 'Mid-level':'#d2f0eb',
                                 'Senior':'#8dd3c7'})
    fig3.update_layout(
    title = 'Job numbers by experience level'
    )
    
    fig4 = px.bar(experience, y = 'average salary', x='experience_level', orientation= 'v', color = 'experience_level',
                  color_discrete_map={'Entry-level':'lightcyan',
                                 'Executive':'#5c9b90',
                                 'Mid-level':'#d2f0eb',
                                 'Senior':'#8dd3c7'}, text_auto = True)
    fig4.update_layout(
    title='Salaries by experience level', 
    xaxis_title=None,  
    yaxis_title=None 
    )

    st.header(' ')

    st.markdown('Experience Level has an impact on salary and jobs numbers, companies tend to hire more senior employees.')

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig3, use_container_width=True)
    with col2:
        st.plotly_chart(fig4, use_container_width=True)

    # jobs by company size 
    companies = df.groupby('company_size').agg({'job_title':'count', 'salary_in_usd':'mean'})\
        .round().rename(columns = {'job_title':'job numbers', 'salary_in_usd':'average salary'})
    companies.reset_index(inplace = True) 

    fig5 = px.pie(companies, values='job numbers', names='company_size', color='company_size',
             color_discrete_map={'L':'lightcyan',
                                 'M':'#8dd3c7',
                                 'S':'#5c9b90'})
    fig5.update_layout(
    title = 'Job numbers by company size'
    )

    fig6 = px.bar(companies, y = 'average salary', x='company_size', orientation= 'v', color = 'company_size',
                  color_discrete_map={'L':'lightcyan',
                                    'M':'#8dd3c7',
                                    'S':'#5c9b90'}, text_auto = True)
    fig6.update_layout(
    title='Salaries by company size', 
    xaxis_title=None,  
    yaxis_title=None 
    )
    
    st.header(' ')

    st.markdown('Middle size companies provided more than 90% percentage of jobs !')
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig5, use_container_width=True)
    with col2:
        st.plotly_chart(fig6, use_container_width=True)


if sidebar == 'Jobs by Categrory':
    st.subheader('Jobs by Category 🏷️')
    st.markdown("Explore data jobs categorized by different domains and specializations.")
    # Pie chat for jobs categories
    fig_category_pie = px.pie(df, 
                              names='job_category', 
                              title='Distribution of Jobs by Category',
                              color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig_category_pie, use_container_width=True)

    # Treemap for job categories
    fig_category_treemap = px.treemap(df, 
                                      path=['job_category'], 
                                      title='Job Categories Treemap',
                                      color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig_category_treemap, use_container_width=True)

    # Box plot for job categories and salary
    fig_category_box = px.box(df, 
                              x='job_category', 
                              y='salary_in_usd', 
                              title='Salary Distribution Across Job Categories (Box Plot)',
                              color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig_category_box, use_container_width=True)



if sidebar =='Jobs by Country':
    st.subheader('Jobs by Country')

# Average Salary by Countries
    salary_country = df.groupby('employee_residence')['salary_in_usd'].mean().round().sort_values(ascending =False).head(15).reset_index(name='salary')
    fig7 = px.bar(salary_country, x='employee_residence', y='salary', text_auto = True, color_discrete_sequence=px.colors.qualitative.Set3)
    fig7.update_layout(
    title='Average Salary by Countries', 
    xaxis_title=None,  
    yaxis_title=None 
    )
    st.plotly_chart(fig7, use_container_width=True)

# Job Numbers by Countries
    nb_job_country = df.groupby(['employee_residence','work_year']).size().sort_values(ascending = False).head(15).reset_index(name = 'nb_jobs')

    fig8 = px.bar(nb_job_country, x='employee_residence', y='nb_jobs', color='work_year',text_auto = True)
    fig8.update_layout(
    title='Job Numbers by Countries', 
    xaxis_title=None,  
    yaxis_title=None 
    )
    st.plotly_chart(fig8, use_container_width=True)

# Average Salary by Company Location
    country_data = df.groupby('company_location').agg({'salary_in_usd': 'mean', 'job_title': 'count'}).reset_index()
    fig_country_salary = px.bar(country_data, x='company_location', y='salary_in_usd', title='Average Salary by Company Location', color= 'company_location')
    st.plotly_chart(fig_country_salary, use_container_width=True)


if sidebar =='About Dataset':
    st.markdown('This dataset is from kaggle, https://www.kaggle.com/datasets/hummaamqaasim/jobs-in-data')
    st.markdown("""
         <div id="dataset">
    <div><h3> 🇫🇷 work_year</h3><p>The year in which the data was recorded. This field indicates the temporal context of the data, important for understanding salary trends over time.</p></div>

<div><h3> 🇫🇷 job_title</h3><p>The specific title of the job role, like 'Data Scientist', 'Data Engineer', or 'Data Analyst'. This column is crucial for understanding the salary distribution across various specialized roles within the data field.</p></div>

<div><h3> 🇫🇷 job_category</h3><p>A classification of the job role into broader categories for easier analysis. This might include areas like 'Data Analysis', 'Machine Learning', 'Data Engineering', etc.</p></div>

<div><h3> 🇫🇷 salary_currency</h3><p>The currency in which the salary is paid, such as USD, EUR, etc. This is important for currency conversion and understanding the actual value of the salary in a global context.</p></div>

<div><h3> 🇫🇷 salary</h3><p>The annual gross salary of the role in the local currency. This raw salary figure is key for direct regional salary comparisons.</p></div>

<div><h3> 🇫🇷 salary_in_usd</h3><p>The annual gross salary converted to United States Dollars (USD). This uniform currency conversion aids in global salary comparisons and analyses.</p></div>

<div><h3> 🇫🇷 employee_residence</h3><p>The country of residence of the employee. This data point can be used to explore geographical salary differences and cost-of-living variations.</p></div>

<div><h3> 🇫🇷 experience_level</h3><p>Classifies the professional experience level of the employee. Common categories might include 'Entry-level', 'Mid-level', 'Senior', and 'Executive', providing insight into how experience influences salary in data-related roles.</p></div>

<div><h3> 🇫🇷 employment_type</h3><p>Specifies the type of employment, such as 'Full-time', 'Part-time', 'Contract', etc. This helps in analyzing how different employment arrangements affect salary structures.</p></div>

<div><h3> 🇫🇷 work_setting</h3><p>The work setting or environment, like 'Remote', 'In-person', or 'Hybrid'. This column reflects the impact of work settings on salary levels in the data industry.</p></div>

<div><h3> 🇫🇷 company_location</h3><p>The country where the company is located. It helps in analyzing how the location of the company affects salary structures.</p></div>

<div><h3> 🇫🇷 company_size</h3><p>The size of the employer company, often categorized into small (S), medium (M), and large (L) sizes. This allows for analysis of how company size influences salary.     </p></div>
         </div>
         <style>
         #dataset{display:flex; flex-wrap:wrap;gap:50px;}
         #dataset>div{
         flex-basis:40%;)
         }
            #dataset h3{font-size:16px; font-family:monospace; color:#8dd3c7;  }    
                
         </style>
            """,
    unsafe_allow_html=True)