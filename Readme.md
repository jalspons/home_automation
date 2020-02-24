Home automation system
======================
------

## 1. Introduction

* Automation system for the cottage
* No Internet connection
* Idea is to develop a cost-effective method for controlling the heating system

#### 1.1 Messaging

Messages ():
{   
    'recipier': _                       # String    *required
    'request_type': _,                  # String    *required
    'outlet_data': {                    # 
        '_': {                          # Char (outlet_id)
            'activation_time': _,       # Timestamp (seconds)
            'deactivation_time': _,     # Timestamp (seconds)
            'status': _,                # Boolean (Active)
        },
        '_': { ... },
        ...
    }
}

## 2. Concept

The project consists of three separate parts:
* A cloud server with an user interface
* A local server on the node (e.g. a raspberry pi)
* An outlet manager to control the heateners

### Gear
* A raspberry pi
* Remote controlled outlets
* WiFi connection (e.g. 4G Hotspot)

## 3. Cloud Server 

`The cloud server gathers the data and brings the system open for the users.`  

### UI
* Authentication
* Dashboard with controls for each outlet

### Communication

Local Server <--- Websocket ---> Cloud server <--- HTTPS (Django app) ---> User

### Libraries
* Python3
* Python3 websockets
* Django 2

## 4. Local Server

`The local server act as the message passing interface. The interface is located at the local node in order to minimize computation performed at the cloud and to allow gathering data into a bigger chunks. `

### Services
* Server: Deliver user input
* Visualize 
* Inventory follow-up
* Temperature level settings
* Weather info

### Tech

* Python3 
* Python3 Asyncio
* Python websockets

## 5. Outlet Manager
`Outlet manager is a program running on a local node. It has the access for controlling the outlets. The Outlet Manager is independent from the local server to increase the reliability. When the server crashes, the outlets are still under control and turned off eventually.`

### Services
* On / Off switches for outlets
* Timers for activating outlets

### Tech
* Python3
* RPi.GPIO library

# The future

## 6. Data Collectors
### Services
* Server: POST-messages in every 15 minutes and receive control parameters
* Sensors: Adjust according to control parameters

### Components
* Microcontrollers for data collection
* 4G hotspot
* Humidity & Temperature:  DHT22 sensor
* Cameras?
* 5V Relays
* LEDs

## 7. Open data
* Data resources to support the system, e.g. local weather data
