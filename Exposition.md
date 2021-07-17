# Exposition

- The process of making metrics available to Prometheus is known as exposition.

- Exposition to Prometheus is done over HTTP. Usually you expose metrics under the /metrics path, and the request is handled for you by a client library.

- Prometheus uses a human-readable text format, so you also have the option of producing the exposition format by hand. You may choose to do this if there is no suitable library for your language, but it is recommended you use a library as it’ll get all the little details like escaping correct.

# Pushgateway

Batch jobs are typically run on a regular schedule, such as hourly or daily. They start up, do some work, and then exit. As they are not continuously running, Prometheus can’t exactly scrape them.5 This is where the Pushgateway comes in.

The Pushgateway is a metrics cache for service-level batch jobs.

# Bridges

A bridge takes metrics output from the client library registry and outputs it to some‐ thing other than Prometheus.So the Graphite bridge will convert the metrics into a form that Graphite can understand and write them out to Graphite.

Prometheus client libraries are not limited to outputting metrics in the Prometheus format. There is a separation of concerns between instrumentation and exposition so that you can process the metrics in any way you like.
For example, the Go, Python, and Java clients each include a Graphite bridge.

- This works because the registry has a method that allows you to get a snapshot of all the current metrics. This is `CollectorRegistry.collect` in Python, `CollectorRegistry.metricFamilySamples` in Java, and `Registry.Gather` in Go. This is the method that HTTP exposition uses, and you can use it too. For example, you could use this method to feed data into another non-Prometheus instrumentation library.

The metrics made available at `/metrics` HTTP endpoint has
`Content-Type: text/plain; version=0.0.4; charset=utf-8`

In the simplest cases, the text format is just the name of the metric followed by a 64- bit floating-point number. Each line is terminated with a line-feed character (\n).

e.g.

- my_counter_total 14
- a_small_gauge 8.3e-96

Major types of metrics in Prometheus: Gauge, Counter, Historgram, Summary.

```text
# HELP example_gauge An example gauge
# TYPE example_gauge gauge
example_gauge -0.7
# HELP my_counter_total An example counter
# TYPE my_counter_total counter my_counter_total 14
# HELP my_summary An example summary
# TYPE my_summary summary my_summary_sum 0.6
my_summary_count 19
# HELP my_histogram An example histogram
# TYPE my_histogram histogram latency_seconds_bucket{le="0.1"} 7
latency_seconds_bucket{le="0.2"} 18
latency_seconds_bucket{le="0.4"} 24
latency_seconds_bucket{le="0.8"} 28
latency_seconds_bucket{le="+Inf"} 29
latency_seconds_sum 0.6
latency_seconds_count 29
```

HELP is a description of what the metric is, and should not generally change from scrape to scrape.

TYPE is one of counter, gauge, summary, histogram, or untyped. untyped is used when you do not know the type of the metric, and is the default if no type is specified.

Prometheus currently throws away HELP and TYPE, but they will be made available to tools like Grafana in the future to aid in writing quer‐ ies. It is invalid for you to have a duplicate metric, so make sure all the time series that belong to a metric are grouped together.
