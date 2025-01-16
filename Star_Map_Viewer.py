import streamlit as st
import requests
import base64
from datetime import datetime, time

def fetch_star_chart(api_key, latitude, longitude, datetime_str):
    """
    Fetches a star chart image from the Astronomy API based on the given parameters.

    :param api_key: Dictionary containing 'application_id' and 'application_secret'
    :param latitude: Latitude of the observer's location
    :param longitude: Longitude of the observer's location
    :param datetime_str: The datetime as a string in the format "YYYY-MM-DD HH:MM:SS"
    :return: Image URL of the star chart if successful, else None
    """
    # Extract the date and time from datetime_str
    date, time = datetime_str.split(" ")

    # Construct the Basic Authentication string
    auth_string = f"{api_key['application_id']}:{api_key['application_secret']}"
    encoded_auth_string = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_auth_string}",
        "Content-Type": "application/json"  # Ensure the content type is set to JSON
    }
    
    # Construct the body of the request (Star chart parameters)
    data = {
        "observer": {
            "latitude": latitude,
            "longitude": longitude,
            "date": date
        },
        "view": {
            "type": "area",
            "parameters": {
                "position": {
                    "equatorial": {
                        "rightAscension": 14.83,  # Example RA (can adjust or make dynamic)
                        "declination": -15.23    # Example Dec (can adjust or make dynamic)
                    }
                },
                "zoom": 6,  # Increased zoom level for a more focused area (adjust as needed)
                "fisheye": True  # To give a more circular view, if supported
            }
        }
    }

    # Send the request to fetch the star chart
    response = requests.post("https://api.astronomyapi.com/api/v2/studio/star-chart", headers=headers, json=data)

    # Check the response
    if response.status_code == 200:
        image_url = response.json()['data']['imageUrl']
        return image_url
    else:
        # Log the error message for debugging
        print(f"Error {response.status_code}: {response.text}")
        return None

def main():
    # Streamlit app title
    st.title("Star Map Viewer")

    # User Inputs
    latitude = st.number_input("Latitude", value=0.0)
    longitude = st.number_input("Longitude", value=0.0)
    date_input = st.date_input("Date", min_value=datetime.today())
    time_input = st.time_input("Time", value=time(20, 0))

    # Convert date and time to string
    date_str = date_input.strftime("%Y-%m-%d")
    time_str = time_input.strftime("%H:%M:%S")
    datetime_str = f"{date_str} {time_str}"

    # Fetch API Key from Streamlit secrets
    api_key = st.secrets["astronomyapi"]

    # Fetch Star Chart
    if st.button("Generate Star Map"):
        image_url = fetch_star_chart(api_key, latitude, longitude, datetime_str)
        if image_url:
            st.image(image_url, caption="Star Map", use_column_width=True)
        else:
            st.error("Error fetching star chart.")

if __name__ == "__main__":
    main()
