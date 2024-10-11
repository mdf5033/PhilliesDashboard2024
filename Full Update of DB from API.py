import mysql.connector
from mysql.connector import Error
import requests

def fetch_updated_schedule():
    url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBTeamSchedule"
    querystring = {"teamAbv": "PHI", "season": "2024"}
    headers = {
        "X-RapidAPI-Key": "",
        "X-RapidAPI-Host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def update_database_full(db_config, updated_schedule):
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        for game in updated_schedule['body']['schedule']:
            sql = """
            INSERT INTO PhilliesSchedule2024 (gameID, gameType, away, gameTime, teamIDHome, gameDate, gameStatus, gameTime_epoch, teamIDAway, home, awayResult, homeResult, homeH, homeR, homeE, awayH, awayR, awayE)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            gameType = VALUES(gameType), away = VALUES(away), gameTime = VALUES(gameTime), teamIDHome = VALUES(teamIDHome), gameDate = VALUES(gameDate), gameStatus = VALUES(gameStatus),
            gameTime_epoch = VALUES(gameTime_epoch), teamIDAway = VALUES(teamIDAway), home = VALUES(home), awayResult = VALUES(awayResult), homeResult = VALUES(homeResult),
            homeH = VALUES(homeH), homeR = VALUES(homeR), homeE = VALUES(homeE), awayH = VALUES(awayH), awayR = VALUES(awayR), awayE = VALUES(awayE);
            """
            cursor.execute(sql, (
                game['gameID'], game.get('gameType'), game.get('away'), game.get('gameTime'),
                game.get('teamIDHome'), game.get('gameDate'), game.get('gameStatus'),
                game.get('gameTime_epoch'), game.get('teamIDAway'), game.get('home'),
                game.get('awayResult'), game.get('homeResult'), game.get('homeH'), game.get('homeR'),
                game.get('homeE'), game.get('awayH'), game.get('awayR'), game.get('awayE')
            ))
        connection.commit()
        print("Database has been fully updated.")
    except Error as e:
        print(f"Error updating database: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def main():
    db_config = {
        'host': 'btbm-db.c57m1yfxa4e2.us-east-2.rds.amazonaws.com',
        'user': 'admin',
        'passwd': 'pyvtYr-nyrtoh-mupde6',
        'database': 'my_database_name'
    }
    updated_schedule = fetch_updated_schedule()
    if updated_schedule['statusCode'] == 200:
        update_database_full(db_config, updated_schedule)
    else:
        print("Failed to fetch updated schedule from API.")

if __name__ == "__main__":
    main()
