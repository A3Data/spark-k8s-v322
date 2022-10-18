
# CREATE SPARK SESSION
from pyspark.sql import SparkSession
from delta.tables import *

builder = (
    SparkSession
    .builder
    .appName('teste-322-20221011-2002')
    # Packages
    .config("spark.jars.packages",
            ["io.delta:delta-core_2.12:2.0.0",
            "io.delta:delta-storage:2.0.0",
            "org.apache.hadoop:hadoop-aws:3.3.1",
            "org.apache.hadoop:hadoop-common:3.3.1",
            "org.apache.hadoop:hadoop-mapreduce-client-core:3.3.1"
            "org.apache.spark:spark-hadoop-cloud_2.12:3.3.0"
            ])
    # Delta Configs
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    # S3 Configs
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .config("spark.hadoop.fs.s3a.fast.upload", "true")
    # Comitters Configs
    .config("spark.hadoop.fs.s3a.bucket.all.committer.magic.enabled", "true")
    .config("spark.hadoop.fs.s3a.directory.marker.retention", "keep")
    # Spark Configs    
    .config("spark.default.parallelism", 8)
    .config("spark.sql.adaptive.enabled", 'true')
    .config("spark.sql.adaptive.coalescePartitions.enabled", 'true')
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
    .config("spark.sql.parquet.int96RebaseModeInWrite", 'LEGACY')
)

spark = delta.configure_spark_with_delta_pip(builder).getOrCreate()
spark.sparkContext.setLogLevel("INFO")

## Write Data On s3 using Dynamic Partition Overwrite Mode
def write_df_s3(df, path):
    (
        df
        .coalesce(1)
        .write
        .format("delta")
        .option("partitionOverwriteMode", "dynamic")
        .mode("overwrite")
        .partitionBy('<INSERT HERE PARTITION COLUMNS>')
        .save(path)
    )