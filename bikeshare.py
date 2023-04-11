import time
import pandas as pd
import json
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("\033[92m" + 'Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = None
    city_list = ['chicago','new york','washington']
    while city not in city_list:
        city = input("\nPlease select a City\nChicago, New York or Washington : ").lower()

    # get user input for month (all, january, february, ... , june)
    month = None
    month_list = ['all', 'january','february','march','april','may','june']
    while month not in month_list:
        month = input("\nPlease select Month or 'All' for all months\nAll, January, February, March, April, May or June : ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = None
    day_list = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    while day not in day_list:
        day = input("\nPlease select Day or 'All' for all days\nAll, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday : ").lower()
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

    # capitalize selections
    city_cap = city.capitalize()
    month_cap = month.capitalize()
    day_cap = day.capitalize()
    print("\nYou have selected the following filters :\n""City = " + city_cap + ", Month = " + month_cap + ", Day = " + day_cap)
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new dataframe columns
    df['month'] = df['Start Time'].dt.month
    df['selected_day'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['selected_day'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    if 'Start Time' in df.columns:
        print("\033[92m" + '\nCalculating The Most Frequent Times of Travel...\n' + "\033[0m")
        start_time = time.time()

        ######### display the most common month #########

        # convert Start Time to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        
        # extract month from Start Time column to create data month 
        df['month'] = df['Start Time'].dt.month
        
        # identify and display the most common month
        common_month = df['month'].mode()[0]
        print('Most common month =',common_month)
        
        ######### display the most common day of week #########
        
        # extract day from Start Time to create day of week
        df['selected_day'] = df['Start Time'].dt.day_name()
        
        # identify and display the most common day of week
        common_day = df['selected_day'].mode()[0]
        print('Most common day of the week =',common_day)

        ######### display the most common start hour #########

        # extract hour from the Start Time to create hour 
        df['hour'] = df['Start Time'].dt.hour
        
        # identify and display the most common start hour
        common_hour = df['hour'].mode()[0]
        print('Most common start hour =',common_hour)

        print("\nThis calculation took %s seconds." % (time.time() - start_time))
        
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\033[92m" + '\nCalculating the most popular stations and trip...\n' + "\033[0m")
    start_time = time.time()

    # identify and display most commonly used start station
    if 'Start Station' in df.columns:
        print('Most common start station =',df['Start Station'].mode()[0])

    # identify and display most commonly used end station
    if 'End Station' in df.columns:
        print('Most commonly used End station =',df['End Station'].mode()[0])
       
    # identify and display most frequent combination of start station and end station trip
    if 'Start Station' in df.columns and 'End Station' in df.columns:
        df['route'] = df['Start Station'] + ' -> ' + df['End Station']
        print('Most frequent route =',df['route'].mode()[0])

    print("\nThis calculation took %s seconds." % (time.time() - start_time))

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\033[92m" + '\nCalculating Trip Duration...\n' + "\033[0m")
    start_time = time.time()

    # Trip Duration stats:
    # identify and display total travel time
    print('Total Travel Time =',df['Trip Duration'].sum(),'seconds')

    # identify and display max travel time
    print('Max Travel Time =',df['Trip Duration'].max(),'seconds')
    
    # identify and display mean travel time
    print('Mean Travel Time =',df['Trip Duration'].mean(),'seconds')
  
    print("\nThis calculation took %s seconds." % (time.time() - start_time))

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\033[92m" + '\nCalculating User Stats...\n' + "\033[0m")
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        print("\033[92m" + 'User type count \n' + "\033[0m")
        print(df['User Type'].value_counts())
        # print()

    # Display counts of gender if available
    if 'Gender' in df.columns:
        print("\033[92m" + '\nGender stat count \n ' + "\033[0m")
        df['Gender'].replace(np.nan, 'not disclosed', inplace=True)
        print(df['Gender'].value_counts(dropna=False))

    # Display earliest, most recent, and most common year of birth if available
    if 'Birth Year' in df.columns:
        print("\033[92m" + '\nAge stats\n' + "\033[0m")
        print('Earliest year of birth =',int(df['Birth Year'].min()))
        print('Most recent year of birth =',int(df['Birth Year'].max()))
        print('Most common year of birth =',int(df['Birth Year'].mode()[0]))
    
    print("\nThis calculation took %s seconds." % (time.time() - start_time))

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # raw data
        rows = 5
        raw_data = input('\nWould you like to see raw data? Enter (Yes/No) : ').lower()
        df['Start Time'] = df['Start Time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        while raw_data == 'yes':
            print("\nHere is your raw data\n")
            # print first 5 rows as dictionary
            print(json.dumps(df.head(rows).to_dict('index'), indent=1))
            raw_data = input('Would you like to see more raw data? Enter (Yes/No) : ').lower()
            rows += 5
        if raw_data.lower() == 'no':
            print('\nProgram terminated - goodbye\n')
            break
if __name__ == "__main__":
    main()