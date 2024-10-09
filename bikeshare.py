import time
import pandas as pa

# Dictionary mapping city names to their respective CSV data files
DATA_CITY = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

# List of valid months for filtering data
MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june',
          'july', 'august', 'september', 'october', 'november', 'december']

# List of valid days for filtering data
DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 
        'saturday', 'sunday']

def get_filters():
    """Asks user to specify a city, month, and day to analyze."""
    print('Hi there! Let\'s dive into some US bikeshare data!')
    print('Would you like to see data for Chicago, New York City, or Washington?\n')
    
    # Get user input for city
    city = input('Enter the selected city (Chicago, New York City, or Washington?)\n').strip().lower()
    while city not in DATA_CITY:
        print('Invalid input. Please enter a valid city (Chicago, New York City, or Washington)')
        city = input('Choose a city: ').strip().lower()

    # Get user input for month
    month = input("Enter the month (all, January, ..., December): ").strip().lower()
    while month not in MONTHS:
        print('Invalid selected month. Please enter a valid month (all, January, ..., December).')
        month = input("Choose a month: ").strip().lower()

    # Get user input for day
    day = input("Enter the selected day (all, Monday, ..., Sunday): ").strip().lower()
    while day not in DAYS:
        print('Invalid day. Please enter a valid day (all, Monday, ..., Sunday).')
        day = input("Choose a day: ").strip().lower()

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """Loads data for the specified city and filters by month and day if applicable."""
    # Load the data into a DataFrame
    df = pa.read_csv(DATA_CITY[city])
    df['Start Time'] = pa.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time
    df['Month'] = df['Start Time'].dt.month_name().str.lower()
    df['Day_of_Week'] = df['Start Time'].dt.day_name().str.lower()

    # Filter by month if applicable
    if month != 'all':
        df = df[df['Month'] == month]

    # Filter by day if applicable
    if day != 'all':
        df = df[df['Day_of_Week'] == day]

    return df

def display_time_stats(df):
    """Calculates and displays statistics on the most common travel times."""
    print('\nCalculating...\n')
    start_time = time.time()

    # Display the most common month, day, and start hour
    print('\nThe Most Common Travel Time:\n')
    print('Most Common Month:', df['Month'].mode()[0])
    print('Most Common Day of Week:', df['Day_of_Week'].mode()[0])
    print('Most Common Start Hour:', df['Start Time'].dt.hour.mode()[0])

    print("\nTake about %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_station_stats(df):
    """Calculates and displays statistics on the most popular stations and trips."""
    print('\nCalculating...\n')
    start_time = time.time()

    # Display the most common start and end stations
    print('\nThe Most Popular Station and Trip:\n')
    print('Most Common Start Station:', df['Start Station'].mode()[0])
    print('Most Common End Station:', df['End Station'].mode()[0])
    
    # Create a combined trip column and display the most common trip
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    print('Most Common Trip:', df['Trip'].mode()[0])

    print("\nTake about %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_trip_duration_stats(df):
    """Calculates and displays statistics on trip duration."""
    print('\nCalculating...\n')
    start_time = time.time()

    # Display total and mean trip duration
    print('\nTrip Duration:\n')
    print('Total Trip Time:', df['Trip Duration'].sum())
    print('Mean Trip Time:', df['Trip Duration'].mean())

    print("\nTake about %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_user_stats(df):
    """Calculates and displays statistics on users."""
    print('\nCalculating...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nUser Statistics:\n')
    print('Counts of User Categories:\n', df['User Type'].value_counts())

    # Display gender statistics if available
    if 'Gender' in df.columns:
        print('Counts of Gender Categories:\n', df['Gender'].value_counts())

    # Display birth year statistics if available
    if 'Birth Year' in df.columns:
        print('The Earliest Year of Birth:', int(df['Birth Year'].min()))
        print('The Most Recent Year of Birth:', int(df['Birth Year'].max()))
        print('The Most Frequent Year of Birth:', int(df['Birth Year'].mode()[0]))

    print("\nTake about %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(data):
    """Displays raw data for user inspection."""
    start_loc = 0
    while True:
        # Ask user if they want to see raw data
        view_data = input("Would you like to see 5 rows of individual trip information? Please Enter y or n: ").strip().lower()
        if view_data != 'y':
            break
        # Display the next 5 rows of data
        print(data.iloc[start_loc:start_loc + 5])
        start_loc += 5
        if start_loc >= len(data):
            print("No additional data to show.")
            break

def main():
    """Main function to run the bike share analysis."""
    while True:
        # Get user input for city, month, and day
        city, month, day = get_filters()
        # Load the data based on user input
        data = load_data(city, month, day)

        # Display various statistics
        display_time_stats(data)
        display_station_stats(data)
        display_trip_duration_stats(data)
        display_user_stats(data)
        display_data(data)

        # Ask user if they want to restart the program
        restart = input('\nWould you like to start over? Please Enter y or n.\n')
        if restart.lower() != 'y':
            break

if __name__ == "__main__":
    main()
