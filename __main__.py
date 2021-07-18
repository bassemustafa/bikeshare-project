# Importing modules:
import numpy as np
import pandas as pd
import time

# Define dictionaries 
bike_files = {
    'CH': 'chicago.csv',
    'NYC': 'new_york_city.csv',
    'WA': 'washington.csv'
}
months_dic = {
    'jan': 1,
    'feb': 2,
    'mar': 3,
    'apr': 4,
    'may': 5,
    'jun': 6,
    'jul': 7,
    'aug': 8,
    'sep': 9,
    'oct': 10,
    'nov': 11,
    'dec': 12
}
days_dic = {
    'mon': 0,
    'tue': 1,
    'wed': 2,
    'thu': 3,
    'fri': 4,
    'sat': 5,
    'sun': 6
}

def usr_filters_param():
    '''
    Getting a state, month, and/or day from user to filter the data as he/she needs

    Returns:
        usr_st : the state to load its data file for the user -> (str)
        usr_mth : the month which user need to filter the data with it [all if none or day] -> (str)
        usr_day : the day which user need to filter the data with it [all if none or month] -> (str)
    '''
    # Define the variables for the function
    usr_st = ''
    usr_filter = ''
    usr_mth = ''
    usr_day = ''

    try:
        # Ask user for a state to use its data, and check if user enters a valid state from our dectionary, if not ask him/her again
        while usr_st not in bike_files.keys():
            usr_st = input('\nFirst, Choose a state to analyze its data.\n'
            'Provide an US state from this list [Chicago - New York City - Washington] as {}:\n'
            .format(list(bike_files.keys())))\
            .upper()
        
        # Ask user how he/she wants to filter the data, and check if user enters a valid filter, if not ask him/her again
        while usr_filter not in ['month', 'day', 'both', 'none']:
            usr_filter = input("\nSecond, Choose a date filter type from list ['Month', 'Day', 'Both', 'None']:\n")\
            .lower()

        # Ask user for the month to filter with it, and check if user enters a valid month from our dectionary, if not ask him/her again
        while (usr_filter in ['both', 'month']) and (usr_mth not in months_dic.keys()):
            usr_mth = input('\nNow, Choose a month to get its data.\n'
            'Provide a 3 letters abbr for a month (e.g. Jan for January) or just type All:\n')\
            .lower()
            # Set the value of the day to 'all' to make sure we filter with all days if user choose only month filter
            usr_day = 'all'

        # Ask user for the day to filter with it, and check if user enters a valid day from our dectionary, if not ask him/her again
        while (usr_filter in ['both', 'day']) and (usr_day not in days_dic.keys()):
            usr_day = input('\nNow, Choose a week day to focus on it.\n'
            'Provide a 3 letters abbr for a day (e.g. Mon for Monday) or just type All:\n')\
            .lower()
            # Set the value of the month to 'all' if it's not specified before to make sure wefilter with all months if user choose only day filter
            if not usr_mth:
                usr_mth = 'all'
        
        # Set the month and day value to all if user doesn't want a filter
        if usr_filter == 'none':
            usr_mth = 'all'
            usr_day = 'all'

        print('\nOkay get ready for some analysis.\n')
        print('-'*100, '\n')

        
        return usr_st, usr_mth, usr_day

    except KeyboardInterrupt:
        print('\nit seems that you exit the program or something, We are sad to see you go please come back and try again\n')

    except:
        print('\nUnfortunatelly, Something goes wrong so please try again with a correct paramater\n')


def data_filter(state, month , day):
    '''
    Load the csv file contains the data and filter it with user filters and fill the missing values to make the dataframe ready for the analysis

    Args:
        state: the US State that the user wants to see its data -> (str)
        month: the month filter that the user wants -> (str)
        day: the day filter that user wants -> (str)
    Return:
        df: the data of the US State after applying the filter and filling missing values -> (pd.DataFrame)
    '''
    try:
        # Load the data file and convert the time columns type to datetime instead of object
        df = pd.read_csv(bike_files[state], index_col=0)
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['End Time'] = pd.to_datetime(df['End Time'])
        
        # Filter the data of with month filter if user specify it
        if month != 'all':
            df = df[df['Start Time'].dt.month == months_dic[month]]

        # Filter the data of the day filter if user specify it
        if day != 'all':
            df = df[df['Start Time'].dt.weekday == days_dic[day]]
        
        # If the data is empty after applying the filters return empty dataframe and exit the function
        if df.empty:
            print('Oh! There are no data for your parameters')
            return pd.DataFrame()

        # Check the existance of Gender column in the data and fill the missing values with Female
        if 'Gender' in df.columns.values:
            df['Gender'].fillna('Female', inplace = True)
        
        # Check the existance of Birth Year column in the data and fill the missing values with the average Birth Year in the data
        if 'Birth Year' in df.columns.values:
            avg_year = int(df['Birth Year'].mean())
            df['Birth Year'].fillna(avg_year, inplace = True)
            df['Birth Year'] = df['Birth Year'].astype('int64')
        
        return df

    except:
        print('\nit seems that something wrong while filtering the data\n')


def time_anlysis(df):
    '''
    Create the analysis related to the time and view [Most Common Month - Most Common day - Most Common Hour] for the bike trips

    Args:
        df : the filtered dataset -> (pd.DataFrame)
    '''
    print('\nAnalyzing some data about Time, Here we are:\n')
    # Save the start time of the analysis
    stime = time.time()

    # The first most common month in the data
    mcm = df['Start Time'].dt.month_name().mode()[0]

    # The first most common day in the data
    mcd = df['Start Time'].dt.day_name().mode()[0]

    # The first most common hour in the data
    mch = df['Start Time'].dt.hour.mode()[0]

    # The count of most common month in the data
    cmcm = df['Start Time'].dt.month_name().value_counts()[mcm]

    # The count of most common day in the data
    cmcd = df['Start Time'].dt.day_name().value_counts()[mcd]

    # The count of most common hour in the data
    cmch = df['Start Time'].dt.hour.value_counts()[mch]
    
    # Calculate the analysis time
    atime = time.time() - stime

    # Printing the analysis data
    print('\nThe most common Month for trips is ({}) and it occures ({}) times.\n'.format(mcm, cmcm))
    print('\nThe most common Day for trips is ({}) and it occures ({}) times.\n'.format(mcd, cmcd))
    print('\nThe most common Hour for trips is ({}) and it occures ({}) times.\n'.format(mch, cmch))
    print('\nThe analysis and extracting the data takes {:.3f} seconds.\n'.format(atime,))
    print('-'*100)


def station_anlysis(df):
    '''
    Create the analysis related to the stations and view [Most Common Start Station - Most Common End Station - 
    Most Common Combination for Start and End Station] for the bike trips

    Args:
        df : the filtered dataset -> (pd.DataFrame)
    '''
    print('\nNow analyzing some data about Stations, Here we are:\n')

    # Save the start time of the analysis
    stime = time.time()

    # The first most common start station in the data
    mcss = df['Start Station'].mode()[0]

    # The first most common end station in the data
    mces = df['End Station'].mode()[0]

    # The most common combination of start and end stations
    mcc = df.groupby(['Start Station', 'End Station']).size().idxmax()

    # The count of the most common start station in the data
    cmcss = df['Start Station'].value_counts()[mcss]

    # The count of the most common end station in the data
    cmces = df['End Station'].value_counts()[mces]

    # The count of the most common combination of start and end stations
    cmcc = df.groupby(['Start Station', 'End Station']).size().max()
    
    # Calculate the analysis time
    atime = time.time() - stime

    # Printing the analysis data
    print('\nThe most common Start Station for trips is ({}) and it occures ({}) times.\n'.format(mcss, cmcss))
    print('\nThe most common End Station for trips is ({}) and it occures ({}) times.\n'.format(mces, cmces))
    print('\nThe most common combination of Start and End Stations is {} and it occures ({}) times.\n'.format(mcc, cmcc))
    print('\nThe analysis and extracting the data takes {:.3f} seconds.\n'.format(atime,))
    print('-'*100)


def trip_anlysis(df):
    '''
    Create the analysis related to the trips duration and view [Total Trips Duration - Average Trips Duration] for the bike trips

    Args:
        df : the filtered dataset -> (pd.DataFrame)
    '''
    print('\nNow analyzing some data about Trips, Here we are:\n')

    # Save the start time of the analysis
    stime = time.time()

    # Calculate the sum of Trip Duration columns [Total Trips Duration]
    ttt = df['Trip Duration'].sum()

    # Calculate the average of Trip Duration columns [Average Trips Duration]
    att = df['Trip Duration'].mean()

    # Calculate the analysis time
    atime = time.time() - stime

    # Printing the analysis data in decimal precise of 3 numbers after the point and with a suitable unit
    print('\nThe Total Trips Duration for trips is ({:.3f}) hours.\n'.format(ttt/3600))
    print('\nThe Average Trips Duration for trips is ({:.3f}) minutes.\n'.format(att/60))
    print('\nThe analysis and extracting the data takes {:.3f} seconds.\n'.format(atime))
    print('-'*100)


def user_anlysis(df):
    '''
    Create the analysis related to the usereand view [Numbers of Each User Type - If Avilable
    [Number of Each Gender - Earliest Birth Year - Recent Birth Year - Most Common Birth Year] for the bike trips

    Args:
        df : the filtered dataset -> (pd.DataFrame)
    '''
    print('\nNow analyzing some data about Users, Here we are:\n')

    # Save the start time of the analysis
    stime = time.time()

    # Getting number of each user type and print it
    cut = df['User Type'].value_counts()
    print('\nThe analysis of Users Type Numbers are:\n', cut.to_string())
    
    # Check if the data has Gender column, if available get number of each gender and print it
    if 'Gender' in df.columns.values:
        cg = df['Gender'].value_counts()
        print('\nThe analysis of the Gender Numbers are:\n', cg.to_string())
        
    # Check if the data has Birth Year column, if available get earlist, recent, and most common birth yeaer and print it
    if 'Birth Year' in df.columns.values:
        ey = df['Birth Year'].min()
        mry = df['Birth Year'].max()
        mcy = df['Birth Year'].mode()[0]
        cmcy = df['Birth Year'].value_counts()[mcy]
        print('\nThe Earliest Birth Year for users in the data is ({}).\n'.format(ey))
        print('\nThe Most Recent Birth Year for users in the data is ({}).\n'.format(mry))
        print('\nThe Most Common Birth Year in the data is ({}) and it occures ({}) times.\n'.format(mcy, cmcy))

    # Calculate the analysis time
    atime = time.time() - stime

    print('\nThe analysis and extracting the data takes {:.3f} seconds.\n'.format(atime))
    print('-'*100)
    

def show_sample(df):
    '''
    Show sample of the bike data to the user five by five each time he/she wants to

    Args:
        df : the filtered dataset -> (pd.DataFrame)
    '''
    # Define a variable for the user answer
    answer = ''
    
    # Set the index to 0 to start from the beginning of the dataset
    i = 0

    # Keep asking user if he/she wants to see a data sample untill he/she provide yes or no
    while answer not in ['yes', 'no']:
        answer = input('\nDo you want to see a random sample of the data?   (Yes/No):\n')\
                .lower()
        
        # If the user answered yes and want to see data sample
        if answer == 'yes':
            # If the index is still in the range of the length of the dataset print a sample of five rows, if not Break
            if i in range(len(df.index)):
                print(df.iloc[i:i+5])
            else:
                break

            # Increase the index by 5 to get ready for the next 5 rows
            i += 5

            # Re-assign the answer of the user to be empty so the script asks him/her again.
            answer = ''

        # If the user answered no break the loop.
        if answer == 'no':
            print('\nThanks for your time it was pleasure for me, Let\'s give it another try if you want.\n')
        

# The main excutable block of the script
if __name__ == '__main__':

    print('Hello to the bike share system data center.\n')
    try:
        answer = ''

        while answer not in ['yes', 'no']:
            answer = input('Do yo want to analyze some data?   (Yes/No):\n')\
            .lower()
            if answer == 'yes':
                # Set the user filters and the US State after getting them from the user
                state, month, day = usr_filters_param()

                # Pass the US State and filters to get the filtered dataset
                df = data_filter(state, month, day)

                # If filtered dataset is not empty do the analysis
                if not df.empty:
                    time_anlysis(df)
                    station_anlysis(df)
                    trip_anlysis(df)
                    user_anlysis(df)
                    show_sample(df)
                
                answer = ''

            if answer =='no':
                print('\nThanks for anlyzing with us, Hope to see you soon.')

    except:
        print('\noh! an error occured, We are sorry and hope you to try again\n')
