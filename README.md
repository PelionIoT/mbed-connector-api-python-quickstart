# mbed-connector-python-quickstart
This is a quickstart application for the [mbed-connector-python](https://github.com/armmbed/mbed-connector-python) package. 
The goal of this application is to get the user up and running, using the mbed-connector-python package and talking to devices through mbed Device Connector in under 5 min, 5 steps or less.
The quickstart webapp is meant to be paired with the [quickstart embedded app](TODO). The quickstart web app will allow the user to visualize quickstart embedded devices and interact with them. 

### Pre-requisites
This quickstart assumes you already have a [mbed connector](www.connector.mbed.com) account and have generated an API token and have a device registered on your domain. 


This application uses the following python packages, make sure to install them before using the quickstart.
* **web.py** - python web framework for serving web pages - `pip install web.py`
* **socketio** - simple websockets for realtime results - `pip install python-socketio`
* **pybars** - handlebar templates - `pip install pybars`
* **mdc-api** - mbed Device Connector REST interface in python - `pip install mdc_api`

### Use
1. Put your [API key](https://connector.mbed.com/#accesskeys) into the app.py file, replace the following text
    ```python
    token = "Change Me" # replace with your API token
    ```
2. Run the `app.py` file
    ```python
    python ./app.py
    ```
3. Open a web page to the web.py server.
4. Interact with the web page, blink the LED's, subscribe to the resources, click the button on the board and see the numbers tick up on the web app.
    {{TODO: insert gif's here}}
5. Modify : go checkout the API for the [mbed-connector-python library](TODO) and make your own applications!

