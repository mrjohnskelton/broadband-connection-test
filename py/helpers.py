import os
import json
import datetime
import pyppeteer
import requests
import uuid
import const  # for graphql queries
import platform


def getPwd():
    # Get current directory in cross-platform safe way
    return os.path.dirname(os.path.realpath(__file__))


# If local config does not exist then open alternative
def getConfig():
    pwd_ = getPwd()
    # get directory seperator in cross-platform safe way
    sep = os.path.sep
    # Construct file path to config using join
    filePath = ''.join([pwd_, sep, 'config.local.json'])
    # Check if file exists
    if not os.path.isfile(filePath):
        filePath = ''.join([pwd_, sep, 'config.json'])
    # Load config from json file
    with open(filePath) as json_file:
        config = json.load(json_file)  # Load config from json file
    return config


# Return ISO 8601 formatted date
def getTimestamp():
    return datetime.datetime.now().isoformat()


# Use pyppeteer to extract an element from a web page
async def getStatus(url):
    try:
        if platform.system().lower() == 'windows':
            # Create a browser
            browser = await pyppeteer.launch()
        else:
            from selenium import webdriver
            browser = webdriver.Chrome(
                executable_path='/usr/lib/chromium-browser/' +
                'chromedriver-v2.21-linux-armv7l')
            # Create a browser
            browser = await pyppeteer.launch()
            # Create a new page
            page = await browser.newPage()
            # Navigate to url
            await page.goto(url)
            # Get the status of the page
            selector = "#status_tile > ul > .ng-binding"
            # Extract element using selector
            element = await page.querySelector(selector)
            if element:
                status = await page.evaluate(
                    '(element) => element.innerText', element)
            else:
                status = 'Unknown'
            # Close the browser
            await browser.close()
            return status
    except Exception as e:
        print(e)
        return 'Error'


# Get globally unique identifier
def getGuid():
    return str(uuid.uuid4())


# Save to file as couldn't send to API
def saveToFile(output):
    # Get config
    config = getConfig()
    # Get directory seperator in cross-platform safe way
    sep = os.path.sep
    pwd_ = getPwd()
    # Construct file path to config using join
    filePath = ''.join([
          pwd_, sep,
          config['failToSendPath']])
    # Check if dir exists
    if not os.path.isdir(filePath):
        # If not then create it
        os.makedirs(filePath)
    # Save to file
    with open(''.join([
            filePath, sep, output['uuid'], '.json']), 'w') as outfile:
        json.dump(output, outfile)


# Get list of files in directory
def getFileList():
    # Get config
    config = getConfig()
    # Get directory seperator in cross-platform safe way
    sep = os.path.sep
    pwd_ = getPwd()
    # Construct file path to config using join
    filePath = ''.join([
          pwd_, sep,
          config['failToSendPath']])
    # Check if dir exists
    if not os.path.isdir(filePath):
        # Return empty list
        return []
    # Return list of files in directory
    return os.listdir(filePath)


def logOutput(output):
    # Get config
    config = getConfig()
    # check if key exists in dict
    if 'logToFile' in config and config['logToFile']:
        return logToFile(config, output)
    else:
        return logToAPI(config, output)


def logToFile(config, output):
    try:
        # Get directory seperator in cross-platform safe way
        sep = os.path.sep
        pwd_ = getPwd()
        # Construct file path to config using join
        filePath = ''.join([
              pwd_, sep,
              config['logToFilePath']])
        # Check if dir exists
        if not os.path.isdir(filePath):
            # If not then create it
            os.makedirs(filePath)
        # Get time in YYYYmmDD format
        time = datetime.datetime.now().strftime("%Y%m%d")
        filename = ''.join([
            filePath, sep, time, '.csv'])
        # Remember if we need to write headings
        writeHeadings = not os.path.isfile(filePath + sep + time + '.csv')
        # Save to file
        with open(filename, 'a') as outfile:
            if writeHeadings:
                outfile.write(','.join(output.keys()) + '\n')
            # Convert JSON to csv - assumes keys alsway parsed in same sequence
            # if this turns out not to be the case then try
            # dict(sorted(d.items())).keys() and .values()
            outfile.write(','.join(output.values()) + '\n')
        return True
    except Exception as e:
        print(e)
        return False


# Post output to AWS API over http
def logToAPI(config, output):
    ###
    # Post individual results
    try:
        variable = {}
        variable['data'] = output
        request = requests.post(
            config['endpoint']['url'],
            json={
              'query': const.getGraphQLMutation(),
              'variables': variable
            },
            headers=config['endpoint']['headers']
            )
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception(
                "Query failed to run by returning code of {}. {}"
                .format(request.status_code, const.getGraphQLMutation()))
    except requests.exceptions.SSLError:
        print('No internet connection?')


# Post output to AWS API over http
def logToAPI2(config, output):
    # Get url
    url = config['endpoint']['url']
    # Get headers
    headers = config['endpoint']['headers']
    # Send data to API
    try:
        response = requests.post(url, headers=headers, data=json.dumps(output))
        # Check if response is successful
        if response.status_code == 200:
            # If successful then return true
            return True
        else:
            # If unsuccessful then return false
            return False
    except Exception as e:
        print(e)
        # If exception then return false
        return False
