FROM prom/prometheus:latest
COPY prometheus.yml /etc/prometheus/prometheus.yml
EXPOSE 9090
ENTRYPOINT ["/bin/sh", "-c", "exec /bin/prometheus --config.file=/etc/prometheus/prometheus.yml --storage.tsdb.path=/prometheus --web.listen-address=0.0.0.0:${PORT:-9090} --web.enable-lifecycle"]
