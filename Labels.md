# Labels

The ordering of labels does not matter, but it is a good idea to have the ordering consistent from scrape to scrape. This will make writing your unit tests easier, and consistent ordering ensures the best ingestion performance in Prometheus.

```
# HELP my_summary An example summary
# TYPE my_summary summary
my_summary_sum{foo="bar",baz="quu"} 1.8
my_summary_count{foo="bar",baz="quu"} 453
my_summary_sum{foo="blaa",baz=""} 0
my_summary_count{foo="blaa",baz="quu"} 0
```

The format is encoded in UTF-8

**Promtool** is a utility included with Prometheus that among other things can verify that your metric output is valid and perform lint checks.

`curl http://localhost:8000/metrics | promtool check metrics`

Labels are key-value pairs associated with time series that, in addition to the metric name, uniquely identify them.

What abstractions `labels` give? 

If you had a metric for HTTP requests that was broken out by path, you might try putting the path in the metric name, such as is common in Graphite:

```
http_requests_login_total 
http_requests_logout_total
http_requests_adduser_total 
http_requests_comment_total 
http_requests_view_total
```

These would be difficult for you to work with in PromQL. In order to calculate the total requests you would either need to know every possible HTTP path or do some form of potentially expensive matching across all metric names.

Instead, to handle this common use case, Prome‐ theus has labels. In the preceding case you might use a path label:

```
http_requests_total{path="/login"} 
http_requests_total{path="/logout"} 
http_requests_total{path="/adduser"}
http_requests_total{path="/comment"} 
http_requests_total{path="/view"}
```

Labels come from two sources, instrumentation labels and target labels. When you are working in PromQL there is no difference between the two, but it’s important to dis‐ tinguish between them in order to get the most benefits from labels.
