# Prometheus Instrumentation

The program starts up a HTTP server on port 8000 to serve metrics to Prometheus.

You can setup prometheus to scrape from this endpoint by adding

```yaml
- job_name: python_web_server
  static_configs:
    - targets: ["localhost:8000"]
      labels:
        group: "python web server"
```

Few important metrics being instrumented:

1. `rate(hello_world_latency_seconds_count[1m])` : per-second rate of Hello World requests
2. `rate(hello_world_latency_seconds_sum[1m])` is the amount of time spent responding to requests per second

If you divide these two expressions you get the average latency over the last minute. The full expression for average latency would be:

```
rate(hello_world_latency_seconds_sum[1m]) / rate(hello_world_latency_seconds_count[1m])
```

Let’s take an example. Say in the last minute you had three requests that took 2, 4, and 9 seconds. The count would be 3 and the sum would be 15 seconds, so the average latency is 5 seconds. rate is per second rather than per minute, so you in principle need to divide both sides by 60, but that cancels out.
