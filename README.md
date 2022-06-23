# Consumer service

This service has three endpoints:

* `/` which always returns the same JSON payload
* `/health` for health checks, always returns `200`
* `/inject/latency` which takes a query-string made of `value=<float>` to 
  induce a slower response of `/`. The value is in seconds.

It consumes data from the producer service.