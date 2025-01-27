import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

# First some MPG Data Exploration
mpg_df=pd.read_csv("./data/raw/mpg.csv")

# Add title and header
st.title("Introduction to Streamlit")
st.header("MPG Data Exploration")

#st.dataframe(mpg_df)

# We can write stuff
url = "https://archive.ics.uci.edu/ml/datasets/auto+mpg"
st.write("Data Source:", url)
#"This work too:", url

#st.table(data=mpg_df)
if st.sidebar.checkbox("Show Dataframe"):
    st.header("MPG Dataset:")
    st.dataframe(mpg_df)

@st.cache_data # decorator
def load_data(path):
    df=pd.read_csv(path)
    return df

mpf_df_raw=load_data(path="./data/raw/mpg.csv")
mpg_df=deepcopy(mpg_df)

left_column, right_column=st.columns(2)

years=["All"]+sorted(pd.unique(mpg_df['year']))
year=left_column.selectbox("Choose a year", years, index=2)

plot_types = ["Matplotlib", "Plotly"]
plot_type = right_column.radio("Choose Plot Type", plot_types)



show_means=right_column.radio(
    label='Show class means', options=['Yes', 'No'])

if year == "All":
    reduced_df = mpg_df
else:
    reduced_df = mpg_df[mpg_df["year"] == year]

means = reduced_df.groupby('class').mean(numeric_only=True)

# matplotlib plot
m_fig, ax = plt.subplots(figsize=(10, 8))
if show_means == "Yes":
    ax.scatter(means['displ'], means['hwy'], alpha=0.7,
               color="red", label="Class Means")


ax.scatter(reduced_df['displ'], reduced_df['hwy'], alpha=0.7)
ax.set_title("Engine Size vs. Highway Fuel Mileage")
ax.set_xlabel('Displacement (Liters)')
ax.set_ylabel('MPG')
#st.pyplot(m_fig)

p_fig = px.scatter(reduced_df, x='displ', y='hwy', opacity=0.5,
                   range_x=[1, 8], range_y=[10, 50],
                   width=750, height=600,
                   labels={"displ": "Displacement (Liters)","hwy": "MPG"},
                   #title=f"Engine Size vs. Highway Fuel Mileage for {year}",
                   title="Engine Size vs. Highway Fuel Mileage for {}".format(year))
p_fig.update_layout(title_font_size=22)
#st.plotly_chart(p_fig)

if plot_type == "Matplotlib":
    st.pyplot(m_fig)
else:
    st.plotly_chart(p_fig)


# Sample Streamlit Map
st.subheader("Streamlit Map")
ds_geo = px.data.carshare()

ds_geo['lat'] = ds_geo['centroid_lat']
ds_geo['lon'] = ds_geo['centroid_lon']

st.map(ds_geo)