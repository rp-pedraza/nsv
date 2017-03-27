#!?bin/bash
exec docker image build --tag nsv-backend:$(date +%Y%m%d%H%M%S) .
