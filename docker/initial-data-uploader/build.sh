#!?bin/bash
exec docker image build --tag nsv-initial-data-uploader:$(date +%Y%m%d%H%M%S) .
