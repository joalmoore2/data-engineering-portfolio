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

# Script generated for node step_trainer_trusted
step_trainer_trusted_node1745968148911 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="step_trainer_trusted", transformation_ctx="step_trainer_trusted_node1745968148911")

# Script generated for node accelerometer_trusted
accelerometer_trusted_node1745968151103 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="accelerometer_trusted", transformation_ctx="accelerometer_trusted_node1745968151103")

# Script generated for node SQL Query
SqlQuery2395 = '''
SELECT
  st.sensorreadingtime,
  st.serialnumber,
  st.distancefromobject,
  ac.timestamp,
  ac.x,
  ac.y,
  ac.z
FROM step_trainer_trusted AS st
JOIN accelerometer_trusted AS ac
  ON st.sensorreadingtime = ac.timestamp
WHERE st.cc_sharewithresearchasofdate IS NOT NULL;

'''
SQLQuery_node1745972864635 = sparkSqlQuery(glueContext, query = SqlQuery2395, mapping = {"step_trainer_trusted":step_trainer_trusted_node1745968148911, "accelerometer_trusted":accelerometer_trusted_node1745968151103}, transformation_ctx = "SQLQuery_node1745972864635")

# Script generated for node Machine Learning Curated
EvaluateDataQuality().process_rows(frame=SQLQuery_node1745972864635, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1745968068104", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
MachineLearningCurated_node1745968384997 = glueContext.getSink(path="s3://jmoore-wgu-bucket/step_trainer/curated/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="MachineLearningCurated_node1745968384997")
MachineLearningCurated_node1745968384997.setCatalogInfo(catalogDatabase="stedi",catalogTableName="machine_learning_curated")
MachineLearningCurated_node1745968384997.setFormat("json")
MachineLearningCurated_node1745968384997.writeFrame(SQLQuery_node1745972864635)
job.commit()