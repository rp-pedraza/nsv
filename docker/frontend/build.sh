#!?bin/bash
exec docker image build --tag nsv-frontend:$(date +%Y%m%d%H%M%S) .
