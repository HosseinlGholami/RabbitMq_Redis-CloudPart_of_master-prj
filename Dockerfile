FROM rabbitmq:3-management

COPY definitions.json /opt/definitions.json
COPY rabbitmq.conf /etc/rabbitmq/rabbitmq.conf
