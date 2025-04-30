import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue.dynamicframe import DynamicFrame
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

# Script generated for node Step_Trainer Landing
Step_TrainerLanding_node1745957150496 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="step_trainer_landing", transformation_ctx="Step_TrainerLanding_node1745957150496")

# Script generated for node Customer Curated
CustomerCurated_node1745957156011 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="customer_curated", transformation_ctx="CustomerCurated_node1745957156011")

# Script generated for node Renamed keys for Join Customer
RenamedkeysforJoinCustomer_node1745971753292 = ApplyMapping.apply(frame=CustomerCurated_node1745957156011, mappings=[("customername", "string", "cc_customername", "string"), ("email", "string", "cc_email", "string"), ("phone", "string", "cc_phone", "string"), ("birthday", "string", "cc_birthday", "string"), ("serialnumber", "string", "cc_serialnumber", "string"), ("registrationdate", "long", "cc_registrationdate", "long"), ("lastupdatedate", "long", "cc_lastupdatedate", "long"), ("sharewithresearchasofdate", "long", "cc_sharewithresearchasofdate", "long"), ("sharewithpublicasofdate", "long", "cc_sharewithpublicasofdate", "long"), ("sharewithfriendsasofdate", "long", "cc_sharewithfriendsasofdate", "long")], transformation_ctx="RenamedkeysforJoinCustomer_node1745971753292")

# Script generated for node Join Customer
Step_TrainerLanding_node1745957150496DF = Step_TrainerLanding_node1745957150496.toDF()
RenamedkeysforJoinCustomer_node1745971753292DF = RenamedkeysforJoinCustomer_node1745971753292.toDF()
JoinCustomer_node1745957415371 = DynamicFrame.fromDF(Step_TrainerLanding_node1745957150496DF.join(RenamedkeysforJoinCustomer_node1745971753292DF, (Step_TrainerLanding_node1745957150496DF['serialnumber'] == RenamedkeysforJoinCustomer_node1745971753292DF['cc_serialnumber']), "left"), glueContext, "JoinCustomer_node1745957415371")

# Script generated for node SQL Query
SqlQuery0 = '''
select * from myDataSource
WHERE cc_sharewithresearchasofdate IS NOT NULL;
'''
SQLQuery_node1745979895674 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"myDataSource":JoinCustomer_node1745957415371}, transformation_ctx = "SQLQuery_node1745979895674")

# Script generated for node Step_Trainer Trusted
EvaluateDataQuality().process_rows(frame=SQLQuery_node1745979895674, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1745957081567", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
Step_TrainerTrusted_node1745958082961 = glueContext.getSink(path="s3://jmoore-wgu-bucket/step_trainer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="Step_TrainerTrusted_node1745958082961")
Step_TrainerTrusted_node1745958082961.setCatalogInfo(catalogDatabase="stedi",catalogTableName="step_trainer_trusted")
Step_TrainerTrusted_node1745958082961.setFormat("json")
Step_TrainerTrusted_node1745958082961.writeFrame(SQLQuery_node1745979895674)
job.commit()
