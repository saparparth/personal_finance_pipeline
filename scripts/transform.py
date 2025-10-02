import os
import logging
from datetime import datetime
from scripts.extract import extract
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, to_date, when, regexp_replace, month, year, from_utc_timestamp
)

logging.basicConfig(level=logging.INFO)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")


def transform(url: str):
    spark = SparkSession.builder \
        .appName("Transaction Data Cleaning") \
        .getOrCreate()

    data = extract(url)
    if data:
        df = spark.createDataFrame(data)

        clean_df = (
            df
            .withColumn("date", to_date(col("createdAt").substr(1, 10), "yyyy-MM-dd"))
            .withColumn("amount", regexp_replace(col("amount"), "[^0-9.-]", "").cast("double"))
            .withColumn(
                "category",
                when(col("description").rlike("(?i)food|restaurant|cafe"), "Food")
                .when(col("description").rlike("(?i)bill|utility|electricity"), "Bills")
                .when(col("description").rlike("(?i)shop|mall|amazon|games"), "Shopping")
                .when(col("description").rlike("(?i)salary|payroll|credit"), "Salary")
                .otherwise(col("category"))
            )
            .withColumn("year", year(col("date")).cast("integer"))
            .withColumn("month", month(col("date")).cast("integer"))
            .withColumn(
            "transaction_type",
            when(col("type").isin("deposit", "invoice"), "Income")
            .when(col("type").isin("payment", "withdrawal"), "Expense")
            .otherwise("Other")
)
            .withColumn("createdAt_ts", from_utc_timestamp(col("createdAt"), "UTC"))
        )

        sorted_df = clean_df.orderBy(col("createdAt_ts").desc())
        sorted_df.show(truncate=False)

        # Save to staging
        staging_dir = "data/staging"
        os.makedirs(staging_dir, exist_ok=True)

        output_path = os.path.join(staging_dir, f"cleaned_data_{timestamp}")
        sorted_df.coalesce(1).write.mode("overwrite").parquet(output_path)

        logging.info(f"✅ Cleaned data written to: {output_path}")

        return output_path

    else:
        logging.error("❌ No data fetched. Please check the API or network.")
        return None