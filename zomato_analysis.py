import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the application
st.title('Zomato Data Analysis')

# File upload
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load data
    dataframe = pd.read_csv(uploaded_file)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    
    # Function to handle rate column
    def handleRate(value):
        value = str(value).split('/')
        value = value[0]
        return float(value)

    dataframe['rate'] = dataframe['rate'].apply(handleRate)

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    options = st.sidebar.multiselect(
        'Select analysis to perform:',
        ['Explore listed_in (type) column', 
         'Preferred by a larger number of individuals', 
         'Restaurant with maximum votes', 
         'Explore online_order column', 
         'Explore ratings',
         'Compare online and offline order ratings',
         'Heatmap of listed_in(type) and online_order']
    )

    # Explore listed_in (type) column
    if 'Explore listed_in (type) column' in options:
        st.subheader('Explore by Type of Restaurant')
        plt.figure(figsize=(10, 6))
        dataframe['listed_in(type)'].value_counts().plot(kind='bar')
        plt.xlabel("Type of restaurant")
        plt.ylabel("Count")
        plt.title("Number of Restaurants by Type")
        st.pyplot()

    # Preferred by a larger number of individuals
    if 'Preferred by a larger number of individuals' in options:
        st.subheader('Preferred by a Larger Number of Individuals')
        plt.figure(figsize=(10, 6))
        grouped_data = dataframe.groupby('listed_in(type)')['votes'].sum()
        grouped_data.plot(kind='line', marker='o', color='green')
        plt.xlabel("Type of restaurant")
        plt.ylabel("Votes")
        plt.title("Total Votes by Restaurant Type")
        st.pyplot()

    # Restaurant with maximum votes
    if 'Restaurant with maximum votes' in options:
        st.subheader('Restaurant with Maximum Votes')
        max_votes = dataframe['votes'].max()
        restaurant_with_max_votes = dataframe.loc[dataframe['votes'] == max_votes, 'name']
        st.write("Restaurant(s) with the maximum votes:")
        st.write(restaurant_with_max_votes)

    # Explore online_order column
    if 'Explore online_order column' in options:
        st.subheader('Explore Online Orders')
        plt.figure(figsize=(10, 6))
        dataframe['online_order'].value_counts().plot(kind='bar')
        plt.xlabel("Online Order")
        plt.ylabel("Count")
        plt.title("Number of Restaurants with Online Orders")
        st.pyplot()

    # Explore rate column
    if 'Explore ratings' in options:
        st.subheader('Explore by Ratings')
        plt.figure(figsize=(10, 6))
        plt.hist(dataframe['rate'], bins=5, edgecolor='black')
        plt.xlabel("Rating")
        plt.ylabel("Frequency")
        plt.title("Distribution of Ratings")
        st.pyplot()

    # Compare online and offline order ratings
    if 'Compare online and offline order ratings' in options:
        st.subheader('Compare Online and Offline Order Ratings')
        plt.figure(figsize=(10, 6))
        dataframe.boxplot(column='rate', by='online_order')
        plt.xlabel("Online Order")
        plt.ylabel("Rating")
        plt.title("Ratings by Online Order")
        plt.suptitle("")  # Suppress the default title
        st.pyplot()

    # Heatmap for listed_in(type) and online_order
    if 'Heatmap of listed_in(type) and online_order' in options:
        st.subheader('Heatmap of Listed In (Type) and Online Order')
        pivot_table = dataframe.pivot_table(index='listed_in(type)', columns='online_order', aggfunc='size', fill_value=0)
        plt.figure(figsize=(12, 8))
        plt.imshow(pivot_table, cmap='YlGnBu', interpolation='nearest')
        plt.colorbar(label='Count')
        plt.xticks(ticks=range(len(pivot_table.columns)), labels=pivot_table.columns)
        plt.yticks(ticks=range(len(pivot_table.index)), labels=pivot_table.index)
        plt.xlabel("Online Order")
        plt.ylabel("Listed In (Type)")
        plt.title("Heatmap of Restaurant Types and Online Orders")
        st.pyplot()

else:
    st.info('Please upload a CSV file to get started.')
