"""
Name: Lashman Singh
Assignment: 1
Date: 30-08-2024
"""

# REQUIRED LIBRARY TO RUN THIS FILE ERROR FREE. 
# [ pip install requests python-dateutil colorama ]

from requests import get
from dateutil.parser import parse
from colorama import just_fix_windows_console, Fore, Style

# Setup colorama
just_fix_windows_console()

# API key for Winnipeg Transit
API_KEY = "QgBGbuO1DN9XERs23fmK"

# Function to fetch and display nearby bus stops
def fetch_nearby_stops(lon, lat, distance):
    url_stops = f"https://api.winnipegtransit.com/v3/stops.json?lon={lon}&lat={lat}&distance={distance}&api-key={API_KEY}"
    resp_stops = get(url_stops).json()
    stops = resp_stops.get('stops', [])
    
    if stops:
        print("Nearby Bus Stops:")
        for stop in stops:
            print(f"Stop ID: {stop['key']} - {stop['name']}")
    else:
        print("No stops found in this area.")
    
    return stops

# Function to fetch and display scheduled and estimated arrival times for a specific stop
def fetch_arrival_times(stop_id):
    url_schedule = f"https://api.winnipegtransit.com/v3/stops/{stop_id}/schedule.json?api-key={API_KEY}"

    try:
        resp_schedule = get(url_schedule).json()

        # Check for the presence of an error in the API response
        if 'error' in resp_schedule:
            print(f"Error: {resp_schedule['error']['message']}")
            return  # Exit the function if there's an error

        if 'stop-schedule' in resp_schedule:
            schedule = resp_schedule['stop-schedule']['route-schedules']
            for route in schedule:
                print(f"Route: {route['route']['name']}")
                for scheduled_stop in route['scheduled-stops']:
                    # Check if 'arrival' key exists in 'times' before accessing it
                    if 'arrival' in scheduled_stop['times']:
                        scheduled_time = parse(scheduled_stop['times']['arrival'].get('scheduled'))
                        estimated_time = parse(scheduled_stop['times']['arrival'].get('estimated', scheduled_time))

                        if estimated_time > scheduled_time:
                            color = Fore.RED
                        elif estimated_time < scheduled_time:
                            color = Fore.BLUE
                        else:
                            color = Fore.GREEN

                        print(color + f"Scheduled: {scheduled_time.strftime('%H:%M:%S')} | Estimated: {estimated_time.strftime('%H:%M:%S')}")
                        print(Style.RESET_ALL)
                    else:
                        print("Arrival times not available for this scheduled stop ID.")
        else:
            print("No schedule information available for this stop." )

    except Exception as e:
        print(Fore.RED + f"Wrong Stop ID! Please choose a above mentioned stop." + Style.RESET_ALL)

# Main logic to execute the script
if __name__ == "__main__":
    lon = -97.14148496904943  # GPS longitude of location
    lat = 49.90060230978042   # GPS latitude of location
    distance = 150  # radius in meters to search around GPS coordinates

    # Fetch and display nearby stops
    stops = fetch_nearby_stops(lon, lat, distance)
    
    if stops:
        stop_id = input("\nEnter the Stop ID to see scheduled and estimated arrival times: ")
        fetch_arrival_times(stop_id)
    else:
        print("No stops to select.")
