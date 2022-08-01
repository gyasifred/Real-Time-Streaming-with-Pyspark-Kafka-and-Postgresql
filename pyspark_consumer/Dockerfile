FROM bde2020/spark-submit:3.3.0-hadoop3.3

COPY requirements.txt .

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

COPY / .

ENV SPARK_MASTER_NAME spark-master
ENV SPARK_MASTER_PORT 7077
ENV SPARK_SUBMIT_ARGS "--driver-class-path=postgresql-42.4.0.jar --driver-memory 5G --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 --py-files /consumer.py"
ENV SPARK_APPLICATION_PYTHON_LOCATION /consumer.py
ENV SPARK_APPLICATION_ARGS ""

COPY submit.sh /
CMD ["/bin/bash", "/submit.sh"]

