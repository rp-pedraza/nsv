FROM buildpack-deps:jessie

COPY data.processed /data.processed
COPY check-if-no-data.sh /check-if-no-data.sh
COPY import-processed-data-2.sh /import-processed-data-2.sh

CMD exec bash -c 'cd /; echo "Initial data will be attempted to be loaded after 40 seconds." && sleep 40 && ( . check-if-no-data.sh ) && ( . import-processed-data-2.sh )'
