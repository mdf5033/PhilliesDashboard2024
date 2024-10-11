import os


def get_db_connection():
    return {
        'host': 'rds instance',
        'user': os.getenv('DB_USER'),  # Get username from environment variable
        'passwd': os.getenv('DB_PASSWORD'),  # Get password from environment variable,
        'database': 'my_database_name'
    }


def get_wp_config():
    return {
        'url': [wordpress site url],
        'page_id': [wordpress paage id],
        'username': os.getenv('WP_USER'),
        'application_password': os.getenv('WP_PASSWORD')
    }
