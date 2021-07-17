# Exposition

- The process of making metrics available to Prometheus is known as exposition.

- Exposition to Prometheus is done over HTTP. Usually you expose metrics under the /metrics path, and the request is handled for you by a client library.

- Prometheus uses a human-readable text format, so you also have the option of producing the exposition format by hand. You may choose to do this if there is no suitable library for your language, but it is recommended you use a library as it’ll get all the little details like escaping correct.
