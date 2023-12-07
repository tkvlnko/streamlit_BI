import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


df = pd.read_csv("./data/terrorism.csv", encoding='latin-1', low_memory=False)

if __name__ == "__main__":
    st.set_page_config(
        page_title="BI GTD Analytics",
        initial_sidebar_state="collapsed")

    with st.sidebar:
        st.write("Some information about the project")
        st.link_button(
            "Dataset (source)",
            "https://www.kaggle.com/datasets/START-UMD/gtd",
        )

    st.title("Global Terrorism BI") 
    x = np.arange(1970, 2017)
    y = df['iyear'].value_counts().sort_index(ascending=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="Cases", value=f"{df.shape[0]}") 

    with col2:
        st.metric(label="Years", value=f"{df['iyear'].unique().shape[0]}") 

    with col3:
        st.metric(label="Countries", value=f"{df['country_txt'].unique().shape[0]}") 

    st.write("Dataframe:")
    st.dataframe(df.dropna(axis=1).head(4))



    st.subheader("Total amount of attacks per year (worldwide)")
    fig = px.line(x=x, y=y)
    st.plotly_chart(fig, use_container_width=True)


# operations per country
    countries = df['country_txt'].unique() 
    st.subheader('Total amount of attacks (per country)')
    selected_countries = st.multiselect('Select countries', countries)

    if selected_countries:
        traces = []
        for country in selected_countries:
            trace = go.Scatter(x=df[df['country_txt'] == country]['iyear'].value_counts().sort_index(ascending=True).index,
                                y=df[df['country_txt'] == country]['iyear'].value_counts().sort_index(ascending=True).values,
                                mode='lines',
                                name=country,
                                visible=True)  
            traces.append(trace)
        fig = go.Figure(traces)

        fig.update_layout(title='Incidents Over Years for Selected Countries',
                            xaxis_title='Year',
                            yaxis_title='Number of Incidents')

        st.plotly_chart(fig)
    else:
        st.write('Please select countries to display the line graph.')


#map
    st.subheader('Map: Attacks Around the World')
    df['iyear'] = df['iyear'].astype(str)
    fig = px.scatter_geo(df, 
                        lat='latitude', 
                        lon='longitude', 
                        hover_name='country_txt', 
                        projection='natural earth',
                        color='iyear',
                        animation_frame='iyear',
                        color_discrete_sequence=["#2a658f"],
                        opacity=0.5)
    fig.update_layout({
    'plot_bgcolor': 'rgba(17, 17, 17, 0.8)',  # Set the background color to grey with some transparency
    'geo': {
        'showland': True, 
        'landcolor': 'rgb(217, 217, 217)',  # Set the land color to a light grey
        'subunitcolor': 'rgb(255, 255, 255)',  # Set the contour color to white
        'countrycolor': 'rgb(255, 255, 255)',  # Set the country contour color to white
    }
})

    st.plotly_chart(fig)

#big sunburst 
    st.subheader('Proportions: part of the world/country/city')
    top_provstates_per_country = df.groupby('country_txt')['provstate'].value_counts().groupby(level=0).nlargest(5).reset_index(level=1, drop=True).reset_index()
    top_provstates_per_country = pd.merge(top_provstates_per_country, df[['country_txt', 'provstate', 'region_txt', 'success']], on=['country_txt', 'provstate'], how='left')
    color_palette = ["#224c6e", "#2a658f", "#3883a9", "#5aaed2", "#8ad5eb", "#b9e5f3", "#d4eff8", "#c8f4fc", "#b9f9fd", "#aafcff"]


    fig = px.sunburst(top_provstates_per_country, 
                    path=["region_txt", "country_txt", "provstate"], 
                    values="success", 
                    color='region_txt',
                    title='Tap to select a particular region',
                    color_discrete_map={
                            'Middle East & North Africa': color_palette[0],  
                            'South Asia': color_palette[1], 
                            'Sub-Saharan Africa': color_palette[2],  
                            'South America': color_palette[3],  
                            'Western Europe': color_palette[4],  
                            'Central America & Caribbean': color_palette[5],  
                            'Southeast Asia': color_palette[6],  
                            'Eastern Europe': color_palette[7],  
                            'North America': color_palette[8]
                            }
                    )
    st.plotly_chart(fig)









