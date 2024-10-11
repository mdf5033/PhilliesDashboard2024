import mysql.connector
from mysql.connector import Error


def update_database_with_changes(current_schedule, updated_schedule, db_config):
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        for game in updated_schedule['body']['schedule']:
            gameID = game['gameID']
            if gameID in current_schedule and 'lineScore' in game:
                # Extract lineScore details for home and away
                line_score = game['lineScore']
                home_details = line_score['home']
                away_details = line_score['away']

                # Gather details for updating
                updated_status = game.get('gameStatus', 'NULL')
                updated_time = game.get('gameTime', 'NULL')
                updated_homeResult = game.get('homeResult', 'NULL')
                updated_awayResult = game.get('awayResult', 'NULL')
                updated_homeH = home_details.get('H', 'NULL')
                updated_homeR = home_details.get('R', 'NULL')
                updated_homeE = home_details.get('E', 'NULL')
                updated_awayH = away_details.get('H', 'NULL')
                updated_awayR = away_details.get('R', 'NULL')
                updated_awayE = away_details.get('E', 'NULL')

                # Prepare and execute the SQL update statement
                update_stmt = """
                UPDATE PhilliesSchedule2024
                SET gameTime = %s, gameStatus = %s,
                    homeH = %s, homeR = %s, homeE = %s,
                    awayH = %s, awayR = %s, awayE = %s,
                    homeResult = %s, awayResult = %s
                WHERE gameID = %s
                """
                cursor.execute(update_stmt, (updated_time, updated_status,
                                             updated_homeH, updated_homeR, updated_homeE,
                                             updated_awayH, updated_awayR, updated_awayE,
                                             updated_homeResult, updated_awayResult,
                                             gameID))

        connection.commit()
        print("Database has been updated based on the latest schedule.")
    except Error as e:
        print(f"Error updating database: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
