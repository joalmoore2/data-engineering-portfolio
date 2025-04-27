from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 sql_statement="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql_statement = sql_statement

    def execute(self, context):
        self.log.info(f'Starting LoadFactOperator for {self.table}')
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        formatted_sql = f"""
            INSERT INTO {self.table}
            {self.sql_statement};
        """
        self.log.info(f"Executing SQL for {self.table}:\n{formatted_sql}")
        redshift.run(formatted_sql)
        self.log.info(f"LoadFactOperator completed for {self.table}")
