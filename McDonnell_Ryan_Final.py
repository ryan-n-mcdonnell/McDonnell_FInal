'''
Ryan McDonnell
CS230
Uber Data Set
URL:

Discription:
This program is designed to show data from past uber trips as well as run programs for users looking to take an uber.
I wanted it to be more engaging so I made a query to allow you to enter two coordinates and find out the length in Km
between them as well as the price of an average uber based on how many people you are traveling with. The three charts
I have allow you to see the portions of ubers related to the amount of riders in each, the starting points of all the
ubers in the set over a map, and all the ubers related to fare in a bar chart. After that I have a few tables that
allow the user to querie to see the X highest and lowest priced ubers from the dataset. Overall this program has a lot
of interesting data and interesting interative features.
'''
import numpy as np
import streamlit as st
import pydeck as pdk
import pandas as pd
import geopy.distance
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt

df_uber = pd.read_csv("uber_8000_sample.csv")

#site map allows user to toggle through different functions
selected_map = st.sidebar.radio("Please select the Function You Would Like to Explore",
                                ["Home", "NYC Uber Map", "Track Your Trip", "Uber Split", "Most Bang For Your Buck"])

#introductiont to my project as well as a pie chart based on passenger count
if selected_map == 'Home':

    st.title("Ryan McDonnell's Final Python Project ")
    st.write(
        "For my project I designed four different functions for a user to gain more knowledge about Uber fares based on Historical Data. My first interesting findings are Below. ")

    one = sum(df_uber.passenger_count == 1)
    two = sum(df_uber.passenger_count == 2)
    three = sum(df_uber.passenger_count == 3)
    four = sum(df_uber.passenger_count == 4)
    five = sum(df_uber.passenger_count == 5)
    six = sum(df_uber.passenger_count == 6)

    labels = 'One', 'Two', 'Three', 'Four', 'Five', 'Six'
    sizes = np.array([one, two, three, four, five, six])

    # Code is referenced from discuss streamlit.com
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    plt.title('Portion of Ubers Broken Down by Passenger Count')

    st.pyplot(fig1)

#map of NYC with the uber icon over all the starting coordinates of the rides
elif selected_map == "NYC Uber Map":
    st.title('Greater NYC Uber Map')

    ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/7/79/Uber_App_Icon.svg"
    icon_data = {
        "url": ICON_URL,
        "width": 100,
        "height": 100,
        "anchorY": 100
    }

    df_uber["icon_data"] = None
    for i in df_uber.index:
        df_uber["icon_data"][i] = icon_data

    icon_layer = pdk.Layer(type="IconLayer",
                           data=df_uber,
                           get_icon="icon_data",
                           get_position='[pickup_longitude,pickup_latitude]',
                           get_size=4,
                           size_scale=10,
                           pickable=True)

    view_state = pdk.ViewState(
        latitude=df_uber["pickup_latitude"].mean(),
        longitude=df_uber["pickup_longitude"].mean(),
        zoom=6,
        pitch=0
    )

    tool_tip = {"html": "Number of Passengers:<br/> <b>{passenger_count}</b>",
                "style": {"backgroundColor": "blue",
                          "color": "white"}
                }

    icon_map = pdk.Deck(
        map_style='mapbox://styles/mapbox/navigation-day-v1',
        layers=[icon_layer],
        initial_view_state=view_state,
        tooltip=tool_tip)

    st.pydeck_chart(icon_map)

#used python geo distance package to get the distance between two sets of coordinates that user enters and operates on a button
elif selected_map == "Track Your Trip":
    st.title("Find out how long your upcoming trip will be")

    lat1 = st.number_input("Enter your beginning Lat: ")
    lon1 = st.number_input("Enter your beginning Lon: ")
    lat2 = st.number_input("Enter your ending Lat: ")
    lon2 = st.number_input("Enter your ending Lon: ")
    # referenced this article from stackoverflow to calculate distance between coordinates in Km https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    coords_1 = (lat1, lon2)
    coords_2 = (lat2, lon2)

    dist = geopy.distance.geodesic(coords_1, coords_2).km
    result = st.button("Click Here to See the Distance of Uber")  # streamlit website helped on implementation of button
    if result:
        st.write("The distance of your uber is: ", dist, "Kilometers")

#function that allows you to selecct from a "selectbox" how many people you are riding with and the total cost of the uber to yourself
elif selected_map == "Uber Split":

    st.title("How Much Will this uber cost you?")
    option = float(st.selectbox("How many people are you traveling with?", ("1", "2", "3", "4", "5")))
    st.write("You selected", option, "People")

    df_avg = float(df_uber["fare_amount"].mean())
    roundavg = round(df_avg, 2)
    st.write("The Average if you are riding alone is $", roundavg)
    real_avg = (df_avg / option)
    realround = round(real_avg, 2)
    st.write("However, with", option, "riders it is: $", realround)

#this section incompasees a lot of the general price inforamtion from the dataset to understant what the best deals and worst deals are when comparing to a prospective trip.
elif selected_map == "Most Bang For Your Buck":

    st.title("Cheapest and Most expensive ubers")

amount = st.slider('Select How many of the most expensive and cheapest Ubers would you like to see', 0, 100, 10) # can change to see top 10, 50, etc.

large = df_uber['fare_amount'].nlargest(n=amount)
small = df_uber['fare_amount'].nsmallest(n=amount)

large10 = df_uber['fare_amount'].nlargest(n=10)
small10 = df_uber['fare_amount'].nsmallest(n=10)
x = ['1','2','3','4','5', '6', '7', '8','9', '10']


s_2 = df_uber.loc[:, #trips over $100
      ['fare_amount', 'pickup_datetime', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude'
       ]][df_uber['fare_amount'] >= 100]

s_3 = df_uber.loc[:, #trips under $10
      ['fare_amount', 'pickup_datetime', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude'
       ]][df_uber['fare_amount'] <= 10]


# Code is referenced from discuss streamlit.com





st.write("Top", amount, "Most Expensive")
st.write(large)

fig2, ax2 = plt.subplots()
ax2.bar(x, height = large10, bottom=None,align='edge', width=0.7, color='green')
#ax2.axis('equal')
plt.xticks(x, rotation = 'horizontal')
plt.title('Price of top ten most expensive Ubers in the Data Set')
plt.ylabel("Cost of Uber")
plt.xlabel("10 Ubers")
st.pyplot(fig2)

st.write("Top", amount, "Lest Expensive")
st.write(small)

fig3, ax3 = plt.subplots()
ax3.bar(x, height = small10, bottom=None,align='edge', width=0.7, color='green')
#ax2.axis('equal')
plt.xticks(x, rotation = 'horizontal')
plt.title('Price of top ten least expensive Ubers in the Data Set')
plt.ylabel("Cost of Uber")
plt.xlabel("10 Ubers")
st.pyplot(fig3)


st.write("Rides Over $100")
st.write(s_2)
st.write("Rides under $10")
st.write(s_3)
