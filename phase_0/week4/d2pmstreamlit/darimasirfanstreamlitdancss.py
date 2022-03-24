import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt


st.set_option('deprecation.showPyplotGlobalUse', False) #biar gak muncul warning

DATA_URL = ('http://data.insideairbnb.com/united-states/ny/new-york-city/2021-11-02/visualisations/listings.csv')

@st.cache
def load_data():
    data = pd.read_csv(DATA_URL)
    return data

df= load_data()

# catatan: dalam streamlit h2= header, h3= subheader
st.markdown(
'''
<style>
h2   {background-color: #b7d7e8;
        color: #000000;
      font-family: "Arial";
      font-size: 40px;
      text-align: center;
      border-radius: 15px 50px;
      margin: 0px 0px 20px 0px;
      }
.button {
  padding: 15px 25px;
  font-size: 24px;
  text-align: center;
  cursor: pointer;
  outline: none;
  color: #fff !important;
  background-color: #1E90FF;
  border: none;
  border-radius: 15px;
  box-shadow: 0 9px #999;
}

.button:hover {background-color: #00BFFF}

.button:active {
  background-color: #3e8e41;
  box-shadow: 0 5px #666;
  transform: translateY(4px);
}

</style>
<h2>Intro</h2>

<a href="https://github.com/Sardiirfan27" class="button">My Github</a>

---
- **Author** &#127942; : SARDI IRFANSYAH <br>
- **MENTOR** &#128640; : Jomblo Expert <br>
- **Email** &#128187; : sirfansyah@hacktiv8.com /  sardiirfan27@gmail.com <br>
- **Submission** &#128197; : 08 Maret 2022
---

'''
,unsafe_allow_html=True)



"""
## NYC Dataset
"""

st.subheader("Dataframe")
# checkbox 
show_df= st.checkbox("Show dataframe")
st.write(show_df) #bisa dihilangkan
if show_df:
  st.write(df)

st.header("Where are the most expensive properties located?")
st.subheader("On a map")
st.markdown("The following map shows the top 1% most expensive Airbnbs priced at $800 and above.")
st.map(df.query("price>=800")[["latitude", "longitude"]].dropna(how="any"))
st.subheader("In a table")
st.markdown("Following are the top five most expensive properties.")
st.write(df.query("price>=800").sort_values("price", ascending=False).head())

st.subheader("Selecting a subset of columns")
st.write(f"Out of the {df.shape[1]} columns, you might want to view only a subset. Streamlit has a [multiselect](https://streamlit.io/docs/api.html#streamlit.multiselect) widget for this.")
defaultcols = ["name", "host_name", "neighbourhood", "room_type", "price"]
cols = st.multiselect("Columns", df.columns.tolist(), default=defaultcols)
st.dataframe(df[cols].head(10))

st.header("Average price by room type")


# # CSS to inject contained in a string
# hide_table_row_index = """
#             <style>
#             tbody th {display:none}
#             .blank {display:none}
#             </style>
#             """

# # Inject CSS with Markdown
# st.markdown(hide_table_row_index, unsafe_allow_html=True)


df_room= df.groupby(['room_type'])['price'].mean()
st.table(df_room.reset_index().round(2).sort_values("price", ascending=True)\
    .assign(avg_price=lambda x: x.pop("price").apply(lambda y: "%.2f" % y)))


# plotly barchat vertical
fig = px.bar(x=df_room, y=df_room.index,color=df_room.index,
    orientation="h",
    labels={"y": "Room Type", "x": "Average Price"},
    title="Average Price by Room Type")
st.plotly_chart(fig)


st.subheader("Average price by room type using matplotlib")
plt.figure(figsize=(12,6))
plt.bar(df_room.index, df_room)
plt.title("Average Price by Room Type")
plt.xlabel("Room Type")
plt.ylabel("Average Price")
plt.xticks(rotation=90)
st.pyplot()


# selectbox
st.subheader("Scatter plot of price vs. number of reviews")
room_type = st.selectbox("Room Type", df.room_type.unique())


fig = px.scatter(df.query("room_type==@room_type"), x="price", y="number_of_reviews",
    color="room_type", size="price",
    hover_data=["name", "host_name", "neighbourhood", "room_type", "price"])
st.plotly_chart(fig)


fig= px.histogram(df.query("room_type==@room_type"), x="number_of_reviews", nbins=20, title="Number of Reviews by Room Type")
st.plotly_chart(fig)


st.header("What is the distribution of property price?")
st.write("""Select a custom price range from the side bar to update the histogram below displayed as a Plotly chart using
[`st.plotly_chart`](https://streamlit.io/docs/api.html#streamlit.plotly_chart).""")

values = st.sidebar.slider("Price range", float(df.price.min()), float(df.price.clip(upper=1000.).max()), (50., 300.))
f = px.histogram(df.query(f"price.between{values}"), x="price", nbins=15, title="Price distribution")
f.update_xaxes(title="Price")
f.update_yaxes(title="No. of listings")
st.plotly_chart(f)


#radio button
st.subheader("Select a room type")
room_type_radio = st.radio("Room Type", df.room_type.unique())
st.write(f"The average price of {room_type_radio} is ${df.query('room_type==@room_type_radio').price.mean().round(2)}")
