# This is the Dockerfile used by 'docker image build'.
# The Dockerfile configured to be used during 'docker compose' is configured
# in the compose file.

FROM python:3-alpine

RUN pip install requests

WORKDIR /import-processed-data/scripts
COPY --from=root data/data.processed /import-processed-data/data.processed
COPY --from=root data/scripts/*.py /import-processed-data/scripts/

CMD ["/bin/sh", "-c", "python3 wait-for-valid-response.py http://nsv-es:9200 && python3 import-processed-data.py http://nsv-es:9200 --yes"]
