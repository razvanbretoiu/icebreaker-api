# icebreaker-api

### Setup

1. Install [pipenv](https://pypi.org/project/pipenv/)
2. ``pipenv shell`` (to activate the virtual environment)
3. ```pipenv install``` (to install the dependencies)
4. ``python ./src/endpoints.py`` to start the local server

### Deploy

The deployment is done using [Cloud Run](https://cloud.google.com/run) service from Google Cloud Platform.

To deploy new version, just push the code on `main` branch. 

This is the API url:

https://api-xx5alou65q-ey.a.run.app
