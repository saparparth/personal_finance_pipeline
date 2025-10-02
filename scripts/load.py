
import os
from dotenv import load_dotenv

def load_to_db():
    # Set environment variable BEFORE any Spark imports
    os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.postgresql:postgresql:42.7.3 pyspark-shell'
    
    from pyspark.sql import SparkSession
    from scripts.transform import transform
    
    
    load_dotenv()
    url = os.getenv('API_URL')
    
    output_path = transform(url)
        
    if output_path is None:
        print("❌ No data returned from transform.py")
        return
            
    spark = SparkSession.builder \
        .appName("YourApp") \
        .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3") \
        .getOrCreate()
  
    sorted_df = spark.read.parquet(output_path)
    
    db_url = "jdbc:postgresql://localhost:5432/personal_finance"
    db_properties = {
        "user": "parth",
        "password": "root",
        "driver": "org.postgresql.Driver"
    }
  
    sorted_df.write.jdbc(
        url=db_url,
        table="transactions",
        mode="append",
        properties=db_properties
    )
    
    print("✅ Data successfully loaded into Postgres!")


if __name__ == "__main__":
    load_to_db()