#!/usr/bin/python

import socket, json, sys, httplib, datetime;

from xml.dom.minidom import parseString;
from urllib import urlencode;

apiURL = "api.prowlapp.com";
prowlKey = "9739ad3d982355711a879ba66cbf1d1642eae48a";

rabbitURL = "www.ltcrabbit.com"
rabbitID = 6351;
rabbitKey = "319b11ea3f9825bc5695a16f2ba9985264b48ca1eabd26376052361bb0229c92";

def sendNotification(name, event, description, priority = 0):
    # Construct arguments to the api
    args = {};
    args['apikey'] = prowlKey;
    args['priority'] = priority;
    args['application'] = name;
    args['event'] = event;
    args['description'] = description;

    # Headers for the POST request
    headers = {};
    headers['Content-type'] = 'application/x-www-form-urlencoded';

    # Construct the connection and send the request
    c = httplib.HTTPSConnection(apiURL);
    c.request("POST", "/publicapi/add", urlencode(args), headers); 
    resp = c.getresponse();

    # Record the transaction
    print datetime.datetime.now(), 'NOTIFY', resp.status, resp.reason;

    # Get the server's response
    root = parseString(resp.read()).firstChild;

    # Clean up the connection
    c.close();

    # Parse the response XML
    for elem in root.childNodes:
        if elem.nodeType == elem.TEXT_NODE: continue;
        if elem.tagName == 'success':
            return True;
        if elem.tagName == 'error':
            res = dict(list(elem.attributes.items()));
            return False;

def checkRabbit(threshold):
    args = {};
    args['page'] = 'api';
    args['action'] = 'getuserstatus';
    args['api_key'] = rabbitKey;
    args['id'] = rabbitID;

    # Make the Call
    c = httplib.HTTPSConnection(rabbitURL);
    c.request("GET", '/index.php?' + urlencode(args));
    resp = c.getresponse();

    # Record transaction
    print datetime.datetime.now(), 'CHECK', resp.status, resp.reason;

    # Get the data from the response and clean up
    data = json.loads(resp.read());
    c.close();

    # Handle the result of the request
    if 'getuserstatus' not in data:
        sendNotification('Rabbit', 'Failure', 'Invalid response.');
        return;

    if 'hashrate' not in data['getuserstatus']:
        sendNotification('Rabbit', 'Failure', "Didn't return hashrate.");
        return;

    if int(data['getuserstatus']['hashrate']) < threshold:
        sendNotification('Rabbit', 'Hashrate', "Hashrate fallen below " + str(threshold));
        return;

if __name__ == "__main__":
    checkRabbit(1000);
    sys.exit(0);

