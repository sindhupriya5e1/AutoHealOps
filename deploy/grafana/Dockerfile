FROM grafana/grafana:latest
COPY provisioning /etc/grafana/provisioning
ENV GF_SERVER_HTTP_ADDR=0.0.0.0
ENV GF_SERVER_HTTP_PORT=10000
EXPOSE 10000
ENTRYPOINT ["/bin/sh", "-c", "export GF_SERVER_HTTP_PORT=10000; exec /run.sh"]
