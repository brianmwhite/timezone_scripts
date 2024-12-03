# This script was created with assistance from ChatGPT, an AI language model developed by OpenAI.

# import urllib.request
# import json
import sys
# import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

def format_utc_offset(offset_seconds):
    """Format UTC offset as HH:MM."""
    total_minutes = int(offset_seconds / 60)
    hours = total_minutes // 60
    minutes = abs(total_minutes % 60)  # Use abs to avoid negative signs in minutes
    return f"{hours:+02}:{minutes:02}"

def get_timezone_name(timezone):
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
    return timezone_path

def get_next_transition(timezone_name):
    try:
        # Create a timezone object
        tz = ZoneInfo(timezone_name)
        
        # Get the current time in the specified timezone
        now = datetime.now(tz)
        
        # Get the current offset and DST status
        current_offset = now.utcoffset()
        
        # Find the next transition by iterating future dates
        days_ahead = 365  # Check up to one year in advance
        for day_offset in range(1, days_ahead + 1):
            future_date = now + timedelta(days=day_offset)
            future_offset = future_date.astimezone(tz).utcoffset()
            
            # Check if the offset has changed
            if future_offset != current_offset:
                # Found the next transition
                transition_date = future_date.replace(hour=2, minute=0, second=0, microsecond=0)
                dst_change = "starts" if future_date.dst() != timedelta(0) else "ends"
                formatted_date = transition_date.strftime("%B %d, %Y")  # Format as "Month Day, Year"
                return formatted_date, dst_change
        
        return None, "No transition found within one year."
    except Exception as e:
        return None, f"Error: {e}"

def get_timezone_info_local(timezone="et"):
    try:
        # Create a timezone object
        timezone_name = get_timezone_name(timezone)
        tz = ZoneInfo(timezone_name)
        
        # Get the current time in the specified timezone
        now = datetime.now(tz)
        
        # Determine if it's DST and the UTC offset
        # is_dst = now.dst() != timedelta(0)
        # utc_offset = now.utcoffset().total_seconds() / 3600  # Convert to hours
        utc_offset_as_time = format_utc_offset(now.utcoffset().total_seconds())
        timezone_abbreviation = now.tzname()
        
        # Get the next transition
        next_transition, dst_change = get_next_transition(timezone_name)
        
        # Display results
        # print(f"Time Zone: {timezone_name}")
        # print(f"Current Time: {now}")
        print(f"{timezone_abbreviation} (UTC{utc_offset_as_time})")
        # print(f"Daylight Saving Time: {'Yes' if is_dst else 'No'}")
        # print(f"UTC Offset: {utc_offset:+.2f} hours")
        
        if next_transition:
            print(f"Next Time Change: {dst_change} on {next_transition}")
        else:
            print("Next Time Change: Not found within one year.")
    except Exception as e:
        print(f"Error: {e}. Please ensure the timezone name is valid.")

# def get_time_info_from_api(timezone="et"):
#     base_url = "http://worldtimeapi.org/api/timezone/"
    
#     timezone_path = get_timezone_name(timezone)

#     # Combine base URL with the timezone path
#     url = base_url + timezone_path
    
#     # Check if we have stored data for today
#     cached_file = f"cached_time_{timezone.lower()}.json"
#     today_date = datetime.now().date()
    
#     if os.path.exists(cached_file):
#         with open(cached_file, 'r') as file:
#             cached_data = json.load(file)
#             cached_date = datetime.fromisoformat(cached_data['date']).date()
            
#             if cached_date == today_date:
#                 # Use cached data if it's from today
#                 return f"{cached_data['abbreviation']} (UTC{cached_data['utc_offset']})"
    
#     # If no valid cache is found or the cache is outdated, query the API
#     with urllib.request.urlopen(url) as response:
#         data = response.read()
        
#     # Decode the response to a string
#     decoded_data = data.decode('utf-8')
    
#     # Parse the JSON data
#     time_info = json.loads(decoded_data)
    
#     # Store the relevant fields with today's date
#     cached_data = {
#         "date": today_date.isoformat(),
#         "utc_offset": time_info['utc_offset'],
#         "abbreviation": time_info['abbreviation']
#     }
    
#     # Write the data to the cache file
#     with open(cached_file, 'w') as file:
#         json.dump(cached_data, file)
    
#     # Format and return the result
#     result = f"{time_info['abbreviation']} (UTC{time_info['utc_offset']})"
#     print(result)

# Example usage
if __name__ == "__main__":
    timezone = sys.argv[1] if len(sys.argv) > 1 else "et"
    try:
        get_timezone_info_local(timezone)
    except ValueError as e:
        print(e)