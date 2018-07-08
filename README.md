# Autocomplete Web Service

Flask based web service that suggests words starting with a given prefix. The words are obtained from a pre-configured corpus text file. This was implemented in the context of [a python challenge](https://github.com/Aptoide/python-challenge).

**DISCLAIMER**: This web service can be unsuitable for big corpus, once it loads them entirely in memory.

## Requirements

This web service has the following dependencies:

- [Flask](http://flask.pocoo.org/)
- [pygtries](https://github.com/google/pygtrie)

Install them in your environment before running the server. You can use the requirements file at the root of the project:

`pip install -r requirements.txt`

## Configuration

The web service is configured using the following environment variables:

- `CORPUS_PATH`: The path for the corpus text file. It should be a list of words, one by line.

Set the configurations variable before running the server:
`export CORPUS_PATH=<corpus_file_path>`

## Execution

To run the server:

1.  Set the flask application module, which is implemented in the `flaskr` directory: `export FLASK_APP=flaskr`.

2.  Run the flask application: `flask run`.

## API

The web service provides the following end-point.

`GET /suggestions`

###### Query Parameters

`q` - prefix for the suggestions be be obtained.
`limit` - number of results to be obtained.
`offset` - position of the first result to be obtained from all suggestions.

###### Response

The response is a `application/json` with the following keys.

`total` - total number of suggestions for the given prefix.
`limit` - number of results being presented.
`offset` - position of the first result from all suggestions.
`next` - URL for the next page of results.

###### Example

Request:

`GET /suggestions?q=F&limit=10&offset=10`

Response:

```json 
{
    limitl : 10,
    next: "suggestions?limit=10&offset=20",
    offset: 10,
    results: [
        "FaceApp",
        "FaceLock for apps",
        "FaceLOOK for Facebook",
        "Facetune",
        "FaceSwap Face Swap Live",
        "Fast Racing 3D",
        "Fast Reboot",
        "Fast Download Manager",
        "Fast Followers",
        "Fast Facebook Video Downloader",
    ],
    total: 393
}
```

## Tests

All unit tests can be run using _pytest_ from the project's root directory.

`pytest`