# flaskapi
This repo is a proof of concept for creating an API.

This implementation allows GET/PUT to an array of buckets, and a GET or POST query to check those buckets against a requested time range.

This solution was created using Python: Flask, datetime, pytz (time zones).

Metrics were added using [prometheus-flask-exporter](https://pypi.org/project/prometheus-flask-exporter/).

I added a static swagger.json and exposed it with [flask-swagger-ui](https://github.com/sveint/flask-swagger-ui)https://pypi.org/project/prometheus-flask-exporter/).

## Manifest
Entrypoint is app.py.  rates.py is broken out to separate it from the Flask functionality.

```
.
├── app.py
├── Dockerfile
├── LICENSE
├── rates.py
├── README.md
├── requirements.txt
└── static
    └── swagger.json
```
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

The worst part of my implementation is that I don't yet have Python unit tests.
The best way to test the app is with smoke testing (Examples).  
Here are 3 different ways to test via Exmaple.

### Testing via /swagger

The API's Swagger UI at /swagger allows you to directly inject HTTP requests and see the results.  It even shows you the actual curl it crafted.  

For example, from {{URL}}/swagger, click on "GET /rates", then "Try it out", then "Execute".  This will show you that it ran `curl -X GET "{{URL}}:5000/rates" -H "accept: */*"`, and it got back a 200 response with the current rate table.

### Testing via curl

All of the following should work from the command line.  These examples assume you did not change the default values from host:localhost (127.0.0.1) and port:5000.

Get current rates:
```
[root@localhost flaskapi]# curl "http://127.0.0.1:5000/rates/"
[{"days":"mon,tues,thurs","price":1500,"times":"0900-2100","tz":"America/Chicago"},{"days":"fri,sat,sun","price":2000,"times":"0900-2100","tz":"America/Chicago"},{"days":"wed","price":1750,"times":"0600-1800","tz":"America/Chicago"},{"days":"mon,wed,sat","price":1000,"times":"0100-0500","tz":"America/Chicago"},{"days":"sun,tues","price":925,"times":"0100-0700","tz":"America/Chicago"}]
```

Rate queries via GET:
```
[root@localhost flaskapi]# curl "http://127.0.0.1:5000/query-rate?start_time=2015-07-01T07:00:00-05:00&end_time=2015-07-01T12:00:00-05:00"
1750
[root@localhost flaskapi]# curl "http://127.0.0.1:5000/query-rate?start_time=2015-07-04T15:00:00%2B00:00&end_time=2015-07-04T20:00:00%2B00:00"
2000
[root@localhost flaskapi]# curl "http://127.0.0.1:5000/query-rate?start_time=2015-07-04T07:00:00%2B05:00&end_time=2015-07-04T20:00:00%2B05:00"
unavialable
```

A rate query via POST:
```
[root@localhost flaskapi]# curl -X POST 'http://10.0.0.222:5000/query-rate'  --header 'Content-Type: application/json' --data-raw '{"start_time":"2015-07-01T07:00:00-05:00","end_time":"2015-07-01T12:00:00-05:00"}'
1750
```

Set rates to some new values. 
This example changes some time zones.  This is saved in memory, so this will change your query results!  Restarting the docker container will reload the defaults.
```
[root@localhost flaskapi]# curl -X PUT "http://127.0.0.1:5000/setrates" -H "accept: */*" -H "Content-Type: application/json" -d "{\"rates\":[{\"days\":\"mon,tues,thurs\",\"times\":\"0900-2100\",\"tz\":\"America/Chicago\",\"price\":1500},{\"days\":\"fri,sat,sun\",\"times\":\"0900-2100\",\"tz\":\"America/New_York\",\"price\":2000},{\"days\":\"wed\",\"times\":\"0600-1800\",\"tz\":\"America/Los_Angeles\",\"price\":1750},{\"days\":\"mon,wed,sat\",\"times\":\"0100-0500\",\"tz\":\"America/Chicago\",\"price\":1000},{\"days\":\"sun,tues\",\"times\":\"0100-0700\",\"tz\":\"America/Chicago\",\"price\":925}]}"
Thanks!
```

### Testing via Postman.

I mostly live tested via Postman on a Windows box, querying a bridged VM running my app.  To test via postman, first install from [Postman Install](https://www.postman.com/downloads/), then Import the file "flaskapi.postman_collection" from this repo's root.  

From there, you will need to define a global environment variable "base_url" set to your URL, eg "http://1270.0.1:5000".  

After that, you can run smoke tests vial the Postman GUI.  They are comparable to the above /swagger and cron tests.

## Metrics

Available at {{URL}/metrics.

