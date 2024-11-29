# Fastapi Starter Kit

## Description

This is a starter template for creating a service using fastapi, this service uses pymongo as an intermediary for connecting to a No-SQL database (Mongo), there is also a model, response, middleware which according to the developer is good enough.

if there is something that needs to be added or there are shortcomings, you can open an issue in this repository.

## Prerequisites

Before starting the application, let's install the libraries needed first in the following way

if you have poetry installed, run the following command:
```bash
poetry install
```

or using pip:
```bash
pip install -r requirements.txt
```

### Testing

To test whether the module runs properly
```bash
python -m pytest test/test_module.py
```
for testing other than `test/test_module.py`. required so that the api is already running first. If the service is already running, you can immediately do overall testing

```bash
python -m pytest
```

## Contributors

[//]: contributor-faces

<a href="https://github.com/oktapiancaw"><img src="https://avatars.githubusercontent.com/u/48079010?v=4" title="Oktapian Candra" width="80" height="80" style="border-radius: 50%"></a>

[//]: contributor-faces
