import time
import pandas as pd
import numpy as np
import calendar


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ["chicago", "new york city", "washington"]
    city = ""

    while city not in cities:
        city = input("Please choose Chicago, New York City or Washington: ").lower()
        if city.casefold() in cities:
            print("Okay, I'll show you bikeshare data for " + city)

    # TO DO: get user input for month (all, january, february, ... , june)
    months = ["all", "january", "february", "march", "april", "may", "june"]
    month = input("Choose a month or enter 'all': ")

    while month not in months:
        month = input("Please choose a month from January to June: ").lower()
        if month.casefold() in months:
            print("Okay, I'll show you data for: " + month)


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    day = input("Enter 'all' or choose a day of the week:").casefold()

    print('-'*60)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month']== month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

print()

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    month_name = calendar.month_name[popular_month]
    print('Most common month: ', month_name)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most common day: ', popular_day)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    if popular_hour < 12:
        print('Most common hour was: ', popular_hour, "AM")
    else:
        print('Most common hour was: ', (popular_hour-12), "PM")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)

print()

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start = df['Start Station'].mode()[0]
    print('The most common start station was: ', most_common_start)

    # display most commonly used end station
    most_common_end = df['End Station'].mode()[0]
    print('The most common end station was: ', most_common_end)

    # display most frequent combination of start station and end station trip
    most_common_combo = (df['Start Station'] + df['End Station']).mode()[0]
    print('The most common start and end station combo was: ', most_common_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)

print()

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    hours = 3600
    total_duration = df['Trip Duration'].sum()
    tot_duration_hrs = int(total_duration/hours)
    print('The total travel time for the given filters is: ', total_duration, ' seconds.')
    print('This is equivalent to: ', tot_duration_hrs, ' hours.')

    # display mean travel time
    average_duration = df['Trip Duration'].mean()
    avg_duration_hrs = average_duration/hours
    print('The average travel time for the given filters is: ', average_duration, ' seconds.')
    print('This is equivalent to: ', avg_duration_hrs, ' hours.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)

print()

def user_stats(df):
    """Displays statistics on bikeshare users."""
    cities = ["chicago", "new york city", "washington"]
    city = ""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    try:
        print('\nBoth men and women rented bikes:\n', df['Gender'].value_counts())
    except KeyError:
        print("Sorry, there is no gender data for this city.")

    # Display earliest, most recent, and most common year of birth
    try:
        print("The oldest user was born in", df['Birth Year'].min(), "and is", 2021 - df['Birth Year'].min(), "years old.")
        print("The youngest user was born in", df['Birth Year'].max(), "and is", 2021 - df['Birth Year'].max(), "years old.")
        print("Most users were born", df['Birth Year'].mode(), "They are", 2021 - df['Birth Year'].mode(),"years old.")
    except KeyError:
        print("Sorry, there is no birth year data for this city.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)

print()

def view_data(df):
    """Shows user data based on inputs chosen 5 rows at a time"""
    print("\nHere's the first 5 rows of raw data based on your filters: \n", df.head())
    next_five = 0
    while True:
        view_more = input('\n''If you would like to see the next 5 rows, enter yes. Otherwise enter no: \n')
        if view_more.casefold() != "yes":
            return
        next_five = next_five + 5
        print(df.iloc[next_five:next_five + 5])


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_data(df)

        restart = input('\nWould you like to choose a different city? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
