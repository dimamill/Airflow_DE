import pathlib
from datetime import datetime
import psycopg2
import pandas as pd
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator

#pg_hostname = 'host.docker.internal'
#pg_port = '5425'
#pg_username = 'postgres'
#pg_pass = 'password'
#pg_db = 'test'



def hello():
    print("Hello!")

def file_path():
    from airflow.models import Variable
    values = Variable.get("var")
    print("our value: ", values)

def pull_function(**kwargs):
    from airflow.models import Variable
    values = Variable.get("var")
    df = pd.read_csv(values)
    df.to_csv("df.csv")
    len_csv1=len(df)
    kwargs['ti'].xcom_push(key='len_csv', value=len_csv1)
    print(len_csv1)

def random_number():
    import random
    number1 = random.randint(0, 125)
    number2 = random.randint(0, 125)
    print(number1,' ',number2)
    file=open("file.txt","a")
    file.write(str(number1))
    file.write(" ")
    file.write(str(number2))
    print(file)
    file.close()

def summa():
    import numpy as np
    with open('file.txt') as f:
        result1, result2 = np.fromfile(f, dtype=int, count=2, sep=" ")
        sum1=np.sum(result2)
        sum2=np.sum(result2)
        raz=sum1-sum2
        np.save('file.txt', raz)




# A DAG represents a workflow, a collection of tasks
with DAG(dag_id="first_dag", start_date=datetime(2022, 1, 1), schedule="*/5 * * * *") as dag:
    # Tasks are represented as operators
    bash_task = BashOperator(task_id="hello", bash_command="echo hello")
    python_task = PythonOperator(task_id="world", python_callable=hello)
    file_path_task = PythonOperator(task_id="file_path", python_callable=file_path)
    pull_task = PythonOperator(task_id="pull_task", python_callable=pull_function)
    broadcast_task=PythonOperator(task_id="broadcast_task", python_callable=pull_function)
    number_task = PythonOperator(task_id="number_task", python_callable=random_number)
    sum_task = PythonOperator(task_id="sum_task", python_callable=summa)





    # Set dependencies between tasks
    bash_task>>python_task>>file_path_task>>pull_task>>broadcast_task>>number_task>>sum_task


