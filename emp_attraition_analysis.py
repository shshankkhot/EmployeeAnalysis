import streamlit as st
import pandas as pd
import plotly as plt
import plotly.express as px
import seaborn as sns

st.set_page_config(page_title="Employee Dashboard", page_icon=":bar_chart:", layout="wide")

#For CSV File
@st.cache
def get_data_from_excel():
    df = pd.read_csv("HR_Employee_Attrition.csv")
    return df

df = get_data_from_excel()
filtered_df = df

#st.set_page_config(layout="wide")
#st.sidebar.[element_name]

#st.title("Employee Attrition Report")
#st.line_chart(df)

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
#Department Select Filter
dept_list = ["All","Human Resources", "Sales", "Research and Development"]
select = st.sidebar.selectbox('Select the Department:', dept_list, key='1')
if select =="All":
    filtered_df = df
else:
    filtered_df = df[df['Department']==select]
#Job SatisfactionSlider
score = st.sidebar.slider('Select min Job Satisfaction ', min_value=1, max_value=5, value = 4) # Getting the input.
filtered_df = filtered_df[filtered_df['JobSatisfaction'] <= score] # Filtering the dataframe.

EducationField = st.sidebar.multiselect(
    "Select the Education Field:",
    options=df["EducationField"].unique(),
    default=df["EducationField"].unique()
)

Attrition = st.sidebar.multiselect(
    "Select the Attrition :",
    options=df["Attrition"].unique(),
    default=df["Attrition"].unique(),
)
gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

filtered_df = filtered_df.query(
    "EducationField == @EducationField & Attrition ==@Attrition & Gender == @gender"
)




# ---- MAINPAGE ----
st.title(":bar_chart: Employee Dashboard")
st.markdown("##")

# TOP KPI's
Total_EmpCnt = int(filtered_df["EmployeeCount"].sum())
#Avg_MthInc = round(filtered_df["MonthlyIncome"].mean(),1)

average_rating = round(filtered_df["PerformanceRating"].mean(), 1)

star_rating = ":star:" * int(round(average_rating, 0))
average_inc_by_transaction = round(filtered_df["MonthlyIncome"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Employee:")
    st.subheader(f"{Total_EmpCnt:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Monthly Income:")
    st.subheader(f"US $ {average_inc_by_transaction}")

st.markdown("""---""")

# Employee Count BY JobRole [BAR CHART]
Empcnt_by_Job_Role = (
    filtered_df.groupby(by=["JobRole"]).sum()[["EmployeeCount"]].sort_values(by="EmployeeCount")
)
fig_Job_Role = px.bar(
    Empcnt_by_Job_Role,
    x="EmployeeCount",
    y=Empcnt_by_Job_Role.index,
    orientation="h",
    title="<b>Aittration BY JobRole</b>",
    color_discrete_sequence=["#0083B8"] * len(Empcnt_by_Job_Role),
    template="plotly_white",
)
fig_Job_Role.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


# Average Employee Salary By Job Role [BAR CHART]
Employee_Salary = filtered_df.groupby(by=["JobRole"]).mean()[["MonthlyIncome"]].sort_values(by="MonthlyIncome",ascending=False)
fig_Employee_Salary = px.bar(
    Employee_Salary,
    x=Employee_Salary.index,
    y="MonthlyIncome",
    title="<b>Employee Salary By Job Role</b>",
    color_discrete_sequence=["#0083B8"] * len(Employee_Salary),
    template="plotly_white",
)
fig_Employee_Salary.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_Employee_Salary, use_container_width=True)
right_column.plotly_chart(fig_Job_Role, use_container_width=True)

st.header("Employee Report")
st.write(filtered_df)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)