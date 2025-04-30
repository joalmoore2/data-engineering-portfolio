import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue import DynamicFrame

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node Accelerometer Landing
AccelerometerLanding_node1745957150496 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="accelerometer_landing", transformation_ctx="AccelerometerLanding_node1745957150496")

# Script generated for node Customer Trusted
CustomerTrusted_node1745957156011 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="customer_trusted", transformation_ctx="CustomerTrusted_node1745957156011")

# Script generated for node Join Customer
JoinCustomer_node1745957415371 = Join.apply(frame1=AccelerometerLanding_node1745957150496, frame2=CustomerTrusted_node1745957156011, keys1=["user"], keys2=["email"], transformation_ctx="JoinCustomer_node1745957415371")

# Script generated for node Drop Fields
SqlQuery2252 = '''
select  
  timestamp,
  user,
  x,
  y,
  z 
from myDataSource

'''
DropFields_node1745958513543 = sparkSqlQuery(glueContext, query = SqlQuery2252, mapping = {"myDataSource":JoinCustomer_node1745957415371}, transformation_ctx = "DropFields_node1745958513543")

# Script generated for node Accelerometer Trusted
EvaluateDataQuality().process_rows(frame=DropFields_node1745958513543, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1745957081567", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AccelerometerTrusted_node1745958082961 = glueContext.getSink(path="s3://jmoore-wgu-bucket/accelerometer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AccelerometerTrusted_node1745958082961")
AccelerometerTrusted_node1745958082961.setCatalogInfo(catalogDatabase="stedi",catalogTableName="accelerometer_trusted")
AccelerometerTrusted_node1745958082961.setFormat("json")
AccelerometerTrusted_node1745958082961.writeFrame(DropFields_node1745958513543)
job.commit()