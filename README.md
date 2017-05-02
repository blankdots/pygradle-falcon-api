# PyGradle Falcon REST API

Example of of building a Falcon REST API using PyGradle (using python-web-app plugin). The functionality of the API is minimal has the following endpoints:
* `index` - registers data sent via POST in a SQLite3 Database;
* `health` - checks if the application is running.

## Building and Running the application

### Requirements
1. Python 2.7
2. Gradle 3.0+ https://gradle.org/
3. Pypi Ivy repository either a local one (see https://github.com/linkedin/pygradle/blob/master/docs/pivy-importer.md for more information) or you can deploy your own version using https://github.com/blankdots/ivy-pypi-repo


### Building the application

After all the requirements are satisfied in the root directory run `gradle build`

### Running the application

To use the deployable artifact after build run `./build/deployable/bin/gunicorn webapp.webapi:webapp`

To deploy the artifact on your a server unzip `build/distributions/pygradle-falcon-api-1.0.tar.gz` on one's server and run using `./gunicorn webapp.webapi:webapp` (the options for gunicorn can be added to command such as port number `./build/deployable/bin/gunicorn webapp.webapi:webapp -b 127.0.0.1:4300` )

Example of requests:

```
curl -X POST \
  http://localhost:8000/0.1/index/ \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -d '{
  "author": "random author",
  "data": "Some random data."
}'
```

```
curl -X GET \
  http://localhost:8000/health \
  -H 'cache-control: no-cache'
```
