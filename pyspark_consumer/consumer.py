# Read from kafka comnsumer
# Peform dataframe transformation
# Sink to Postgres JDBC

from pyspark.sql import SparkSession
from pyspark.sql.functions import asc, col, from_json, to_timestamp, window
from pyspark.sql import Row
from pyspark.sql.types import StructType, StringType, LongType
from consume.foreachatch import foreach_batch_function
from consume.database import engine
from consume import models

# create the temperature_reading table
models.Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    # Instantiate SparkSession
    spark = SparkSession.builder\
        .master("local[2]")\
        .config("spark.jars", "postgresql-42.4.0.jar") \
        .appName("StreamingPipeline").getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    kafka_topic_input = "temperature_readings"

    # Read Streams from kakfka
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", kafka_topic_input) \
        .option("startingOffsets", "earliest") \
        .option("spark.streaming.backpressure.enabled", True) \
        .option("spark.streaming.receiver.maxRate", "2") \
        .option("spark.scheduler.mode", "FAIR") \
        .load()

    df_str = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

    # Define the dataframe schema
    schema = (
        StructType()
        .add('id', StringType())
        .add('room_id/id', StringType())
        .add('noted_date', StringType())
        .add('temp', LongType())
        .add('out/in', StringType())
    )

    df_parsed = df_str.select(
        from_json(df_str.value, schema).alias("dataframe"))

    df_formatted = df_parsed.select(
        col("dataframe.id").alias("log_id"),
        col("dataframe.room_id/id").alias("room_id"),
        col("dataframe.noted_date").alias("timestamp"),
        col("dataframe.temp").alias("temperature"),
        col("dataframe.out/in").alias("room_location")
    )
    # Format timestamp
    df_time_stamp = df_formatted.withColumn(
        "timestamp", to_timestamp(
            df_formatted.timestamp, "dd-MM-yyyy HH:mm")
    )

    # Define  the window to perform transformation on the dataframe
    df_window = (
        df_time_stamp.withWatermark("timestamp", "30 minutes")
        .groupBy(window(df_time_stamp.timestamp, "30 minutes"), df_time_stamp.room_location)
        .avg("temperature")
    )

    df_final = df_window.select(
        "room_location",
        col("window.start").alias("window_start"),
        col("window.end").alias("window_end"),
        col("avg(temperature)").alias("avg_temperature")).orderBy(asc("room_location"), asc("window_start"))

    query = df_final\
        .writeStream.outputMode("complete").format("jdbc")\
        .foreachBatch(foreach_batch_function).start()

    query.awaitTermination()
