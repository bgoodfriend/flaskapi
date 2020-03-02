# flaskapi
This repo is a proof of concept for creating an API.

This implementation allows GET/PUT to an array of buckets, and a GET or POST query to check those buckets against a requested time range.

This solution was created using Python: Flask, datetime, pytz (time zones).

Metrics were added using [prometheus-flask-exporter](https://pypi.org/project/prometheus-flask-exporter/).

I added a static swagger.json and exposed it with [flask-swagger-ui](https://github.com/sveint/flask-swagger-ui)https://pypi.org/project/prometheus-flask-exporter/).

## Installation
Acquire flaskapi, either from a zip, or via private repo.

```
[root@localhost ~]# git clone git@github.com:bgoodfriend/flaskapi.git
Cloning into 'flaskapi'...
remote: Enumerating objects: 41, done.
remote: Counting objects: 100% (41/41), done.
remote: Compressing objects: 100% (27/27), done.
remote: Total 41 (delta 19), reused 29 (delta 10), pack-reused 0
Receiving objects: 100% (41/41), 21.12 KiB | 1.17 MiB/s, done.
Resolving deltas: 100% (19/19), done.
```

Build and deploy a docker image.
To do this, you must select a port to serve the API to.  The following serves to port 5000 on localhost

```
[root@localhost ~]# cd flaskapi
[root@localhost flaskapi]# docker build -t flaskapi .
Sending build context to Docker daemon  125.4kB
[...]
[root@localhost flaskapi]# docker run -d -p 5000:5000 flaskapi
558d8420b5aa7b6d883364bfdbf073032741cdcc337e16c8bbeccb0c0c8947d5
```
The container should now be serving the API.  A quick way to confirm this is to hit the API root and confirm a response:
```
[root@localhost flaskapi]# curl http://127.0.0.1:5000/
<h1>Bob Goodfriend Flask API proof of concept</h1>
```

## Usage

A complete Swagger doc is available at {{URL}}/static/swagger.json, eg http://127.0.0.1:5000/static/swagger.json.

The API also exposes a GUI version of its swagger doc at {{URL}}/swagger, eg http://127.0.0.1:5000/swagger.

As indicated in that doc, additional endpoints are exposed at /rates, /setrates, /query-rate, and /metrics.

## Testing and Examples
The worst part of my implementation is that I don't yet have Python unit tests.  Therefore, the best way to test the app is with smoke testing (examples).

There are 3 ways to test via example.

### Testing via /swagger

The API's Swagger UI at /swagger allows you to directly inject HTTP requests and see the results.  It even shows you the actual curl it crafted.

For example, from {{URL}}/swagger, click on "GET /rates", then "Try it out", then "Execute".  This will show you that it ran `curl -X GET "{{URL}}:5000/rates" -H "accept: */*"`, and it got back a 200 response with the current rate table.



