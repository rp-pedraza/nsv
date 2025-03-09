# FROM alpine:latest
# RUN apk add --update curl openssl bash && rm -rf /var/cache/apk/*
FROM nikosch86/bash-curl-ssl:latest

WORKDIR /import-processed-data/scripts
COPY --from=root data/data.processed /import-processed-data/data.processed
COPY --from=root scripts/*.bash data/scripts/*.bash /import-processed-data/scripts/

CMD ["/bin/sh", "-c", "bash wait-for-valid-response.bash http://nsv-es:9200 && bash import-processed-data.bash http://nsv-es:9200 --yes"]
