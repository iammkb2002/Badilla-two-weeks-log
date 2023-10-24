# Import the libraries
import pandas as pd
import streamlit as st
import plotly.express as px
import statsmodels.api as sm

# Set the title and sidebar of the dashboard
st.title('My 2 Week Log Dashboard')
st.sidebar.header('Dashboard Settings')

# Load the dataset
df = pd.read_csv('data.csv')

# Introduction
st.markdown("""
This dashboard shows some visualizations and analyses of my own daily activities from October 9 to October 23, 2023. 
The data set contains information about the activity, start time, end time, location, energy level after, and mood after for each activity. 
The energy and mood columns are based on a scale of 1 to 10, where 1 is the lowest and 10 is the highest.
The dashboard allows you to explore different aspects of the data, such as sleep patterns, activity frequency, time management, location preference, energy levels, mood levels, and the relationship between energy and mood.
You can use the sidebar to select which visualization or analysis you want to see.
""")

# Create a list of options for the sidebar
options = ['Select an option', 'Hours of Sleep Per Night for Last 7 Days', 'Top 5 Activities by Frequency', 'Top 5 Activities by Total Duration', 'Proportion of Time Spent at Top 5 Locations', 'Average Energy Levels Throughout the Day', 'Average Mood Levels Throughout the Day', 'Energy vs Mood']

# Create a selectbox for the sidebar
choice = st.sidebar.selectbox('Choose a visualization or analysis', options)

# Define a function to display the plot and explanation for each option
def display_plot_and_explanation(option):
    # Filter out rows where activity is not 'Sleeping'
    df_sleep = df[df['Activity'] == 'Sleeping']

    # Convert 'Start Time', 'End Time', and 'Date' to datetime format
    df_sleep['Start Time'] = pd.to_datetime(df_sleep['Start Time'])
    df_sleep['End Time'] = pd.to_datetime(df_sleep['End Time'])
    df_sleep['Date'] = pd.to_datetime(df_sleep['Date'])

    # Calculate sleep duration in hours
    df_sleep['Sleep Duration'] = (df_sleep['End Time'] - df_sleep['Start Time']).dt.seconds / 3600

    # Group by date and calculate the sum of sleep duration for each day
    sleep_duration_per_day = df_sleep.groupby('Date')['Sleep Duration'].sum()

    # Filter the data for the last 7 days
    last_7_days = sleep_duration_per_day.last('7D')

    # Create a dataframe for the plot
    plot_df = pd.DataFrame({
        'Date': last_7_days.index,
        'Hours of Sleep': last_7_days.values
    })

    if option == 'Hours of Sleep Per Night for Last 7 Days':
        # Create the plot
        fig = px.bar(plot_df, x='Date', y='Hours of Sleep', title='Hours of Sleep Per Night for Last 7 Days')

        # Display the plot in Streamlit
        st.plotly_chart(fig)

        # Generate and display the explanation
        explanation = f"The bar chart represents the hours of sleep per night for the last 7 days. The x-axis represents the date, ranging from {plot_df['Date'].min().strftime('%b %d, %Y')} to {plot_df['Date'].max().strftime('%b %d, %Y')}. The y-axis represents the hours of sleep. The highest amount of sleep was on {plot_df.loc[plot_df['Hours of Sleep'].idxmax(), 'Date'].strftime('%b %d, %Y')} with {plot_df['Hours of Sleep'].max()} hours of sleep, and the lowest amount of sleep was on {plot_df.loc[plot_df['Hours of Sleep'].idxmin(), 'Date'].strftime('%b %d, %Y')} with {plot_df['Hours of Sleep'].min()} hours of sleep. This chart helps me understand my sleep patterns over the past week. In conclusion, I had an average of 8 hours of sleep per night, but my sleep decreased towards the end of the week. I wonder if this was because I had more work or stress during that time, or if I was affected by other factors such as noise or temperature. Maybe I should try to improve my sleep hygiene and stick to a regular schedule to get more consistent and quality sleep."
        st.write(explanation)

    # Count the frequency of each activity
    activity_counts = df['Activity'].value_counts()

    # Get the top 5 activities
    top_activities = activity_counts.nlargest(5)

    # Create a dataframe for the plot
    plot_df = pd.DataFrame({
        'Activity': top_activities.index,
        'Count': top_activities.values
    })

    if option == 'Top 5 Activities by Frequency':
        # Create the plot
        fig = px.bar(plot_df, x='Activity', y='Count', title='Top 5 Activities by Frequency')

        # Display the plot in Streamlit
        st.plotly_chart(fig)

        # Generate and display the explanation
        explanation = f"The bar chart represents the top 5 activities based on their frequency. The activities are: {', '.join(plot_df['Activity'])}. The x-axis represents the activities and the y-axis represents their counts. The activity with the highest count is '{plot_df.iloc[0]['Activity']}' with a count of {plot_df.iloc[0]['Count']}, and the activity with the lowest count among the selected top 5 is '{plot_df.iloc[-1]['Activity']}' with a count of {plot_df.iloc[-1]['Count']}. This chart helps us understand which activities are most frequently performed. However, this does not necessarily show the amount of time spent on each activity. For example, an activity that is performed for a short duration of time may have a high count, while an activity that is performed for a long duration of time may have a low count. To conclude, I found out that the activity I did the most was 'Class' with a count of 30, followed by 'Sleeping', 'Breakfast', 'Watch Netflix', and 'Do assignments'. I am a student, so, it is normal for 'Class' to be the most frequent activity. I also think that I have a pretty good work life balance seeing that I spend about as much time for leisure as with doing assignments."
        st.write(explanation)

    # Convert 'Start Time' and 'End Time' to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Calculate activity duration in hours
    df['Activity Duration'] = (df['End Time'] - df['Start Time']).dt.seconds / 3600

    # Convert 'Activity' to lowercase and remove extra spaces
    df['Activity'] = df['Activity'].str.lower().str.strip()

    # Group by activity and calculate the total duration for each activity
    activity_duration = df.groupby('Activity')['Activity Duration'].sum()

    # Get the top 5 activities with the longest total duration
    top_activities = activity_duration.nlargest(5)

    # Create a dataframe for the plot
    plot_df = pd.DataFrame({
        'Activity': top_activities.index,
        'Total Duration': top_activities.values
    })

    if option == 'Top 5 Activities by Total Duration':
        # Create the plot
        fig = px.bar(plot_df, x='Activity', y='Total Duration', title='Top 5 Activities by Total Duration')

        # Display the plot in Streamlit
        st.plotly_chart(fig)

        # Generate and display the explanation
        explanation = f"The bar chart represents the total duration of the top 5 activities. The x-axis represents different activities: {', '.join(plot_df['Activity'])}. The y-axis represents the total duration of each activity. The activity with the longest total duration is '{plot_df.iloc[0]['Activity']}' with a total duration of {plot_df.iloc[0]['Total Duration']} hours, and the activity with the shortest total duration among the top 5 is '{plot_df.iloc[-1]['Activity']}' with a total duration of {plot_df.iloc[-1]['Total Duration'].round(2)} hours. This chart helps us understand which activities take up most of my time."
        st.write(explanation)

    # Count the frequency of each location
    location_counts = df['Location'].value_counts()

    # Get the top 5 locations
    top_locations = location_counts.nlargest(5)

    # Create a dataframe for the plot
    plot_df = pd.DataFrame({
        'Location': top_locations.index,
        'Count': top_locations.values
    })

    if option == 'Proportion of Time Spent at Top 5 Locations':
        # Create the plot
        fig = px.pie(plot_df, values='Count', names='Location', title='Proportion of Time Spent at Top 5 Locations')

        # Display the plot in Streamlit
        st.plotly_chart(fig)

        # Generate and display the explanation
        explanation = f"The pie chart represents the proportion of time spent at the top 5 locations. The locations are: {', '.join(plot_df['Location'])}. Each slice of the pie represents a different location, and the size of the slice represents the proportion of time spent at that location. The largest slice represents the location '{plot_df.iloc[0]['Location']}' where most time is spent, and the smallest slice represents the location '{plot_df.iloc[-1]['Location']}' where least time is spent among the top 5 locations. This chart helps us understand where most time is spent."
        st.write(explanation)

    # Create a new column for the hour of the day
    df['Hour of Day'] = df['Start Time'].dt.hour

    # Group by 'Hour of Day' and calculate the mean energy level
    energy_levels = df.groupby('Hour of Day')['Energy Level After'].mean()

    # Create a dataframe for the plot
    plot_df = pd.DataFrame({
        'Hour of Day': energy_levels.index,
        'Average Energy Level': energy_levels.values
    })

    if option == 'Average Energy Levels Throughout the Day':
        # Create the plot
        fig = px.line(plot_df, x='Hour of Day', y='Average Energy Level', title='Average Energy Levels Throughout the Day')

        # Display the plot in Streamlit
        st.plotly_chart(fig)

        # Generate and display the explanation
        explanation = f"The line graph represents the average energy levels throughout the day. The x-axis represents the hour of the day, ranging from 0 to 24. The y-axis represents the average energy level, ranging from approximately 5 to 8.5. The line graph shows a fluctuation in energy levels throughout the day. There is a peak in energy levels at around 8 am and midnight, which could be attributed to activities such as having breakfast, or recharging via sleeping. There are low points at around 3 pm and 6 pm, which could be due to factors like post-lunch slump or fatigue from the day's activities. This visualization can help in understanding how energy levels vary throughout the day and can provide insights into optimizing daily routines for better energy management."
        st.write(explanation)
        
    # Group by 'Hour of Day' and calculate the mean mood level
    mood_levels = df.groupby('Hour of Day')['Mood After'].mean()

    # Create a dataframe for the plot
    plot_df = pd.DataFrame({
        'Hour of Day': mood_levels.index,
        'Average Mood Level': mood_levels.values
    })

    if option == 'Average Mood Levels Throughout the Day':
        # Create the plot
        fig = px.line(plot_df, x='Hour of Day', y='Average Mood Level', title='Average Mood Levels Throughout the Day')

        # Display the plot in Streamlit
        st.plotly_chart(fig)

        # Generate and display the explanation
        explanation = f"The line graph represents the average mood levels throughout the day. The x-axis represents the hour of the day. The y-axis represents the average mood level, ranging from approximately 6 to 8. The line graph shows a fluctuation in mood levels throughout the day. There is a peak in mood levels at around 10 am, which could be attributed to activities such as having breakfast or starting the day's work or classes. There is a low point at around 8 pm, which could be due to factors like fatigue from the day's activities. This visualization can help in understanding how mood levels vary throughout the day and can provide insights into optimizing daily routines for better mood management."
        st.write(explanation)

    if option == 'Energy vs Mood':
        # Fit the regression model
        X = df['Energy Level After']
        y = df['Mood After']
        X = sm.add_constant(X)  # adding a constant

        model = sm.OLS(y, X).fit()
        predictions = model.predict(X)

        # Create the scatter plot with trendline
        fig = px.scatter(df, x='Energy Level After', y='Mood After', trendline="ols", title='Energy vs Mood')
        st.plotly_chart(fig)

        # Display the regression equation
        st.write(f"Regression equation: Mood After = {model.params[0]} + {model.params[1]} * (Energy Level After)")

        # Generate and display the explanation
        explanation = f"The scatter plot shows how my mood changes with my energy level after each activity. The higher my energy level, the higher my mood. The trendline is a line that best fits the data points and shows the general direction of the relationship. The regression equation is a formula that describes the relationship mathematically. It says that my mood is equal to 2.55 plus 0.68 times my energy level. This means that for every one point increase in my energy level, my mood increases by 0.68 points on average, regardless of other factors. The summary statistics give more details about how well the formula fits the data and how confident I am about the results. The R-squared value is 0.606, which means that 60.6% of the variation in mood can be explained by energy level. The p-values are very small, which means that the results are very unlikely to happen by chance."
        st.write(explanation)

        # Display the summary statistics
        st.write(model.summary())

display_plot_and_explanation(choice)
