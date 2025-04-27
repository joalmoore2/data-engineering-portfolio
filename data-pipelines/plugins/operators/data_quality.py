from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 checks=[],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.checks = checks

    def execute(self, context):
        if not self.checks:
            raise ValueError("No data quality test cases provided!")

        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        for i, check in enumerate(self.checks):
            sql = check.get('check_sql')
            expected = check.get('expected_result')
            records = redshift.get_records(sql)

            if callable(expected):
                assert expected(records), f"Check {i} failed: {sql}"
            else:
                actual = records[0][0]
                assert actual == expected, f"Check {i} failed: got {actual}, expected {expected}"

            self.log.info(f"Data quality check {i} passed.")