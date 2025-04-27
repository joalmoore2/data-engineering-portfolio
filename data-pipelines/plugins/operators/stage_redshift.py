from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.providers.amazon.aws.hooks.s3 import S3Hook


class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id='',
                 aws_credentials_id='',
                 table='',
                 s3_bucket='',
                 s3_key='',
                 json_path='',
                 region='',
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.json_path = json_path
        self.region = region

    def execute(self, context):
        self.log.info('Getting AWS credentials...')
        aws_hook = S3Hook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()

        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        # Render key with execution context
        rendered_key = self.s3_key.format(**context)
        s3_path = f"s3://{self.s3_bucket}/{rendered_key}"

        self.log.info(f"Clearing data from Redshift staging table {self.table}")
        self.log.info(f"Trying to delete from: public.{self.table}")
        tables_check = redshift.get_records("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public'")
        self.log.info(f"Available tables in 'public': {[t[0] for t in tables_check]}")

        redshift.run(f"DELETE FROM public.{self.table}")

        self.log.info(f"Copying data from {s3_path} to Redshift table {self.table}")
        copy_sql = f"""
            COPY {self.table}
            FROM '{s3_path}'
            ACCESS_KEY_ID '{credentials.access_key}'
            SECRET_ACCESS_KEY '{credentials.secret_key}'
            REGION '{self.region}'
            FORMAT AS JSON '{self.json_path}';
        """

        redshift.run(copy_sql)
        self.log.info(f"Data staged to {self.table} successfully.")




