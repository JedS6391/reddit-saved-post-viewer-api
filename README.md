# Reddit saved post API

This project contains a web API for accessing reddit saved posts.

## Run

### Environment variables

The following environment variables are required by the API:

- `SECRET_KEY`: A secret key used for flask-session
- `CLIENT_ID`: The reddit client ID (must be obtained via [reddit](https://www.reddit.com/prefs/apps))
- `CLIENT_SECRET`: The reddit client secret (must be obtained via [reddit](https://www.reddit.com/prefs/apps))
- `REDIRECT_URI`: The reddit redirect URI (must be obtained via [reddit](https://www.reddit.com/prefs/apps))
- `SESSION_TYPE`: The type of session backend used by flask-session
- `APP_SETTINGS`: Which configuration object to use: `config.DevelopmentConfig` or `config.ProductionConfig`

The following environment variables are optional for the API:

- `WORKER_LOGGING_LEVEL`: Controls the logging level for the queue workers
- `NUMBER_OF_WORKERS`: Controls the number of queue workers

### Server

To run the main server, first populate any required environment variables, then start an application instance using `gunicorn`:

```
gunicorn main:app.app
```

To start the queue workers, simply execute:

```
python3 worker.py
```