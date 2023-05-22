from src.swen344_db_utils import exec_sql_file

def init_test_data():
    exec_sql_file("init_test_data.sql")
   