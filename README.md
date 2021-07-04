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

#### Generate fake traffic:

```bash
while :
do
	curl -s -o /dev/null 'http://localhost:8001'
done
```

#### Restart program on file change:

```bash
$ watchexec -r -e py -- python3 test.py
```

Few important metrics being instrumented:

1. `rate(hello_world_latency_seconds_count[1m])` : per-second rate of Hello World requests
2. `rate(hello_world_latency_seconds_sum[1m])` is the amount of time spent responding to requests per second

If you divide these two expressions you get the average latency over the last minute. The full expression for average latency would be:

```
rate(hello_world_latency_seconds_sum[1m]) / rate(hello_world_latency_seconds_count[1m])
```

Let’s take an example. Say in the last minute you had three requests that took 2, 4, and 9 seconds. The count would be 3 and the sum would be 15 seconds, so the average latency is 5 seconds. rate is per second rather than per minute, so you in principle need to divide both sides by 60, but that cancels out.

3. Histogram `hello_world_latency_seconds_bucket` - A histogram has a set of buckets, such as 1 ms, 10 ms, and 25 ms, that track the number of events that fall into each bucket.

The `histogram_quantile` PromQL function can calculate a quantile from the buckets. For example, the 0.95 quantile (95th percentile) would be:

`histogram_quantile(0.95, rate(hello_world_latency_seconds_bucket[1m]))`
The rate is needed as the buckets’ time series are counters.

```
# TYPE hello_world_latency_seconds histogram
hello_world_latency_seconds_bucket{le="0.0001"} 6390.0
hello_world_latency_seconds_bucket{le="0.0002"} 11077.0
hello_world_latency_seconds_bucket{le="0.0005"} 11444.0
hello_world_latency_seconds_bucket{le="0.001"} 11447.0
hello_world_latency_seconds_bucket{le="0.01"} 11448.0
hello_world_latency_seconds_bucket{le="0.1"} 11448.0
hello_world_latency_seconds_bucket{le="+Inf"} 11448.0
hello_world_latency_seconds_count 11448.0
hello_world_latency_seconds_sum 1.3022565799996795
```

The buckets also include a count of events in all the smaller buckets, all the way up to the +Inf, bucket which is the total number of events. This is known as a cumulative histogram, and why the bucket label is called le, standing for less than or equal to.

The best way to think of buckets (and metrics generally) is that while they may not always be perfect, they generally give you sufficient information to determine the next step when you are debugging. So, for example, if Prometheus indicates that the 0.95 quantile jumped from 300 ms to 350 ms, but it was actually from 305 ms to 355 ms that doesn’t matter that much. You still know that there was a big jump, and the next step in your investigation would be the same either way.
