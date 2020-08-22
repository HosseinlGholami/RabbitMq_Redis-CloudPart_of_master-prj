FROM rabbitmq:3-management

RUN rabbitmq-plugins enable rabbitmq_management
RUN rabbitmq-plugins enable  rabbitmq_mqtt --offline

EXPOSE 1884
EXPOSE 5672
EXPOSE 15672
