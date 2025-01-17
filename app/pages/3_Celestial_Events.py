import streamlit as st
import requests
from datetime import datetime
import base64

def fetch_celestial_events(api_key, latitude, longitude, elevation, from_date, to_date, time):
    """
    Fetches celestial events for the given location and date range from the Astronomy API.

    :param api_key: Dictionary containing 'application_id' and 'application_secret'
    :param latitude: Latitude of the observer's location
    :param longitude: Longitude of the observer's location
    :param elevation: Elevation (altitude) of the observer's location in meters
    :param from_date: Start date in 'YYYY-MM-DD' format
    :param to_date: End date in 'YYYY-MM-DD' format
    :param time: Specific time in 'HH:MM:SS' format
    :return: List of celestial events
    """
    # Construct the Basic Authentication string
    auth_string = f"{api_key['application_id']}:{api_key['application_secret']}"
    encoded_auth_string = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_auth_string}",
        "Content-Type": "application/json"
    }

    # Construct the body of the request
    data = {
        "latitude": latitude,
        "longitude": longitude,
        "elevation": elevation,  # Added elevation parameter
        "from_date": from_date,
        "to_date": to_date,
        "time": time,  # Added time parameter
        "output": "rows"
    }

    # Send the request to fetch celestial events
    try:
        response = requests.get("https://api.astronomyapi.com/api/v2/bodies/events/sun", headers=headers, params=data)
        
        # Log the raw response text for debugging
        #st.write("Raw API Response: ", response.text)

        # Check if the response is JSON and can be parsed
        try:
            response_data = response.json()
        except ValueError:
            st.error(f"Failed to decode JSON: {response.text}")
            return None

        # Check for successful response
        if response.status_code == 200:
            if 'data' in response_data:
                events_data = response_data['data']
                if 'rows' in events_data:
                    rows = events_data['rows']
                    if rows:
                        events = rows[0]['events']
                        if events:
                            # If events exist, display them in a structured format
                            for event in events:
                                st.subheader(f"Event: {event['type'].replace('_', ' ').title()}")
                                
                                # Event Highlights
                                if "eventHighlights" in event:
                                    event_highlights = event["eventHighlights"]
                                    st.write(f"**Partial Start:** {event_highlights.get('partialStart', {}).get('date', 'N/A')} (Altitude: {event_highlights.get('partialStart', {}).get('altitude', 'N/A')}°)")
                                    st.write(f"**Peak:** {event_highlights.get('peak', {}).get('date', 'N/A')} (Altitude: {event_highlights.get('peak', {}).get('altitude', 'N/A')}°)")
                                    st.write(f"**Partial End:** {event_highlights.get('partialEnd', {}).get('date', 'N/A')} (Altitude: {event_highlights.get('partialEnd', {}).get('altitude', 'N/A')}°)")

                                # Rise and Set Times
                                st.write(f"**Rise Time:** {event.get('rise', 'N/A')}")
                                st.write(f"**Set Time:** {event.get('set', 'N/A')}")

                                # Extra Information (e.g., obscuration for solar events)
                                if "extraInfo" in event:
                                    extra_info = event["extraInfo"]
                                    st.write(f"**Obscuration:** {extra_info.get('obscuration', 'N/A') * 100}%")

                        else:
                            st.write("No celestial events found for the selected date and time.")
                    else:
                        st.error("No event data found in the response.")
                else:
                    st.error("No 'rows' field found in the response.")
            else:
                st.error("No 'data' field found in the response.")
        else:
            st.error(f"Error fetching data: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        # In case of an error with the request (e.g., network error)
        st.error(f"Request failed: {str(e)}")
        return None


def main():
    # Streamlit app title
    st.title("Celestial Events Viewer")
    st.caption("Find out about the Solar and Lunar Eclipses visible in your location!")

    # User Inputs
    latitude = st.number_input("Latitude", value=48.5)
    longitude = st.number_input("Longitude", value=13.5)
    elevation = st.number_input("Elevation (in meters)", value=0)  # Added elevation input
    from_date = st.date_input("From Date", min_value=datetime.today())
    to_date = st.date_input("To Date", min_value=datetime.today())
    time_input = st.time_input("Time", value=datetime.now().time())  # Added time input

    # Convert date and time to string
    from_date_str = from_date.strftime("%Y-%m-%d")
    to_date_str = to_date.strftime("%Y-%m-%d")
    time_str = time_input.strftime("%H:%M:%S")

    # Fetch API Key from Streamlit secrets
    api_key = st.secrets["astronomyapi"]

    # Fetch Celestial Events
    if st.button("Get Celestial Events"):
        events = fetch_celestial_events(api_key, latitude, longitude, elevation, from_date_str, to_date_str, time_str)


if __name__ == "__main__":
    main()
