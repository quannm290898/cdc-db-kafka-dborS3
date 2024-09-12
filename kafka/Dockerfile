FROM debezium/connect:2.1

COPY confluentinc-kafka-connect-s3-10.3.1.zip .
RUN unzip confluentinc-kafka-connect-s3-10.3.1.zip \
    && mv confluentinc-kafka-connect-s3-10.3.1 /kafka/connect/ \
    && rm confluentinc-kafka-connect-s3-10.3.1.zip
# Sao chép JDBC driver vào thư mục plugin
COPY kafka-connect-jdbc-10.4.0.jar /kafka/connect/
COPY mysql-connector-java-8.0.29.jar /kafka/libs/

# Cấu hình biến môi trường
ENV CONNECT_PLUGIN_PATH=/kafka/connect

