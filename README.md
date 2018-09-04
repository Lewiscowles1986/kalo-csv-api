# Python REST API for sample CSV data

This is a coding challenge, it is not designed as a best-practice API

* CSV backing
* Python2 & 3 unittested
* Hypermedia Links in listings
* pip requirements

Improvements

* better repositories
* PUT / PATCH / POST support
* functional tests
* better code organisation
* use of blueprints
* os Environment vars for config (docker, heroku, CF)
* key hashing
* caching

Load testing

```
bombardier -c 500 -n 1000 -r 500 "http://localhost:5000/users"
bombardier -c 500 -n 1000 -r 500 "http://localhost:5000/users?page=1"
bombardier -c 500 -n 1000 -r 500 "http://localhost:5000/users?page=2"
bombardier -c 500 -n 1000 -r 500 "http://localhost:5000/users?page=3"
bombardier -c 500 -n 1000 -r 500 "http://localhost:5000/users?page=1&limit=20"
bombardier -c 500 -n 1000 -r 500 "http://localhost:5000/users?page=2&limit=20"
bombardier -c 500 -n 1000 -r 500 "http://localhost:5000/time/1"
bombardier -c 500 -n 1000 -r 500 "http://localhost:5000/time/2"
bombardier -c 500 -n 1000 -r 500 "http://localhost:5000/time/3"
bombardier -c 500 -n 1000 -r 500 "http://localhost:5000/time/4"
```

average under 500 concurrent is 5s per 1000 listing requests
