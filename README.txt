The functionality of this project is split into two sections the Ionic and Python apps.

Installation of Python:
    Raspberry Pi:
        Open up a new terminal
        sudo apt-get update
        sudo apt-get upgrade 
        sudo apt-get install git
        git clone https://github.com/jmeolmsted/project-white-cane.git
        curl -kL dexterindustries.com/update_grovepi | bash
        cd project-white-cane/scr/assets/
        sudo pip install picamera
        sudo pip install flask_restful
        sudo pip install flask_jsonpify
        sudo pip install flask_cors
        sudo pip install flask
        mkdir laser
        cd laser
        git clone https://github.com/sparkfun/Qwiic_VL53L1X_Py 
        cd Qwiic_VL53L1X_Py 
        mv * ../
        cd ..
        git clone https://github.com/sparkfun/Qwiic_I2C_Py.git
        cd Qwiic_I2C_Py/qwiic_i2c
        mv * ../../ 
        git clone https://github.com/tutRPi/Raspberry-pi-Heartbeat-Pulse-Sensor
        cd Raspberry-Pi-Heartbear-Pulse-Sensor/
        mv * ../
        sudo apt-get install python-dev
        sudo raspi-config
        select "Interfacing Options"
        select "SPI"
        select "Yes"
        select "ok"
        if prompted to reboot select yes if not run sudo reboot
        open a new terminal 
        cd project-white-cane/src/assets
        wget https://github.com/doceme/py-spidev/archive/master.zip
        sudo apt install unzip
        unzip master.zip
        cd py-spidev-master
        sudo python setup.py install

        

Installation of Ionic:
    Windows:
        Download and Install Node.js from https://nodejs.org/en/
        Open the control Panel
        Click User Accounts twice
        Click Change my environment variables
        Select Path, from variables
        Add ;C:\textbackslash Program Files\textbackslash nodejs\textbackslash to the end of your Path variable on the "User variable" section of 
        the Environment Variables on the
		System Properties
        Open a command terminal as administrator
        Run npm install -g cordova ionic 
        cd to where you want to place the app: cd folder
        Run git clone https://github.com/jmeolmsted/project-white-cane.git
        cd into app folder
        Run npm install
        Run npm audit fix (if prompted to do so)
        Run npm update (if you see nothing happen after hitting enter that is fine)
    Mac:
        Download and Install Node.js from https://nodejs.org/en/
        Open a command terminal
        Run sudo npm install -g cordova ionic
        Run git \texttt{-{}-}version 
        If you don't already have git installed you will be prompted to at this point do so.
        Run git clone https://github.com/jmeolmsted/project-white-cane.git
        cd into app folder
        Run sudo npm install
        Run sudo npm audit fix (if prompted to do so)
        Run sudo npm update (if you see nothing happen after hitting enter that is fine)

    Linux:
        Open a command terminal
        Run sudo apt-get install nodejs
        Run npm install -g cordova ionic
        Run git clone https://github.com/jmeolmsted/project-white-cane.git
        cd into app folder
        Run sudo npm install
        Run sudo npm audit fix (if prompted to do so)
        Run sudo npm update (if you see nothing happen after hitting enter that is fine)

Run Application:
    Begin on the Raspberry Pi by openning a terminal
    cd into project-white-cane
    Run python src/assets/filework.py
    Moving to the computer
    Open a terminal
    cd into project-white-cane
    Run ionic serve

Python Functionality:
    The python code uses the grove pi libraries and some libraries specific to the IR sensor and heart rate sensor to read in the data.
    This data is then processed and sent to a flask server to be accessed by our Ionic web app.
    The main file is filework.py, the name originally deriving from the fact that this was initially planned to send just the name of image files
    to the flask server, but as the project developed we found that we were able to send all of the necessary information through this same code.
    Looking more indepth the code can be split into sections:

        Imports:
            picamera this library is needed for the PiCamera object so that the camera can take pictures
            grovepi the libraries to work with the grovepi devices
            flask_restful this library allowed us to create an api to send and recieve data from
            flask_jsonpify allows the conversion of information into the correct format
            flask_cors allowed the flask server to be sent beyond just the Raspberry pi
            flask allowed the creation of the flask server
            os.path allowed us to check the directory for files and read in all of the image filenames
            os makes placing files and locating them much simpler
            multiprocessing as we move forward this will be useful in creating parallel processes to hopefully make the program run smoother
            json for helping to put data into the json format
            pulsensor library needed to the PulseSensor object for reading in the heart rate
            datetime needed for creating the name of the image files by reading in the current date and time
            webbrowser as we move forward this will allow for the webapp to be opened on the Raspberry Pi as part of starting the program for 
            smoother integration
            time needed to set the wait time for certain readings to give the sensors time to wake up
            socket used to get the ip address of the pi so that the flask server can be made externally accessible
            signal this library is needed to properly shutdown multiprocessing functions
            qwiic_vl53lx needed for the IR sensor
        
        Pin Numbers: 
            This section sets the variable for the pin numbers of the sensors for the grovepi calls that need them
        
        IP address:
            This section uses the socket library to collect the ip address of the Raspberry Pi and stores is as a variable

        Data Formatting:
            makeEntry: converts the file number and file name into a json entry to be sent to the filename storage on flask
            makeData: formats the values read in by the sensor into one data package to be sent to the data storage on flask
        
        Data Collection:
            getData: This function reads in the values from all of the sensors we were able to get working at one time and places them into the format the flask server is expecting
            getImages: This function reads in all of the image filenames and prepars this information to be sent to the flask server

        Flask Server:
            This section creates and sets the commands for the flask server
            app: The variable name for the server
            api: The variable name for the api of the flask server

            class Files(Resource): This creates the files resource object with the getImages function as the response when the Ionic web app sends 
            a request
            class Data(Resource): This creates the data resource object with the getData function as the response when the Ionic web app sends a 
            request

            api.add_resource: These lines create the specific address that the Files and Data resources are stored at

        Data Processing:
            This section handles the data read by the sensors and the response of the actuators based on those readings
            takeImage: Looks at the front ultra sonic rangers and the IR sensor data and takes a picture if any of their threshold is met, this 
            image is stored in the project-white-cane/src/assets/images folder
            irDist: This reads the distance from the IR sensor and is called by the getData function  
            getHeart:  Collects the data from the heart rate sensor will be called by getData function in the future
            irConverter: Converts the IR sensor data from mm to feet
            Converter: Converts the ultra sonic ranger data from cm to feet
        
        Proccesses for multiprocessing:
            This section sets functions to be called to start up the parallel processes when we implement them in the future
            runFile: This starts up the flask server at the Raspberry Pi ip address
            funIonic: This starts up the Ionic web app, this currently is not able to be done on the pi 
            openWeb: Opens the Ionic web app on the external page based on the ip address of the pi this will be used to help make the operation of 
            the device smoother

            main: This function creates the pool of processes and starts them up with the command that kills them all when the keyboard interrupt 
            is sent

        Running the app:
            runFile: Starts the flask server
            digitalWrite: turns off the vibration motor when the flask server is stopped

Python Location:
    The python files were placed in project-white-cane/src/assets as by the standard for Ionic the python code is an asset that allows the web app
     to function. In addition because the images for display on the ionic server are to be placed in the assets/images folder it makes the most
     sense to place the python code in the assets directory for ease of file placement and retrieval. The python code is run from the Raspberry Pi 
     as it is what is used to collect sensor data and send the response to the actuators.
    

Ionic Functionality:
    This Ionic code is what creates the web app for the end user to interact with and displays the data from the python code.
    The Ionic code can be split into sections for functionality:
        app:
            This section contains the pages that creates the app and its functionality
            This also contains the files that set the look and necessary modules for the app and creates the app
            explore-container: This creates the formatting for the pages of the app
            images: This is the page that reads and displays the images and file names to the user and shows specific obstacle warnings
            sensors: This is the page that reads and displays the sensor data and whether there is a warning trigger from a specific sensor
            services: This contains services used by the app pages for translating data into usable formats
                images: Converts the response from clicking on a filename by the user into the correct filename to display the selected image
                sensors: Converts the response from the flask server for the sensor data into a usable format for the web app
            tabs: This controls the naviation of the web app allowing it to use a tabular formatting for the navigation

Ionic Location:
	The Ionic app folders and files were placed automatically where they are needed for the Ionic app to funciton as they were generated through
    the terminal commands. This allows ease in creating the application as the formatting is smooth and handled by the language itself. Currently 
    the Ionic app is run through the computer as the Raspberry Pi is unable to handle the processing necessary to launch the Ionic App. In the 
    future we hope to have the device that runs the python code also be able to run the Ionic code as this would make the display of images to the 
    user much simpler as the new image file would not need to be sent to a new device. 



        