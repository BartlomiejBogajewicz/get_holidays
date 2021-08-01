from datetime import timedelta,datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.sensors.filesystem import FileSensor
from get_holidays import get_holidays
from send_holidays_email import send_mail

# create default airflow args
default_args = {
    'owner': 'airflow',
    'retries':  1,
    'retry_delay' : timedelta(seconds = 30)
}


conn_parameters = {
    # Required
    'country': 'UK',
    'year':    2021,
    'api_key' : 'your_api_key'
}

with DAG('get_holidays', default_args=default_args, start_date= datetime(2021,7,22), schedule_interval = '@daily', catchup = False) as dag:

# check if API response is valid 

    check_source = HttpSensor(task_id="is_holidays_available",
            http_conn_id="holidays_api",
            endpoint="api/v2/holidays?",
            response_check=lambda response: "holidays" in response.text,
            poke_interval=5,
            timeout=20,
            request_params = conn_parameters)

# check if json file with holidays was created

    check_file = FileSensor(
        task_id = "holidays_json",
        fs_conn_id = "is_holidays_file_available",
        filepath = "holidays.json",
        poke_interval=5,
        timeout=20)

# add get_holidays to pipeline

    download_holidays = PythonOperator(task_id='get_holidays', python_callable=get_holidays)

# add send_mail to pipeline

    send_holidays = PythonOperator(task_id='send_holidays', python_callable=send_mail)



check_source >> download_holidays >> check_file >> send_holidays