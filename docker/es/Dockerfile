# This image is not necessary for creating the stack since everything
# can be configured in the .yml files, but I'll keep this here for
# reference.

FROM docker.elastic.co/elasticsearch/elasticsearch:5.2.2

ENV cluster.name=nsv-cluster
ENV bootstrap.memory_lock=true
ENV ES_JAVA_OPTS="-Xms512m -Xmx512m"
ENV xpack.security.enabled=false
