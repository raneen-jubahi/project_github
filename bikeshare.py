import time
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt

def load_data(city, month, day):
    """Load and filter data based on the city, month, and day."""
    try:
        # محاولة تحميل البيانات من الملف
        df = pd.read_csv(f"{city.replace(' ', '_')}.csv")
    except FileNotFoundError:
        print("Error: Data file not found for the selected city.")
        return None

    # حذف الأعمدة غير الضرورية إذا كانت موجودة
    if 'Unnamed: 0' in df.columns:
        df.drop(columns=['Unnamed: 0'], inplace=True)

    # تحويل العمود Start Time إلى نوع بيانات تاريخي
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # استخراج month و day_of_week و hour من Start Time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    # تطبيق الفلترة بناءً على الشهر واليوم
    if month != 'all':
        # تحويل اسم الشهر إلى رقمه باستخدام get بدلاً من if
        month_mapping = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6
        }
        df = df[df['month'] == month_mapping.get(month, 0)]
    if day != 'all':
        df = df[df['day_of_week'] == day]

    # معالجة القيم المفقودة في الأعمدة المهمة
    required_columns = ['month', 'day_of_week', 'hour', 'Start Station', 'End Station']
    df.dropna(subset=required_columns, inplace=True)

    return df

def display_raw_data(df):
    """Displays 5 rows of raw data upon user request, with input validation."""
    print("\nDisplaying raw data...\n")
    start_index = 0
    while start_index < len(df):
        while True:
            display = input("Would you like to see 5 rows of raw data? (yes or no): ").strip().lower()
            if display in ['yes', 'no']:
                break
            print("Invalid input. Please enter 'yes' or 'no'.")

        if display == 'no':
            break

        print(f"\nShowing rows {start_index + 1} to {min(start_index + 5, len(df))} of {len(df)}:")
        print(tabulate(df.iloc[start_index:start_index + 5], headers='keys', tablefmt='pretty'))
        start_index += 5

        if start_index >= len(df):
            print("\nNo more data available.")
            break

def get_filters():
    """Gets user input for city, month, and day to filter data."""
    cities = ['chicago', 'new york city', 'washington']
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

    print("\nPlease choose a city from the following:")
    print(', '.join(cities))
    while True:
        city = input("Enter city: ").strip().lower()
        if city in cities:
            break
        print("Invalid city. Please choose from the list.")

    print("\nPlease choose a month from the following:")
    print(', '.join(months))
    while True:
        month = input("Enter month: ").strip().lower()
        if month in months:
            break
        print("Invalid month. Please choose from the list.")

    print("\nPlease choose a day of the week from the following:")
    print(', '.join(days))
    while True:
        day = input("Enter day: ").strip().lower()
        if day in days:
            break
        print("Invalid day. Please choose from the list.")

    return city, month, day

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # Most common month # طباعة الشهر الأكثر شهرة
    most_common_month = df['month'].mode()[0]
    print(f"Most common month: {most_common_month}")

    # Most common day of the week
    most_common_day = df['day_of_week'].mode()[0]
    print(f"Most common day of the week: {most_common_day}")

    # Most common start hour
    most_common_hour = df['hour'].mode()[0]
    print(f"Most common start hour: {most_common_hour}")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # Most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(f"Most commonly used start station: {most_common_start_station}")

    # Most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print(f"Most commonly used end station: {most_common_end_station}")

    # Most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + " to " + df['End Station']
    most_common_trip = df['Trip'].mode()[0]
    print(f"Most common trip: {most_common_trip}")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def plot_data(df):
    """Plot a bar chart for the number of trips by day of the week."""
    day_counts = df['day_of_week'].value_counts()
    day_counts.plot(kind='bar', title="Number of Trips by Day of the Week")
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Trips')
    plt.show()

def main():
    """Main function to run the bikeshare script."""
    while True:
        city, month, day = get_filters()
        bikeshare_data = load_data(city, month, day)  # تغيير الاسم إلى bikeshare_data

        if bikeshare_data is None:
            break

        time_stats(bikeshare_data)
        station_stats(bikeshare_data)
        display_raw_data(bikeshare_data)
        plot_data(bikeshare_data)
        
        restart = input("\nWould you like to restart? (yes or no): ").strip().lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
    main()
