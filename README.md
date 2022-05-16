# came-connect

A Python library/Web Server to use Came Connect for home automation purposes such as automating the control of gates via Home Assistant.

The library lets you authenticate with the Came Connect service, and view the status of devices, issue commands or return the status of inputs.

It was designed with usage of a CAME Ethernet Gateway (RETH001) and associated RF slave (RSLV001) in mind.

It can be used as a CLI, via `cli.py`.

Running `main.py` will start a local RESTful web server, that you can interact with using. This web server can be used with, for example, Home Assistant's [RESTful command](https://www.home-assistant.io/integrations/rest_command/) integration to trigger automations with Gates etc.

## Docker

### Build
`docker build -t jasonmadigan/came-connect .`

## Install Deps

`pipenv install`


## Pre-reqs

You need to setup some environment variables to run both the CLI and the web server.

You need to fetch two values from the Came Connect login page. To get:
- Visit https://www.cameconnect.net/login
- View the source of https://www.cameconnect.net/main.XXX.js
- Search for `clientId` - this will be your `CAME_CONNECT_CLIENT_ID` value
- Search for `clientSecret` - this will be your `CAME_CONNECT_CLIENT_SECRET` value

| Env Var   |      Are      |
|----------|-------------|
| `CAME_CONNECT_CLIENT_ID` |  See above |
| `CAME_CONNECT_CLIENT_SECRET` | See above  |
| `CAME_CONNECT_USERNAME` | Username for the https://www.cameconnect.net portal |
| `CAME_CONNECT_PASSWORD` | Password for the https://www.cameconnect.net portal |


## Run

`pipenv run python main.py --help`


```
docker run -p --rm 9002:8080 --name=came-connect -e CAME_CONNECT_CLIENT_ID=xxx -e CAME_CONNECT_CLIENT_SECRET=xxx -e  CAME_CONNECT_USERNAME=xxx -e CAME_CONNECT_PASSWORD=xxx jasonmadigan/came-connect:latest
```


## Commands

In the examples below, we have a RSLV001 slave device (with an example ID: 11111), with two outputs configured - one for closing a gate (command ID: 2), one for opening it (command ID: 5). Triggering these outputs on cameconnect.net, with an eye on the Dev Tools console in your browser of choice, we can get the ID of these specific commands. Our `came-connect` container is running on 192.168.1.100.

### Read sites

TODO

### Fetch Device statuses

TODO

### Run device commands

`curl http://192.168.1.100:9002/devices/<device_id>/command/<command_id>`

You can get the device or command IDs by triggering these outputs while on cameconnect.net, with a network tab open in your browser.

### Example Home Assistant integration

```
# configuration.yaml

rest_command:
  gate_open:
    url: "http://192.168.1.100:9002/devices/<device_id>/command/5"
    method: GET
  gate_close:
    url: "http://192.168.1.100:9002/devices/<device_id>/command/2"
    method: GET
```
