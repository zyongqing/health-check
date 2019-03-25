# Remote Host Health Check Tools

This is a basic framework for remote host health check.

## Commands

```bash
usage: run.py [-h] [--port PORT] [--verbose]
              host username password {windows,linux}

health check

positional arguments:
  host             host name
  username         host username
  password         host password
  {windows,linux}  host platform

optional arguments:
  -h, --help       show this help message and exit
  --port PORT      host port
  --verbose        debug mode
```
