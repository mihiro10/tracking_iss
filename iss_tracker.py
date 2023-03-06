from flask import Flask, request
from geopy.geocoders import Nominatim
import xmltodict
import requests
import math
import time

app = Flask(__name__)
data = {}

def load_xml()-> dict:
    """
    This function returns the entire data as a dictionary.

    Args:

    Returns:
    entire_data = dictionary of entire data

    """
    url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'
    response = requests.get(url)
    entire_data = xmltodict.parse(response.text)
    return entire_data


def get_data(entire_data:dict) -> list:
    """
    This function returns the state vector as a list of dictionaries

    Args:

    Returns:
    entire_data = list of dictionary of information within state vetor

    """
    return entire_data['ndm']['oem']['body']['segment']['data']['stateVector']

entire_data = load_xml() #entire dataset

data = get_data(entire_data) #define data as global variable

@app.route('/', methods = ['GET']) # default curl method
def location() -> list:
    """
    This function returns the state vectors in the xml file

    Args:

    Returns:
        data['ndm']['oem']['body']['segment']['data']['stateVector'] = Information within State Vectors as a list of dictionaries

    """
    try:
        global data
        return data
    except NameError:
        return "Data does not exist. \n"



@app.route('/epochs', methods = ['GET'])
def epochs_data() -> list:
    """
    This function returns a list of epochs

    Args:

    Returns:
        epoch_list = list of epochs

    """
    global data
    epoch_list = []
    total_results = 0
    index = 0
    
    # check offset
    try:
       offset = int(request.args.get('offset',0))
    except ValueError:
       return "Bad Input",400

    #check limit
    try:
       limit = int(request.args.get('limit',len(data)))
    except ValueError:
       return "Bad Input",400
    except NameError:
        return "Data does not exist. \n"


    for epoch_values in data:
        if (total_results == limit):
            break
        if (index >= offset):
            epoch_list.append(epoch_values['EPOCH'])
            total_results += 1
        index += 1
        
    return epoch_list




@app.route('/epochs/<epoch>', methods = ['GET'])
def epochs_data_specific(epoch: str) -> dict:
    """
    This function returns a specific epoch value taken from the curl

    Args:
    epoch = value of a specific epoch as a string

    Returns:
    epoch_values = a specific epoch value as a dict
    string = when a match is not found

    """
    try:
        global data
        for epoch_values in data:
            if (epoch_values['EPOCH'] == epoch):
                return epoch_values  
        return "did not find matching epoch"
    except NameError:
        return "Data does not exist. \n"





@app.route('/epochs/<epoch>/speed', methods = ['GET'])
def epochs_data_specific_speed(epoch: str) -> dict:
    """
    This function returns a specific epoch value taken from the curl

    Args:
    epoch = value of a specific epoch as a string

    Returns:
    {"speed": speed} = dictionary of the speed value for the specific data

    """
    try:
        global data
        for epoch_values in data:
            if (epoch_values['EPOCH'] == epoch):
                x_dot = float(epoch_values['X_DOT']['#text'])
                y_dot = float(epoch_values['Y_DOT']['#text'])
                z_dot = float(epoch_values['Z_DOT']['#text'])
                speed = math.sqrt(x_dot**2 + y_dot**2 + z_dot**2)
                return {"speed": speed}
        return "did not find matching epoch"
    except NameError: 
        return "Data does not exist. \n"

@app.route('/delete-data', methods=['DELETE'])
def delete_data():
    """
    This deletes the data of entire data and data

    Args:

    Returns:
    If sucessful "All data has been deleted successfully." and "Data was already deleted" if it was already deleted
    
    """
    try:
        global data
        global entire_data
        del data
        del entire_data
        return 'All data has been deleted successfully.\n'
    except NameError:
        return "Data was already deleted. \n"

@app.route('/get-data', methods=['POST'])
def recover_data():
    """
    This recovers the data of entire data and data

    Args:

    Returns:
    "All data has been updated successfully"
    
    """
    global entire_data
    global data
    entire_data = load_xml()
    data = get_data(entire_data)
    return 'All data has been updated successfully.\n'

# What happens when ou post 2 times?

@app.route('/help', methods = ['GET'])
def help():
    """
    This function returns a human-readable description of all available routes and their methods for the API

    Args:

    Returns:
        Help string
    """
    return """
    Available routes:
    
    GET /
        - Returns the state vectors in the XML file
        
    GET /epochs?limit=int&offset=int
        - Returns a list of epoch values
        - Optional query parameters:
            - offset: number of results to skip
            - limit: maximum number of results to return
    
            
    GET /epochs/<epoch>
        - Returns a specific epoch value based on the provided epoch string
        
    GET /epochs/<epoch>/speed
        - Returns the speed value for a specific epoch
        
    DELETE /delete-data
        - Deletes the global data variable
        
    POST /get-data
        - Retrieves the XML data again and updates the global data variable

    GET /comment
        - Returns the comment list object

    GET /header
        - Returns the header as a dictionary
    
    GET /metadata
        - Returns the metadata dictionary from the ISS data

    GET /epochs/<epoch>/location
        - Returns a specific location taken from the curl
            "lat": latitude
            "lon": longitude
            "alt": altitude
            "geoloc": geo location

    GET /now
        - Dictionary of information about the latest recording of the ISS
            "closest_epoch" = The time of the latest epoch
            "seconds from now" = How long ago it was in seconds
            "location" = dictionary of latitude, longitude, and altitude in km
            "geoloc" = Geo location
            "speed" = Speed at given instance in km/s

    
    
    """

@app.route('/comment', methods=['GET'])
def comment():
    """
    This function returns the comment list object

    Args:

    Returns:
        Comment list object from the ISS data

    """
    try:
        global entire_data
        return entire_data['ndm']['oem']['body']['segment']['data']['COMMENT']
    except NameError:
        return "Data does not exist. \n"

@app.route('/header', methods=['GET'])
def header() -> dict:
    """
    This function returns the header as a dictionary

    Args:

    Returns:
        Header information as a dictionary

    """
    try:
        global entire_data
        return entire_data['ndm']['oem']['header']
    except NameError:
        return "Data does not exist. \n"
    
@app.route('/metadata', methods=['GET'])
def metadata() -> dict:
    """
    This function returns the metadata dictionary from the ISS data

    Args:

    Returns:
        metadata dictionary from ISS data

    """
    try:
        global entire_data
        return entire_data['ndm']['oem']['body']['segment']['metadata']
    except NameError:
        return "Data does not exist. \n"
    

@app.route('/epochs/<epoch>/location', methods = ['GET'])
def epochs_data_specific_location(epoch: str) -> dict:
    """
    This function returns a specific location taken from the curl

    Args:
    epoch = value of a specific epoch as a string

    Returns:
    Dictionary of different information
        "lat": latitude
        "lon": longitude
        "alt": altitude
        "geoloc": geo location

    """
    try:
        global data
        MEAN_EARTH_RADIUS = 6371
        for epoch_values in data:
            if (epoch_values['EPOCH'] == epoch):
                x = float(epoch_values['X']['#text'])
                y = float(epoch_values['Y']['#text'])
                z = float(epoch_values['Z']['#text'])
                time_of_epoch = str(epoch_values['EPOCH'])
                hrs = int(time_of_epoch[9] + time_of_epoch[10])
                mins = int(time_of_epoch[12] + time_of_epoch[13])

                lat = math.degrees(math.atan2(z, math.sqrt(x**2 + y**2)))                
                lon = math.degrees(math.atan2(y, x)) - ((hrs-12)+(mins/60))*(360/24) + 24
                
                # Accounting for degrees represented past parameters

                while (lon < -180): # wh
                    lon = lon + 360 
                while (lon > 180):
                    lon = lon - 360
                alt = math.sqrt(x**2 + y**2 + z**2) - MEAN_EARTH_RADIUS 

                geocoder = Nominatim(user_agent='iss_tracker')
                geoloc = geocoder.reverse((lat, lon), zoom=5, language='en')

                try:
                    return {"lat": lat, "lon": lon, "alt": alt, "geoloc": geoloc.address}
                except AttributeError:
                    return {"lat": lat, "lon": lon, "alt": alt, "geoloc": "Over the ocean"}
        return "did not find matching epoch"
    except NameError: 
        return "Data does not exist. \n"
    

@app.route('/now', methods = ['GET'])
def epochs_data_now() -> dict:
    """
    This function returns information about the lastest recoring of the ISS

    Args:

    Returns:
    Dictionary of information about the latest recording of the ISS
        "closest_epoch" = The time of the latest epoch
        "seconds from now" = How long ago it was in seconds
        "location" = dictionary of latitude, longitude, and altitude in km
        "geoloc" = Geo location
        "speed" = Speed at given instance in km/s

    """


    try:
        global data
        MEAN_EARTH_RADIUS = 6371
        really_large_value = 1e20
        smallest_difference = really_large_value
        for epoch_values in data:
            time_now = time.time()         # gives present time in seconds since unix epoch
            time_epoch = time.mktime(time.strptime(epoch_values['EPOCH'] [:-5], '%Y-%jT%H:%M:%S'))        # gives epoch (eg 2023-058T12:00:00.000Z) time in seconds since unix epoch
            difference = time_now - time_epoch
            if difference < smallest_difference:
                smallest_difference = difference
                closest_epoch = epoch_values
        
        # Location
        x = float(closest_epoch['X']['#text'])
        y = float(closest_epoch['Y']['#text'])
        z = float(closest_epoch['Z']['#text'])
        time_of_epoch = str(closest_epoch['EPOCH'])
        hrs = int(time_of_epoch[9] + time_of_epoch[10])
        mins = int(time_of_epoch[12] + time_of_epoch[13])
        lat = math.degrees(math.atan2(z, math.sqrt(x**2 + y**2)))                
        lon = math.degrees(math.atan2(y, x)) - ((hrs-12)+(mins/60))*(360/24) + 24
        
        # Accounting for degrees represented past parameters

        while (lon < -180): # wh
            lon = lon + 360 
        while (lon > 180):
            lon = lon - 360
        alt = math.sqrt(x**2 + y**2 + z**2) - MEAN_EARTH_RADIUS 

        #geo location
        geocoder = Nominatim(user_agent='iss_tracker')
        geoloc = geocoder.reverse((lat, lon), zoom=5, language='en')

        #speed calculation
        x_dot = float(closest_epoch['X_DOT']['#text'])
        y_dot = float(closest_epoch['Y_DOT']['#text'])
        z_dot = float(closest_epoch['Z_DOT']['#text'])
        speed = math.sqrt(x_dot**2 + y_dot**2 + z_dot**2)

        return {"closest_epoch": closest_epoch['EPOCH'], "seconds from now": smallest_difference, "location":{"lat": lat, "lon": lon, "alt": alt,}, "geoloc": geoloc.address, "speed": speed}
    except AttributeError:
        return {"closest_epoch": closest_epoch['EPOCH'], "seconds from now": smallest_difference, "location":{"lat": lat, "lon": lon, "alt": alt,}, "geoloc": "over the ocean", "speed": speed}
    except NameError: 
        return "Data does not exist. \n"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')