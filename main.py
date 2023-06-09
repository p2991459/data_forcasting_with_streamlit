# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import streamlit as st
import io
import pandas as pd
from prophet import Prophet






## python function


def forecast_values(df,periods,col_name):
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=periods,freq='M')
    forecast = model.predict(future)
    forecast = forecast[['ds','yhat']]
    predicted = str(col_name)
    forecast.rename(columns={'yhat': predicted}, inplace=True)
    return forecast



OPTIONS = ['Acura RDX', 'Acura RL', 'Audi Q3', 'BMW 5-Series', 'Buick Envision']
periods = 24


def create_df():
    final_df = pd.DataFrame()
    df = pd.read_csv("temp.csv")
    for index, option in enumerate(OPTIONS):
        temp_df = pd.DataFrame(columns=['ds', 'y'])
        temp_df['ds'] = df['date']
        temp_df['y'] = df[option]
        if index == 0:
            forecast = forecast_values(temp_df,periods,option)
            final_df = pd.concat([final_df,forecast])
        else:
            forecast = forecast_values(temp_df,periods,option)
            column_name = forecast.columns[-1]
            final_df[column_name] = forecast[column_name]
    return final_df

def hit_forecast_button():
    final_df = create_df()
    df_copy = final_df.copy()
    final_df.set_index('ds', inplace=True)
    final_df.plot(kind='line')
    st.line_chart(final_df)
    return df_copy

st.set_page_config('Homepage', page_icon="🏡")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

with st.sidebar:
    st.markdown("# Hello 👋")
    st.markdown("## Welcome to this app on visualizing and forecasting . Of course, real-life data is used. Have fun 🎉!")

st.title('Estimation')
st.subheader('From Q3 1991 to Q1 2023')
st.markdown("Source table can be found [here](https://www150.statcan.gc.ca/t1/tbl1/en/cv.action?pid=1710000901)")

file = st.file_uploader("Insert only normal log files")
submitted = False

if file:
    n = 0
    nfirstlines = []
    with io.BytesIO(file.getvalue()) as f, open("temp.csv", "w",encoding="utf-8") as out:
        for x in range(n):
            nfirstlines.append(next(f))
        for line in f:
            out.write(line.decode())  # Decode bytes to string
    submitted = True

if submitted:
    st.write("File submitted successfully!")

st.subheader("Loaded CSV data")
df = pd.read_csv("temp.csv", index_col=0)
st.dataframe(df)

# column_name buttons in side bar

OPTIONS = st.sidebar.multiselect(
    'Choose columns..',
    df.columns.tolist())


st.sidebar.subheader("Time Frame")
periods = st.sidebar.slider('No. of Months of data-most recent to oldest', 0, 260, 60)
st.write(periods)


if st.button('Forecast'):
    # Globalize the DataFrame
    global final_df_to_download
    final_df = hit_forecast_button()
    final_df_to_download = final_df.copy()


# df_download = hit_forecast_button()
def convert_df(final_df_to_download):
    return final_df_to_download.to_csv(index=False).encode('utf-8')

csv = convert_df(final_df_to_download)

st.download_button(
   "Press to Download",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)