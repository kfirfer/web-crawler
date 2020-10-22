#### Get started

Run [main](./webcrawler/__main__.py) 

#### Docker make commands

You can display available make commands using `make`.

While developing, you will probably rely mostly on `make services`; however, there are additional scripts at your disposal:

| `make <script>`      | Description                                                                  |
| -------------------- | ---------------------------------------------------------------------------- |
| `help`               | Display available make commands                                              |
| `start`              | Run all services.                                                            |
| `stop`               | Stop all services.                                                           |
| `remove`             | Stop & Remove volumes of all services.                                       |
| `services`           | Run main services except the server.                                         |
| `server.daemon`      | Run your local server in its own docker container as a daemon.               |



# Troubleshooting
For ubuntu You should install those packages:
```bash
sudo apt-get install libmysqlclient-dev default-libmysqlclient-dev python3 python-dev python3-dev build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev python-pip # Debian / Ubuntu
```