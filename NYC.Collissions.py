import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

DATA = ".data/NYC.Collissions.csv"

st.title("Motor Vechicle Collisions in NYC")
st.markdown("Streamlit dashboard to analyze colllisions in NYC")

@st.cache_data(persist=True)
def load_data(nrows):
  #print("realoading...")
  data = pd.read_csv(DATA, nrows=nrows, parse_dates=[['CRASH DATE', 'CRASH TIME']])
  lowercase = lambda x: str(x).lower()
  data.rename(lowercase, axis='columns', inplace=True)

  data.dropna(subset=['latitude', 'longitude'], inplace=True)
  data.rename(columns={'crash date_crash time' : 'date/time'}, inplace=True)

  # Convert to numeric
  numeric_cols = ['number of persons injured', 'number of pedestrians injured']
  data[numeric_cols] = data[numeric_cols].apply(pd.to_numeric, errors='coerce') # 'coerce' sets invalid to NaN 
  data.dropna(subset=numeric_cols, inplace=True)

  return data

data = load_data(100_000)

st.header("Where are the most people injured?")
#injured_people = st.slider("Number of injuries", 0, 19)
injured_people = st.sidebar.slider("Number of injuries", 0, 19)

# Show on a simple map
st.map(data.query("`number of persons injured` >= @injured_people")[['latitude', 'longitude']].dropna(how="any"))

st.header("Collissions during a given hour")
hour = st.sidebar.selectbox("Hour of the day", range(0, 24), 1)

print(data.columns)
data = data[data['date/time'].dt.hour == hour]

st.markdown(f"Collisions between {hour} and {(hour + 1) % 24}")

if st.checkbox("Show Table", False):
  st.subheader("Table")
  st.write(data)

# Zoom to nyc, also 3D map
mid_lat, mid_lon = np.average(data['latitude']), np.average(data['longitude'])
st.write(pdk.Deck(
  map_style = "mapbox://styles/mapbox/light-v9",
  initial_view_state = {
    'latitude' : mid_lat,
    'longitude' : mid_lon,
    'zoom' : 11,
    'pitch' : 50,
  },
  layers=[
    pdk.Layer(
      "HexagonLayer",
      data=data[['date/time', 'latitude', 'longitude']],
      get_position=['longitude', 'latitude'],
      radius=100,
      extruded=True, pickable=True, elevaltion_scale=4, elevation_range=[0,1000]),
  ],
))


# Minutely Histogram of crashs
st.subheader(f"Breakdown by hour between {hour} and {(hour + 1) % 24}")
filtered = data[
  (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour + 1))
]
hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({'minute': range(60), 'crashes': hist})
fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400)
st.write(fig)

st.header("Top 5 dangerious streets")
select = st.selectbox("Affected", ['Pedestrians', 'Cyclists', 'Motorists'])

# Debug
#st.write(data['number of pedestrians injured'].unique())
#st.write(data.describe())
#st.write(data.dtypes)

if select == 'Pedestrians':
  st.write(data.query("`number of pedestrians injured` >= 1")
    [['on street name', 'number of pedestrians injured']]
    .sort_values(by=['number of pedestrians injured'], ascending=False).dropna(how='any')[:5])
elif select == 'Cyclists':
  st.write(data.query("`number of cyclist injured` >= 1")
    [['on street name', 'number of cyclist injured']]
    .sort_values(by=['number of cyclist injured'], ascending=False).dropna(how='any')[:5])
elif select == 'Motorists':
  st.write(data.query("`number of motorist injured` >= 1")
    [['on street name', 'number of motorist injured']]
    .sort_values(by=['number of motorist injured'], ascending=False).dropna(how='any')[:5])

