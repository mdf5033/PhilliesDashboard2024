from data_fetching import fetch_current_schedule_from_db, fetch_updated_schedule, fetch_phillies_player_ids, get_player_news, get_first_story
from data_updating import update_database_with_changes
from reporting import analyze_phillies_performance, update_wordpress_page
from utils import get_db_connection, get_wp_config

def main():
    # Retrieve configuration details directly without passing parameters
    db_config = get_db_connection()
    wp_config = get_wp_config()

    # Fetch current schedule from the database
    current_schedule = fetch_current_schedule_from_db(db_config)

    # Fetch updated schedule from the API
    updated_schedule = fetch_updated_schedule()
    if updated_schedule and updated_schedule['statusCode'] == 200:
        # Update the database with the new schedule information
        update_database_with_changes(current_schedule, updated_schedule, db_config)

    #phillies_player_ids = fetch_phillies_player_ids()
    #print("Phillies player IDs:", phillies_player_ids)

    # Analyze the Phillies performance and generate report content
    content = analyze_phillies_performance(db_config)
    if content:
        # Update the WordPress page with the new content
        update_wordpress_page(content, wp_config)

if __name__ == "__main__":
    main()
