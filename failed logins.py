from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import re

# Define default arguments for the DAG
default_args = {
    'owner': 'security_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 1),
    'email': ['security@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'security_monitoring',
    default_args=default_args,
    description='A DAG to monitor unauthorized login attempts',
    schedule_interval='@hourly',  # Runs every hour
    catchup=False,
)

# Function to check logs for unauthorized login attempts
def check_unauthorized_logins():
    log_file = "/var/log/auth.log"  # Modify based on your system logs
    unauthorized_patterns = ["Failed password", "Invalid user", "authentication failure"]

    try:
        with open(log_file, 'r') as file:
            logs = file.readlines()

        # Check for security patterns
        for line in logs:
            if any(re.search(pattern, line) for pattern in unauthorized_patterns):
                print(f"⚠️ Security Alert: Unauthorized access attempt detected! Log: {line.strip()}")

    except FileNotFoundError:
        print(f"Log file {log_file} not found. Ensure the correct path.")

# Define the Python Operator
check_logs_task = PythonOperator(
    task_id='check_unauthorized_logins',
    python_callable=check_unauthorized_logins,
    dag=dag,
)

# Set task dependencies
check_logs_task