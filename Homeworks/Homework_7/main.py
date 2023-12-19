import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import requests

TIME_SEQUENCE = 24
DAYS_AMOUNT = 16
URL = 'https://api.open-meteo.com/v1/forecast'


def get_info_from_api(params):
    response = requests.get(URL, params=params)
    return response.json()


def task1():
    # Prepare params for the task 1
    params_1 = {'latitude': 49.4445,
                'longitude': 32.0574,
                'hourly': 'temperature_2m',
                'forecast_days': 16,
                'timezone': 'auto'}

    # Get data for the task 1
    data_1 = get_info_from_api(params_1)
    weather_timedate = data_1['hourly']['time']
    weather_temp = data_1['hourly']['temperature_2m']

    daily_temp_2m = [weather_temp[i:i + TIME_SEQUENCE] for i in range(0, DAYS_AMOUNT * TIME_SEQUENCE, TIME_SEQUENCE)]

    daily_temp_stats = list(
        map(lambda day_temp: (min(day_temp), max(day_temp), round(sum(day_temp) / len(day_temp), 1)),
            daily_temp_2m))

    # Prepare data for further use
    daily_min_temp = [i[0] for i in daily_temp_stats]
    daily_max_temp = [i[1] for i in daily_temp_stats]
    daily_average_temp = [i[2] for i in daily_temp_stats]
    weather_timedate_24 = [datetime.strptime(i, '%Y-%m-%dT%H:%M') for i in weather_timedate[11::24]]
    weather_timedate = [datetime.strptime(date, '%Y-%m-%dT%H:%M') for date in weather_timedate]

    # Create figure 1
    fig_1 = plt.figure(figsize=(5, 4), dpi=100)
    axes_1 = fig_1.add_axes((0.1, 0.1, 0.9, 0.9))
    axes_1.set_xlabel('Date and time')
    axes_1.set_ylabel('Temperature, °C')
    axes_1.set_title('Temperature chart')

    # Build chart 1 (Hourly temperature)
    axes_1.plot(weather_timedate, weather_temp, color='y', label='Hourly temperature')
    # Build chart 2 (Daily minimal temperature)
    axes_1.plot(weather_timedate_24, daily_min_temp, color='b', marker='o', label='Daily min temperature')
    # Build chart 3 (Daily maximal temperature)
    axes_1.plot(weather_timedate_24, daily_max_temp, color='r', marker='o', label='Daily max temperature')
    # Build chart 4 (Daily average temperature)
    axes_1.plot(weather_timedate_24, daily_average_temp, color='g', marker='o', label='Daily average temperature')

    axes_1.legend(loc=0)

    # Set figure configuration
    fig_1.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d:%m:%Y'))
    fig_1.gca().xaxis.set_major_locator(mdates.DayLocator(interval=2))
    plt.yticks(range(int(round(min(weather_temp))), int(round(max(weather_temp)) + 1), 1))

    fig_1.show()


def task2():
    # Create figure 2
    fig_2 = plt.figure(figsize=(5, 4), dpi=100)
    axes_2 = fig_2.add_axes((0.1, 0.1, 0.9, 0.9))
    axes_2.set_xlabel('Date')
    axes_2.set_ylabel('Sum of daily rain, mm')
    axes_2.set_title('Sum of daily rain in cities')

    # Prepare params for the task 2
    params_2_kyiv = {'latitude': 50.4547,
                     'longitude': 30.5238,
                     'daily': 'rain_sum',
                     'forecast_days': 7,
                     'timezone': 'auto'}

    params_2_lviv = {'latitude': 49.8383,
                     'longitude': 24.0232,
                     'daily': 'rain_sum',
                     'forecast_days': 7,
                     'timezone': 'auto'}

    # Get data for the task 2
    data_2_kyiv = get_info_from_api(params_2_kyiv)
    data_2_lviv = get_info_from_api(params_2_lviv)

    # Prepare data for further use
    daily_rain_sum_date = data_2_kyiv['daily']['time']
    kyiv_daily_rain_sum = data_2_kyiv['daily']['rain_sum']
    lviv_daily_rain_sum = data_2_lviv['daily']['rain_sum']

    date_spc_kiyv = [i for i in range(1, 8)]
    date_spc_lviv = [i + 0.3 for i in range(1, 8)]

    # Build bar chart 1 (Sum of daily rain in Kyiv)
    axes_2.bar(date_spc_kiyv, kyiv_daily_rain_sum, width=0.3, color='#0057b8', label='Kyiv')
    # Build bar chart 2 (Sum of daily rain in Lviv)
    axes_2.bar(date_spc_lviv, lviv_daily_rain_sum, width=0.3, color='#ffd700', label='Lviv')
    axes_2.legend(loc=0)

    # Set custom ticks for axes X and Y
    plt.xticks([i + 0.3 / 2 for i in range(1, 8)], daily_rain_sum_date)
    plt.yticks(np.arange(0, int(max(kyiv_daily_rain_sum + lviv_daily_rain_sum)) + 1, 0.5))

    fig_2.show()


def task3():
    # Prepare params for the task 3
    params_3 = {'latitude': 49.4445,
                'longitude': 32.0574,
                'hourly': ['cloud_cover_low', 'cloud_cover_mid', 'cloud_cover_high'],
                'forecast_days': 3,
                'timezone': 'auto'}

    # Get data for the task 3
    data_3 = get_info_from_api(params_3)

    # Prepare data for further use
    cloud_cover_labels = ['Low cloud cover', 'Middle cloud cover', 'High cloud cover']
    cloud_cover_date_and_time = [i[:-6] for i in data_3['hourly']['time'][::TIME_SEQUENCE]]
    daily_cloud_cover_low = data_3['hourly']['cloud_cover_low']
    daily_cloud_cover_mid = data_3['hourly']['cloud_cover_mid']
    daily_cloud_cover_high = data_3['hourly']['cloud_cover_high']

    average_daily_cloud_cover_low = [round(sum(daily_cloud_cover_low[i:i + TIME_SEQUENCE]) /
                                           len(daily_cloud_cover_low[i:i + TIME_SEQUENCE]))
                                     for i in range(0, len(daily_cloud_cover_low), TIME_SEQUENCE)]
    average_daily_cloud_cover_mid = [round(sum(daily_cloud_cover_mid[i:i + TIME_SEQUENCE]) /
                                           len(daily_cloud_cover_mid[i:i + TIME_SEQUENCE]))
                                     for i in range(0, len(daily_cloud_cover_mid), TIME_SEQUENCE)]
    average_daily_cloud_cover_high = [round(sum(daily_cloud_cover_high[i:i + TIME_SEQUENCE]) /
                                            len(daily_cloud_cover_high[i:i + TIME_SEQUENCE]))
                                      for i in range(0, len(daily_cloud_cover_high), TIME_SEQUENCE)]

    daily_average_cloud_cover = [(average_daily_cloud_cover_low[i],
                                  average_daily_cloud_cover_mid[i],
                                  average_daily_cloud_cover_high[i]) for i in
                                 range(len(average_daily_cloud_cover_low))]

    explode = [0.01] * 3

    # Create figure 3
    fig_3, axes_3 = plt.subplots(1, 3)
    plt.tight_layout()

    # Build bar charts
    for i in range(3):
        axes_3[i].set_title(cloud_cover_date_and_time[i])
        wedges, _, = axes_3[i].pie(daily_average_cloud_cover[i], labels=cloud_cover_labels,
                                   colors=['b', 'g', 'r'], explode=explode)
        axes_3[i].legend(wedges, cloud_cover_labels, loc=0)

    fig_3.show()


def task4():
    # Create figure 4
    fig_4 = plt.figure(figsize=(6, 6), dpi=100)
    axes_4 = fig_4.add_axes((0.05, 0.1, 0.9, 0.8))
    axes_4.set_xlabel('Wind speed, km/h')
    axes_4.set_title('Wind speed 10m in Cherkasy during the day')

    # Prepare params for the task 4
    params_4 = {'latitude': 49.4445,
                'longitude': 32.0574,
                'hourly': 'wind_speed_10m',
                'forecast_days': 1,
                'timezone': 'auto'}

    # Get data for the task 4
    data_4 = get_info_from_api(params_4)

    # Prepare data for further use
    wind_speed_10m = data_4['hourly']['wind_speed_10m']

    # Build histogram
    axes_4.hist(wind_speed_10m, density=True, stacked=True)

    axes_4.grid(True, color='0.1')
    fig_4.show()


def task5():
    # Create figure 5
    fig_5 = plt.figure(figsize=(6, 6), dpi=100)
    axes_5 = fig_5.add_axes((0.05, 0.1, 0.9, 0.8))
    axes_5.set_xlabel('Total cloud cover, %')
    axes_5.set_ylabel('Temperature 2m, °C')
    axes_5.set_title('Weather in Cherkasy during the day')

    # Prepare params for the task 5
    params_5 = {'latitude': 49.4445,
                'longitude': 32.0574,
                'hourly': ['temperature_2m', 'wind_speed_10m', 'relative_humidity_2m', 'precipitation', 'cloud_cover'],
                'forecast_days': 3,
                'timezone': 'auto'}

    # Get data for the task 5
    data_5 = get_info_from_api(params_5)

    # Prepare data for further use
    precipitation = data_5['hourly']['precipitation']
    indexes_with_precipitation = [i for i in range(len(precipitation)) if precipitation[i] > 0]
    temperature_2m = data_5['hourly']['temperature_2m']
    cloud_cover = data_5['hourly']['cloud_cover']
    relative_humidity_2m = data_5['hourly']['relative_humidity_2m']
    wind_speed_10m = data_5['hourly']['wind_speed_10m']

    # Build scatter with precipitation
    axes_5.scatter([cloud_cover[i] for i in range(len(cloud_cover)) if i in indexes_with_precipitation],
                   [temperature_2m[i] for i in range(len(temperature_2m)) if i in indexes_with_precipitation],
                   s=[wind_speed_10m[i] * 20 for i in range(len(wind_speed_10m))
                      if i in indexes_with_precipitation],
                   c=[relative_humidity_2m[i] for i in range(len(relative_humidity_2m))
                      if i in indexes_with_precipitation],
                   marker="^")
    # Build scatter without precipitation
    axes_5.scatter([cloud_cover[i] for i in range(len(cloud_cover)) if i not in indexes_with_precipitation],
                   [temperature_2m[i] for i in range(len(temperature_2m)) if i not in indexes_with_precipitation],
                   s=[wind_speed_10m[i] * 20 for i in range(len(wind_speed_10m))
                      if i not in indexes_with_precipitation],
                   c=[relative_humidity_2m[i] for i in range(len(relative_humidity_2m))
                      if i not in indexes_with_precipitation])

    fig_5.show()


def task6():
    # Create figure 5
    fig_6 = plt.figure(figsize=(6, 6), dpi=100)
    axes_6 = fig_6.add_axes((0.05, 0.1, 0.9, 0.8), projection='3d')
    axes_6.set_xlabel('Total cloud cover, %')
    axes_6.set_ylabel('Temperature 2m, °C')
    axes_6.set_title('Weather in Cherkasy during the day')

    # Prepare params for the task 5
    params_6 = {'latitude': 49.4445,
                'longitude': 32.0574,
                'hourly': ['temperature_2m', 'wind_speed_10m', 'cloud_cover'],
                'forecast_days': 7,
                'timezone': 'auto'}

    # Get data for the task 5
    data_6 = get_info_from_api(params_6)

    # Prepare data for further use
    temperature_2m = data_6['hourly']['temperature_2m']
    cloud_cover = data_6['hourly']['cloud_cover']
    wind_speed_10m = data_6['hourly']['wind_speed_10m']

    # Build scatter with precipitation
    axes_6.contour3D(temperature_2m,
                     cloud_cover,
                     [[i for i in wind_speed_10m] for _ in range(len(wind_speed_10m))],
                     128,
                     cmap='Blues')

    fig_6.show()


def main():
    # TASK 1
    # task1()

    # TASK 2
    # task2()

    # TASK 3
    # task3()

    # TASK 4
    # task4()

    # TASK 5
    # task5()

    # TASK 6
    # task6()
    plt.show()


if __name__ == '__main__':
    main()
