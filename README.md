# mbed-connector-python-quickstart
This is a quickstart application for the [mbed-connector-api-python](https://github.com/armmbed/mbed-connector-api-python) package. 
The goal of this application is to get the user up and running, using the mbed-connector-python package and talking to devices through mbed Device Connector in under 5 min, 5 steps or less.
The quickstart webapp is meant to be paired with the [quickstart embedded app](https://github.com/ARMmbed/mbed-client-quickstart). The quickstart web app will allow the user to visualize quickstart embedded devices and interact with them. 

### Pre-requisites
- A [mbed connector](https://www.connector.mbed.com) account and have generated an API token
- A endpoint running the [mbed client quickstart example]()
- Install the required packages `pip install -r requirements.txt`

### Use
1. Put your [API key](https://connector.mbed.com/#accesskeys) into the app.py file, replace the following text
    ```python
    token = "Change Me" # replace with your API token
    ```
    or set an evironment variable called `ACCESS_KEY` with the value of your API key
2. Run the `app.py` file
    ```python
    python ./app.py
    ```
3. Open a web page to the web.py server. Usually [//localhost:8080](//localhost:8080) will work. 
4. Interact with the web page, blink the LED's, subscribe to the resources, click the button on the board and see the numbers tick up on the web app.
    {{TODO: insert gif's here}}
5. Modify : go checkout the API for the [mbed-connector-api-python library](https://docs.mbed.com/docs/mbed-connector-api-python/en/latest/) and make your own applications!

