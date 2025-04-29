import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality

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

# Script generated for node Customer curated
Customercurated_node1745965724595 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="customer_curated", transformation_ctx="Customercurated_node1745965724595")

# Script generated for node Step_Trainer Landing to Trusted
Step_TrainerLandingtoTrusted_node1745965682532 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="step_trainer_landing", transformation_ctx="Step_TrainerLandingtoTrusted_node1745965682532")

# Script generated for node Join
Join_node1745965767418 = Join.apply(frame1=Step_TrainerLandingtoTrusted_node1745965682532, frame2=Customercurated_node1745965724595, keys1=["serialnumber"], keys2=["serialnumber"], transformation_ctx="Join_node1745965767418")

# Script generated for node Step_Trainer  Trusted
EvaluateDataQuality().process_rows(frame=Join_node1745965767418, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1745965382715", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
Step_TrainerTrusted_node1745965938816 = glueContext.getSink(path="s3://jmoore-wgu-bucket/step_trainer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="Step_TrainerTrusted_node1745965938816")
Step_TrainerTrusted_node1745965938816.setCatalogInfo(catalogDatabase="stedi",catalogTableName="step_trainer_trusted")
Step_TrainerTrusted_node1745965938816.setFormat("json")
Step_TrainerTrusted_node1745965938816.writeFrame(Join_node1745965767418)
job.commit()