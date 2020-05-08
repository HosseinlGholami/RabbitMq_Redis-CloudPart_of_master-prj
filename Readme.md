to access rabbitmqctl inside docker :
docker exec <NAME OF SERVICE> rabbitmqctl <COMMAND>
example:
	docker exec rabbitHGH -it bash
        docker exec rabbitHGH rabbitmqctl status
        docker exec rabbitHGH rabbitmqctl list_queues
        docker exec rabbitHGH rabbitmqctl list_queues name messages_ready messages_unacknowledged //for debuge wich messages arent ACK
	docker exec rabbitHGH rabbitmqctl list_exchanges //for recive the list of exchange
	docker exec rabbitHGH rabbitmqctl list_bindings
	docker exec rabbitHGH rabbitmq-plugins enable rabbitmq_mqtt // enable mqtt plugin