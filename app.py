import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title = "Sales Dashboard",
    page_icon = ":smiling_imp:",
    layout="wide"
)

@st.cache
def extract_data():
    data = pd.read_excel(
        io = "supermarkt_sales.xlsx",
        engine = "openpyxl",
        sheet_name = "Sales",
        skiprows=3,
        usecols="B:R",
        nrows = 10000,
    )
    # adding hour to the dataframe
    data["hour"] = pd.to_datetime(data["Time"],format="%H:%M:%S").dt.hour
    return data

data = extract_data()

st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options = data["City"].unique(),
    default = data["City"].unique(),
)
customer_type = st.sidebar.multiselect(
    "Select Customer Type:",
    options = data["Customer_type"].unique(),
    default = data["Customer_type"].unique(),
)
gender = st.sidebar.multiselect(
    "Select Gender:",
    options = data["Gender"].unique(),
    default = data["Gender"].unique(),
)

df_selection = data.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)

#st.dataframe(df_selection)

# -- Main Page -- 

st.title(":smiling_imp: Sales Dashboard")
st.markdown("##")

# TOP KPI
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(),1)
star_rating = ":star:"*int(round(average_rating,0))
average_sale_by_transaction = round(df_selection["Total"].mean(),2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US ${total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating:}{star_rating}")
with right_column:
    st.subheader("Average Sales per Transaction:")
    st.subheader(f"US ${average_sale_by_transaction}")
    
st.markdown("")

sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x = "Total",
    y = sales_by_product_line.index,
    orientation = "h",
    title = "<b>Sales by Product Line</b>",
    color_discrete_sequence = ["#0083B8"]*len(sales_by_product_line),
    template = "plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis = (dict(showgrid = False)),
)

sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x = sales_by_hour.index,
    y = "Total",
    title  = "<b>Sales by Hour</b>",
    color_discrete_sequence = ["#0083B8"]*len(sales_by_product_line),
    template = "plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis = dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis = (dict(showgrid= False))
)

left_column,right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales,use_container_width = True)
right_column.plotly_chart(fig_product_sales,use_container_width = True)

hide_st_style = """
                <style type="text/css">
                # MainMenu {visibility:hidden;}
                footer {visibility:hidden;}
                header {visibility:hidden;}
                </style>

"""
st.markdown(hide_st_style,unsafe_allow_html = True)