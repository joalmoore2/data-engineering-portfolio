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

# Script generated for node Customer Landing
CustomerLanding_node1745945684400 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://jmoore-wgu-bucket/customer/landing/"], "recurse": True}, transformation_ctx="CustomerLanding_node1745945684400")

# Script generated for node Privacy Filter
SqlQuery2140 = '''
select * from myDataSource
where sharewithresearchasofdate is not null
'''
PrivacyFilter_node1745945847594 = sparkSqlQuery(glueContext, query = SqlQuery2140, mapping = {"myDataSource":CustomerLanding_node1745945684400}, transformation_ctx = "PrivacyFilter_node1745945847594")

# Script generated for node Trusted Customer Zone
EvaluateDataQuality().process_rows(frame=PrivacyFilter_node1745945847594, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1745944901227", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
TrustedCustomerZone_node1745948867019 = glueContext.write_dynamic_frame.from_options(frame=PrivacyFilter_node1745945847594, connection_type="s3", format="json", connection_options={"path": "s3://jmoore-wgu-bucket/customer/trusted/", "partitionKeys": []}, transformation_ctx="TrustedCustomerZone_node1745948867019")

job.commit()