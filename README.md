<h2>Tracking The ISS</h2>
This project aims to develop a Flask web application that provides information on the current location of the International Space Station (ISS). The application retrieves the current location data from an XML file published by NASA and provides a RESTful API to query specific information. This project is then packaged and uploaded onto dockerhub where this information can be pulled from.

<h3>Data Set</h3>
The data set used in this project is the ISS OEM data set published by NASA. The data set is available as an XML file and can be accessed using the following link: https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml.


<h3>Flask App/Scripts</h3>

`iss_tracker.py:` contains a number of endpoints that provide information on the ISS's location and speed:

| Route | Method    | What it does   |
| :---:   | :---: | :---: |
| <code>/</code> | GET   |  Returns the entire state vector information as a list of dictionaries  |
| <code>/epochs</code> | GET   |  Returns a list of all Epochs in the data set |
| <code>/epochs?limit=int&offset=int</code> | GET   |  Returns a list of Epochs given query parameters |
| `/epochs/<epoch>` </code> | GET   |  Returns a specific epoch value as a dictionary. |
| `/epochs/<epoch>/speed` </code> | GET   |  Returns the speed of the ISS at a specific epoch as a dictionary. |
| `/delete-data` </code> | DELETE   | Deletes the global data and global entire_data variables. |
| `/post-data` </code> | POST | Retrieves the XML data again and updates the global data variable |
| ``/comment``                    | GET        | Returns 'comment' list object from ISS data  |
| ``/header``                     | GET        | Returns 'header' dict object from ISS data   |
| ``/metadata``                   | GET        | Returns 'metadata' dict object from ISS data |
| ``/epochs/<epoch>/location``    | GET        | Returns latitude, longitude, altitude, and geoposition for given Epoch|
| ``/now``                        | GET        | Returns latitude, longitude, altidue, and geoposition for Epoch that is nearest in time|
| `/help` </code> | GET | Returns help text as a string. Gives info on all methods|

`Dockerfile:` Is a document that contains the commands neccesary to containerize the iss_tracker docker image.

`docker-compose.yml` Is a file that automates the deployment of the app. It is configured to the image with the chosen tag.

<h3>Installation Methods:</h3>

<h4>Method 1: Using the existing Docker Image</h4>
Step 1: 
Run the following in the terminal to pull the docker container.

```
docker pull mihiro10/iss_tracker:hw05
```

Run,

```
docker run -it --rm -p 5000:5000 mihiro10/iss_tracker:hw05
```

Finally, in a seperate terminal, run the different desired methods.

```
curl localhost:5000/
```

<h4>Method 2: Building the image from Dockerfile</h4>

Check that you are in the directory with the contents of homework05

Here is a way to check.

Run

```
ls
```

and make sure the output looks like

```
Dockerfile  README.md  iss_tracker.py
```

Now, to build the image using the Dockerfile, use

```
docker build -t <username>/iss_tracker:<tag> .
```

To check that it was built, run 
```
$ docker images
REPOSITORY                  TAG       IMAGE ID       CREATED         SIZE
mihiro10/iss_tracker        hw05      ff34eab7ec29   22 hours ago    897MB
``` 


Then to run the flask app, run

```
docker run -it --rm -p 5000:5000 <username>/iss_tracker:<tag>
```

Finally, open up another terminal and run the different methods

```
curl 'localhost:5000/' 
```

<h4>Method 3: Using the docker-compose.yml file</h4>


This method allows you to use the docker-compose.yml file to spin up all the required services in a few simple commands.


Once the repository is cloned, we need to make sure your port is not currently being used, and if so, stop it to allow the port to be used. To check this run

```
docker ps -a
```
If there is a container already running, it will look something like this.
```
CONTAINER ID   IMAGE                      COMMAND                  CREATED          STATUS                    PORTS                                       NAMES
e86b5ae75b3a   mihiro10/iss_tracker:1.0   "python iss_tracker.…"   26 minutes ago   Up 22 minutes             0.0.0.0:5000->5000/tcp, :::5000->5000/tcp   tracking_iss_flask-app_1
```

If the port is being used, run
```
docker stop "container id"
```

and 

```
docker rm -f “container ID”
```

Once the ports are all closed, run the following command to build and deploy your app using

```
docker-compose up
```

This will open up a flask app and take over your terminal. Here is a sample output

```
ubuntu@mihiro10-vm:~/coe332/tracking_iss$ docker-compose up
Starting tracking_iss_flask-app_1 ... done
Attaching to tracking_iss_flask-app_1
flask-app_1  |  * Serving Flask app 'iss_tracker'
flask-app_1  |  * Debug mode: on
flask-app_1  | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
flask-app_1  |  * Running on all addresses (0.0.0.0)
flask-app_1  |  * Running on http://127.0.0.1:5000
flask-app_1  |  * Running on http://172.19.0.2:5000
flask-app_1  | Press CTRL+C to quit
flask-app_1  |  * Restarting with stat
flask-app_1  |  * Debugger is active!
flask-app_1  |  * Debugger PIN: 139-547-370
```

Once up, open up another terminal to run the queries desired. 



<h3>Example Queries</h3>

Once the Flask app is up and running, the following methods are available.


<h4>To return the entire state vector information as a list of dictionaries.</h4>
Run

```
curl localhost:5000
```


Here is an example snippet

```
 {
    "EPOCH": "2023-063T11:51:00.000Z",
    "X": {
      "#text": "-242.12485388276099",
      "@units": "km"
    },
    "X_DOT": {
      "#text": "5.9511600325922904",
      "@units": "km/s"
    },
    "Y": {
      "#text": "-5285.0073157200604",
      "@units": "km"
    },
    "Y_DOT": {
      "#text": "-3.1998687127665399",
      "@units": "km/s"
    },
    "Z": {
      "#text": "4254.7035249005503",
      "@units": "km"
    },
    "Z_DOT": {
      "#text": "-3.6194381039437298",
      "@units": "km/s"
    }
  },

  ... etc.
```



<h4>To find the list of epochs in the XML file, run</h4>

```
curl localhost:5000/epochs
```


Here is an example.

```
[
  "2023-063T11:23:00.000Z",
  "2023-063T11:27:00.000Z",
  "2023-063T11:31:00.000Z",
  "2023-063T11:35:00.000Z",
  "2023-063T11:39:00.000Z",
  "2023-063T11:43:00.000Z",
  "2023-063T11:47:00.000Z",
  "2023-063T11:51:00.000Z",
  "2023-063T11:55:00.000Z",
  "2023-063T11:59:00.000Z",
  "2023-063T12:00:00.000Z"
... etc.
```

To specify the range of these epochs, a query parameters can be added. 
```
curl localhost:5000/epochs?limit=int&offset=int
```
Here is an example using ?limit=20&offset=50
```
[
  "2023-058T12:00:00.000Z",
  "2023-058T12:04:00.000Z",
  "2023-058T12:08:00.000Z",
  "2023-058T12:12:00.000Z",
  "2023-058T12:16:00.000Z",
  "2023-058T12:20:00.000Z",
  "2023-058T12:24:00.000Z",
  "2023-058T12:28:00.000Z",
  "2023-058T12:32:00.000Z",
  "2023-058T12:36:00.000Z",
  "2023-058T12:40:00.000Z",
  "2023-058T12:44:00.000Z",
  "2023-058T12:48:00.000Z",
  "2023-058T12:52:00.000Z",
  "2023-058T12:56:00.000Z",
  "2023-058T13:00:00.000Z",
  "2023-058T13:04:00.000Z",
  "2023-058T13:08:00.000Z",
  "2023-058T13:12:00.000Z",
  "2023-058T13:16:00.000Z"
]
```



<h4>To find information about a specific epoch, include the information after </h4>epoch. Here is an example using 2023-063T11:55:00.000Z

```
curl localhost:5000/epochs/2023-063T11:55:00.000Z
```
This returns

```
{
  "EPOCH": "2023-063T11:55:00.000Z",
  "X": {
    "#text": "1177.59304662879",
    "@units": "km"
  },
  "X_DOT": {
    "#text": "5.8075028706235097",
    "@units": "km/s"
  },
  "Y": {
    "#text": "-5851.2024874564004",
    "@units": "km"
  },
  "Y_DOT": {
    "#text": "-1.4895857081331501",
    "@units": "km/s"
  },
  "Z": {
    "#text": "3241.2823555820801",
    "@units": "km"
  },
  "Z_DOT": {
    "#text": "-4.7739619170779601",
    "@units": "km/s"
  }
}
```

<h4>To find the speed at that location, add /speed to the end.</h4> 

Here is an example continuing the one from before.

```
curl localhost:5000/epochs/2023-063T11:55:00.000Z/speed
```
Output 

```
{
  "speed": 7.663985096533364
}
```

<h4>To get help on different methods, run</h4>

```
curl localhost:5000/help
```
This will return
```
[1]+  Done                    curl localhost:5000/epochs?limit=20

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
        
    POST /post-data
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
```

<h4>To delete the data</h4>
Run

```
curl -X DELETE localhost:5000/delete-data
```
This will return

```
All data has been deleted successfully.
```
confirming that the data was deleted.


<h4>To recover that data</h4>
run
```
curl -X POST localhost:5000/post-data
```
This wil return
```
All data has been updated successfully.
```
This confirms that the data was restored and the other methods will work.





<h4>To return the comment list object</h4>
run

```
curl localhost:5000/comment
```

This should return something like this

```
[
  "Units are in kg and m^2",
  "MASS=473291.00",
  "DRAG_AREA=1421.50",
  "DRAG_COEFF=2.80",
  "SOLAR_RAD_AREA=0.00",
  "SOLAR_RAD_COEFF=0.00",
  "Orbits start at the ascending node epoch",
  "ISS first asc. node: EPOCH = 2023-03-08T12:50:10.295 $ ORBIT = 2617 $ LAN(DEG) = 108.61247",
  "ISS last asc. node : EPOCH = 2023-03-23T11:58:44.947 $ ORBIT = 2849 $ LAN(DEG) = 32.65474",
  "Begin sequence of events",
  "TRAJECTORY EVENT SUMMARY:",
  null,
  "|       EVENT        |       TIG        | ORB |   DV    |   HA    |   HP    |",
  "|                    |       GMT        |     |   M/S   |   KM    |   KM    |",
  "|                    |                  |     |  (F/S)  |  (NM)   |  (NM)   |",
  "=============================================================================",
  "GMT067 Reboost        067:19:47:00.000             0.6     428.1     408.4",
  "(2.0)   (231.1)   (220.5)",
  null,
  "Crew05 Undock         068:22:00:00.000             0.0     428.7     409.6",
  "(0.0)   (231.5)   (221.2)",
  null,
  "SpX27 Launch          074:00:30:00.000             0.0     428.3     408.7",
  "(0.0)   (231.2)   (220.7)",
  null,
  "SpX27 Docking         075:12:00:00.000             0.0     428.2     408.6",
  "(0.0)   (231.2)   (220.6)",
  null,
  "=============================================================================",
  "End sequence of events"
]
```

<h4>To return the header as a dictionary </h4>
run
```
curl localhost:5000/header
```
This should return something like this
```
{
  "CREATION_DATE": "2023-067T21:02:49.080Z",
  "ORIGINATOR": "JSC"
}
```

<h4>To return the metadata dictionary form the ISS data</h4>
run

```
curl localhost:5000/metadata
```

This should return something like this

```
{
  "CENTER_NAME": "EARTH",
  "OBJECT_ID": "1998-067-A",
  "OBJECT_NAME": "ISS",
  "REF_FRAME": "EME2000",
  "START_TIME": "2023-067T12:00:00.000Z",
  "STOP_TIME": "2023-082T12:00:00.000Z",
  "TIME_SYSTEM": "UTC"
}
```

<h4>To return a specific location taken from the curl</h4>
run

```
curl localhost:5000/epochs/<epoch>/location
```

Here is an example using "2023-082T12:00:00.000Z" 

```
{
  "alt": 426.493361256541,
  "geoloc": "Over the ocean",
  "lat": 3.693612400678767,
  "lon": 59.77071661260687
}
```

<h4> To return a dictionary of the information about the latest recording of the ISS</h4>
run

```
curl localhost:5000/now
```

Here is an example output

```
{
  "closest_epoch": "2023-068T18:52:17.828Z",
  "geoloc": "over the ocean",
  "location": {
    "alt": 422.4791789333376,
    "lat": 27.25115813046933,
    "lon": -174.3411771471322
  },
  "seconds from now": 11.438713312149048,
  "speed": 7.663538333123568
}
```