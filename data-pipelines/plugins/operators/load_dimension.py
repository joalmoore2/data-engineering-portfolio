from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 sql_statement="",
                 insert_mode="append",  # or "truncate-insert"
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql_statement = sql_statement
        self.insert_mode = insert_mode

    def execute(self, context):
        self.log.info(f"Starting LoadDimensionOperator for {self.table} with mode {self.insert_mode}")
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        if self.insert_mode == "truncate-insert":
            self.log.info(f"Truncating table {self.table} before insert.")
            redshift.run(f"TRUNCATE TABLE {self.table}")

        formatted_sql = f"""
            INSERT INTO {self.table}
            {self.sql_statement};
        """
        self.log.info(f"Executing SQL: {formatted_sql}")
        redshift.run(formatted_sql)
        self.log.info(f"LoadDimensionOperator completed for {self.table}")
