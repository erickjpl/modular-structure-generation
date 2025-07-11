bind = "0.0.0.0:8000"
module = "{{ project_name }}.wsgi:application"

workers = 2
worker_connections = 1000
threads = 2
