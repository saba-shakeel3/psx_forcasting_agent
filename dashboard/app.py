# psx_agent_ai/dashboard/app.py
import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("../data/merged_data.csv")

st.title("\U0001F4C8 PSX Stock & News Sentiment Dashboard")
st.write("Latest merged data:")

st.dataframe(df.tail(10))

fig = px.line(df, x='timestamp', y='Close', title='Stock Price over Time')
st.plotly_chart(fig)

sent_fig = px.histogram(df, x='sentiment', title='News Sentiment Distribution')
st.plotly_chart(sent_fig)