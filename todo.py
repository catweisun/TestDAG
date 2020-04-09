"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""
from datetime import datetime, timedelta

from airflow.models.dag import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

now = datetime.now()
now_to_the_hour = (
    now - timedelta(0, 0, 0, 0, 0, 3)
).replace(minute=0, second=0, microsecond=0)
START_DATE = now_to_the_hour
DAG_NAME = 'test_dag_v2'

default_args = {
    'owner': 'airflow',
    'depends_on_past': True,
    'start_date': days_ago(2)
}

dag = DAG(DAG_NAME, schedule_interval=timedelta(minutes=5), default_args=default_args)

t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag,
)

t1.doc_md = """\
#### Task Documentation
You can document your task using the attributes `doc_md` (markdown),
`doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
rendered in the UI's Task Instance Details page.
![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)
"""
t2 = BashOperator(
    task_id='sleep',
    depends_on_past=False,
    bash_command='sleep 5',
    retries=3,
    dag=dag,
)
t3 = BashOperator(
    task_id='sleep2',
    depends_on_past=False,
    bash_command='sleep 20',
    retries=3,
    dag=dag,
)
t1 >> [t2, t3]