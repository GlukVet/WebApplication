#FROM rabbitmq

#RUN rabbitmq-plugins enable --offline rabbitmq_management

FROM rabbitmq:3.8-management
RUN rabbitmq-plugins enable --offline rabbitmq_mqtt rabbitmq_federation_management rabbitmq_stomp

EXPOSE 15672 15672



	
