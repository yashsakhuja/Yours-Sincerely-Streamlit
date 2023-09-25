# Installing Streamlit in your system
# pip install streamlit

# Importing Packages
import streamlit as st

import pandas as pd

import altair as alt
from matplotlib import pyplot as plt

# st.set_page_config(layout='wide')

# Getting my logo
st.image('./Header.png')

st.divider()
st.subheader('1. Streamlit Writing')

st.echo()
with st.echo():
    # Printing first statement in streamlit
    st.title("Hello World")

    st.header("Hello World- Part 2!!")
    st.subheader("Who even wrote the first Hello World??")

    st.markdown("The first **Hello, World!!** program is often attributed to "
                ":red[Brian Kernighan], who wrote it in the C programming "
                "language as part of the book -*The C Programming Language*"
                "- (also known as the K&R C) in 1978. ")

    st.markdown(''':rainbow[Pride]  :rose:''')

    st.write('print(Hello World!!)')

    st.markdown(r'$E=mc^2$')
    # st.latex("E = mc^2")

# Playing with Data
st.divider()
st.subheader('2. Streamlit Data')

st.echo()
with st.echo():
    # Reading my data on Saudi Transfer Window
    data = pd.read_csv("./data/Saudi Transfer Window.csv")

    # st.table(data)  #Creates and displays a very raw table with no scrolls
    # like shown here

    st.dataframe(data)

    # st.json helps you show data in json form
    # What business did Chelsea do with Saudi Clubs?
    st.json(data[(data['From Club'] == "Chelsea") & (data["Status"] == "Accepted Deal")].to_dict(orient='records'))

    # KPI (BANs)- Saudi pull for players
    new_wages = (data['Wages Offered'].sum()) / 1000000
    old_wages = (data['Last Club Wages'].sum()) / 1000000
    diff = ((new_wages - old_wages) / old_wages)
    st.metric(label="Wage", value=f'€ {new_wages:.0f} M', delta=f'{diff:.0%}')

    # Edit your dataframes on streamlit
    st.data_editor(data)

# Weaving Interactivity with Widgets
st.divider()
st.subheader('3. Streamlit Graphs & Plots')

df1 = pd.DataFrame(data)
# Remove 'years' suffix and convert to integer
df1['Age'] = df1['Age'].str.replace(' years', '').astype(int)

# Filter players with Status as 'Accepted Deal'
filtered_df = df1[df1['Status'] == 'Accepted Deal']

st.subheader('3.1- Plotting with Altair')
st.echo()
with st.echo():
    # Define custom color
    streamlit_color = "#ff4a48"  # Streamlit natural color

    # Create a histogram using Altair with custom bar colors and bins
    hist_chart = alt.Chart(filtered_df).mark_bar(color=streamlit_color).encode(
        alt.X('Age:O', bin=alt.Bin(step=3), title='Age Group'),
        y='count()',
    ).properties(
        width=700,
        height=500,
        title='Player Age Distribution'
    )

    st.altair_chart(hist_chart)

st.subheader('3.2- Plotting with Matplotlib')
st.echo()
with st.echo():
    # Calculate the counts of players for each club country
    club_country_counts = filtered_df.groupby("Club_Country")["Player"].count().reset_index()
    club_country_counts = club_country_counts.sort_values('Player').reset_index()

    # Create the column chart using Matplotlib
    plt.figure(figsize=(8, 6))
    plt.barh(club_country_counts["Club_Country"], club_country_counts["Player"])
    plt.ylabel("League")
    plt.xlabel("Number of Players")

    # Display the chart in the Streamlit app
    st.pyplot(plt)

st.divider()
st.subheader('3.3- Plotting with Streamlits Own')
st.echo()
with st.echo():
    # Reading my data on Saudi Transfer Window
    sales_data = pd.read_csv("./data/Sales_SampleSuperstore_Data.csv")
    st.dataframe(sales_data)

    sales_data['Order Date'] = pd.to_datetime(sales_data['Order Date'], format="%d/%m/%Y")
    sales_data['Year'] = sales_data['Order Date'].dt.year
    sales_data['Month'] = sales_data['Order Date'].dt.month

    # Group data by Year and Month, calculate total sales, and reset the index
    monthly_sales = sales_data.groupby(['Year', 'Month'])['Sales'].sum().reset_index()
    # Pivot the DataFrame to have years as columns
    pivot_sales = monthly_sales.pivot(index='Month', columns='Year', values='Sales')

    # Create a Streamlit line chart for multiple years
    st.line_chart(pivot_sales)

st.divider()
st.subheader('3.4- Plotting the Maps')

st.echo()
with st.echo():

    travel_data = pd.read_csv("./data/PortsmouthPlaces.csv")
    st.dataframe(travel_data)

    # There is more room to play with packages like folium, mapbox and many others.
    st.map(data=travel_data)


st.divider()
st.subheader('3.5- Plotting with Plotly Express')

st.echo()
with st.echo():
    
    import plotly.express as px
    # Scatter plot using Plotly Express
    fig = px.scatter(
        sales_data, x='Sales', y='Profit', color='Segment',
        title='Sales vs. Profit Scatter Chart',
        labels={'Sales': 'Sales', 'Profit': 'Profit'},
        hover_data={'Segment': True}
    )

    # Display the chart in the Streamlit app
    st.plotly_chart(fig)

st.divider()
st.subheader('4. Streamlit Interactivity')


st.echo()
with st.echo():
    # Create an empty list to store player data as dictionaries
    player_data_list = []

    # Streamlit UI
    st.subheader('Fill player details below')
    pl_name = st.text_input('Enter Player Name', "")
    pl_num = st.text_input('Enter Player Jersey Number', "")
    position = st.selectbox("Select Position", ["ATT", "MID", "DEF", "GK"])
    position_detail = st.multiselect("Select Position Detail",
                                     ["GK", "CB", "LCB", "RCB", "LB", "LWB", "RB", "RWB", "CDM", "CM", "LM", "RM", "LW",
                                      "RW", "ST"])
    age = st.number_input("Age", 15, 50, step=1)
    dob = st.date_input("Enter DoB", None)
    previous_wage = st.slider('Previous Club Wage (In Million €)', 0, 1000, 0)
    tl = st.toggle("Transfer Listed")
    transfer_value = st.slider('Enter Transfer Market Value (In Million €)', 0, 1000, 0, disabled=not tl)
    status = st.radio("Status", ["Accepted Deal", "Ongoing Talks", "Rejected Offer"])
    # Generate Player Card button
    gen_card_but = st.button("Generate Player Data")

st.echo()
with st.echo():
    # Function to update the player data list
    def update_data():
        new_player = {
            "Player Name": pl_name,
            "Jersey Number": pl_num,
            "Position": position,
            "Position Detail": ', '.join(position_detail),
            "Age": age,
            "DoB": dob,
            "Previous Club Wage (Million €)": previous_wage,
            "Transfer Listed": tl,
            "Transfer Market Value (Million €)": transfer_value,
            "Status": status
        }
        player_data_list.append(new_player)


st.echo()
with st.echo():

    if gen_card_but:
        update_data()
        st.subheader("Player Data")
        st.data_editor(player_data_list,num_rows="dynamic")


        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')


        csv = convert_df(pd.DataFrame(player_data_list))

        st.download_button(
            label="Download Player Details",
            data=csv,
            file_name='player_info.csv',
            mime='text/csv',
        )


st.divider()
st.subheader('4.1 Streamlit Additional Interactivity')

st.echo()
with st.echo():
    pic=st.file_uploader("Enter Image File",type=['png','jpeg','jpg'])
    if pic is not None:
        st.image(pic)

st.echo()
with st.echo():
    st.camera_input("Smile Please")

st.echo()
with st.echo():
    audio_file = open("./data/Messi Audio.mp3",'rb')

    audio_bytes = audio_file.read()

    st.audio(audio_bytes, format='audio/mp3',start_time=6)

st.echo()
with st.echo():
    st.video("./data/Messi Video.mp4", format='mp4')

st.divider()
st.subheader('5 Adios Amigos')
st.write("Head to the sidebar")

st.echo()
with st.echo():
    end_button=st.sidebar.button ("FINISH")
    if end_button:
        st.sidebar.image("./data/Lit.jpg")
        st.balloons()
        st.sidebar.success("Congratulations!! You just got lit up")
