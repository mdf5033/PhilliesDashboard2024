import requests
import http.client
import json
import mysql.connector
from mysql.connector import Error


def fetch_current_schedule_from_db(db_config):
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT gameID, gameStatus, gameTime FROM PhilliesSchedule2024")
            current_schedule = {gameID: {'status': gameStatus, 'time': gameTime} for gameID, gameStatus, gameTime in
                                cursor}
            return current_schedule
        else:
            print("Failed to connect to the database.")
    except Error as e:
        print(f"Error fetching schedule from DB: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()


def fetch_updated_schedule():
    url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBTeamSchedule"
    querystring = {"teamAbv": "PHI", "season": "2024"}
    headers = {
        "X-RapidAPI-Key": "",
        "X-RapidAPI-Host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch from API: Status Code", response.status_code)
        return None


def fetch_phillies_player_ids():
    url = 'https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBPlayerList'
    headers = {
        'X-RapidAPI-Key': '',
        'X-RapidAPI-Host': 'tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            data = response.json()  # Attempt to parse JSON
            # Parse the API response to extract player IDs associated with the team "PHI"
            phi_player_ids = []

            # Check if the response contains 'body' key with the list of players
            if 'body' in data:
                players = data['body']
                for player in players:
                    # Check if the player is associated with the team "PHI"
                    if player.get('team') == 'PHI':
                        phi_player_ids.append(player.get('playerID'))

                return phi_player_ids

        except Exception as e:
            print("Error processing JSON data:", str(e))
            return []
        else:
            print("Failed to fetch data:", response.status_code)


def get_player_news(player_ids):
    conn = http.client.HTTPSConnection("tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com")
    headers = {
        'X-RapidAPI-Key': "",
        'X-RapidAPI-Host': "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"
    }

    news_data = {}

    for player_id in player_ids:
        conn.request("GET", f"/getMLBNews?playerID={player_id}&recentNews=true&maxItems=1", headers=headers)
        res = conn.getresponse()
        data = res.read()
        news_data[player_id] = json.loads(data.decode("utf-8"))

    conn.close()
    print(news_data)
    return news_data


def get_first_story(news_data):
    first_stories = {}
    for player_id, news in news_data.items():
        if news['statusCode'] == 200 and news['body']:
            first_stories[player_id] = news['body'][0]
    return first_stories



