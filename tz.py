import urllib.request
import json
import sys
import os
from datetime import datetime

def get_time_info(timezone="et"):
    base_url = "http://worldtimeapi.org/api/timezone/"
    
    # Determine the correct timezone path based on the input
    if timezone.lower() == "et":
        timezone_path = "America/New_York"
    elif timezone.lower() == "ct":
        timezone_path = "America/Chicago"
    elif timezone.lower() == "mt":
        timezone_path = "America/Denver"
    elif timezone.lower() == "pt":
        timezone_path = "America/Los_Angeles"
    else:
        raise ValueError("Unsupported timezone. Use 'ET' for Eastern Time or 'CT' for Central Time or 'MT' for Mountain Time or 'PT' for Pacific Time'.")
    
    # Combine base URL with the timezone path
    url = base_url + timezone_path
    
    # Check if we have stored data for today
    cached_file = f"cached_time_{timezone.lower()}.json"
    today_date = datetime.now().date()
    
    if os.path.exists(cached_file):
        with open(cached_file, 'r') as file:
            cached_data = json.load(file)
            cached_date = datetime.fromisoformat(cached_data['date']).date()
            
            if cached_date == today_date:
                # Use cached data if it's from today
                return f"{cached_data['abbreviation']} (UTC{cached_data['utc_offset']})"
    
    # If no valid cache is found or the cache is outdated, query the API
    with urllib.request.urlopen(url) as response:
        data = response.read()
        
    # Decode the response to a string
    decoded_data = data.decode('utf-8')
    
    # Parse the JSON data
    time_info = json.loads(decoded_data)
    
    # Store the relevant fields with today's date
    cached_data = {
        "date": today_date.isoformat(),
        "utc_offset": time_info['utc_offset'],
        "abbreviation": time_info['abbreviation']
    }
    
    # Write the data to the cache file
    with open(cached_file, 'w') as file:
        json.dump(cached_data, file)
    
    # Format and return the result
    result = f"{time_info['abbreviation']} (UTC{time_info['utc_offset']})"
    return result

# Example usage
if __name__ == "__main__":
    timezone = sys.argv[1] if len(sys.argv) > 1 else "et"
    try:
        print(get_time_info(timezone))
    except ValueError as e:
        print(e)