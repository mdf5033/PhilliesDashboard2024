import requests
import base64
import mysql.connector
from data_fetching import get_player_news, get_first_story
from mysql.connector import Error


def analyze_phillies_performance(db_config):
    query = """
        SELECT COUNT(*) AS GamesCompleted,
        SUM(CASE WHEN (home = 'PHI' AND homeResult = 'W') OR (away = 'PHI' AND awayResult = 'W') THEN 1 ELSE 0 END) AS Wins,
        SUM(CASE WHEN (home = 'PHI' AND homeResult = 'L') OR (away = 'PHI' AND awayResult = 'L') THEN 1 ELSE 0 END) AS Losses,
        (SELECT gameDate FROM PhilliesSchedule2024 WHERE gameStatus = 'Completed' ORDER BY gameDate DESC, gameTime DESC LIMIT 1) AS LastGameDate,
        (SELECT CASE WHEN home = 'PHI' THEN homeR ELSE awayR END FROM PhilliesSchedule2024 WHERE gameStatus = 'Completed' ORDER BY gameDate DESC, gameTime DESC LIMIT 1) AS PhilliesScore,
        (SELECT CASE WHEN home = 'PHI' THEN awayR ELSE homeR END FROM PhilliesSchedule2024 WHERE gameStatus = 'Completed' ORDER BY gameDate DESC, gameTime DESC LIMIT 1) AS OpponentScore,
        (SELECT CASE WHEN home = 'PHI' THEN away ELSE home END FROM PhilliesSchedule2024 WHERE gameStatus = 'Completed' ORDER BY gameDate DESC, gameTime DESC LIMIT 1) AS LastOpponent,
        (SELECT CASE WHEN home = 'PHI' THEN away ELSE home END FROM PhilliesSchedule2024 WHERE gameStatus = 'Scheduled' ORDER BY gameDate ASC, gameTime ASC LIMIT 1) AS NextGameOpponent,
        (SELECT gameDate FROM PhilliesSchedule2024 WHERE gameStatus = 'Scheduled' ORDER BY gameDate ASC, gameTime ASC LIMIT 1) AS NextGameDate,
        (SELECT gameTime FROM PhilliesSchedule2024 WHERE gameStatus = 'Scheduled' ORDER BY gameDate ASC, gameTime ASC LIMIT 1) AS NextGameTime
        FROM PhilliesSchedule2024 WHERE gameStatus = 'Completed';
    """
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            games_completed, wins, losses, last_game_date, phillies_score, opponent_score, last_opponent, next_game_opponent, next_game_date, next_game_time = result
            win_percentage = (wins / games_completed) * 100 if games_completed > 0 else 0

            performance_content = (f"Total Games Completed: {games_completed}\n"
                                   f"Total Wins: {wins}\n"
                                   f"Total Losses: {losses}\n"
                                   f"Win Percentage: {win_percentage:.2f}%\n"
                                   f"Last Game Date: {last_game_date}\n"
                                   f"Last Opponent: {last_opponent}\n"
                                   f"Phillies Score: {phillies_score}\n" 
                                   f"Opponent Score: {opponent_score}\n"
                                   f"Next Game Date: {next_game_date}\n"
                                   f"Next Game Opponent: {next_game_opponent}\n"
                                   f"Next Game Time: {next_game_time}\n")
            return performance_content
        else:
            return "No game data available."
    except Error as e:
        print(f"Database error: {e}")
        return f"Database error: {e}"
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def update_wordpress_page(performance_content, wp_config):
    logo_html = logo_html = '<img src="https://ferrytheboat.com/wp-content/uploads/2024/08/phanatic.webp" ' \
                            'alt="Phillies Logo" width="500" height="300" />'
    full_content = f"{logo_html}\n{performance_content}"

    credentials = base64.b64encode(f"{wp_config['username']}:{wp_config['application_password']}".encode()).decode()
    headers = {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/json"
    }
    response = requests.post(f"{wp_config['url']}/wp-json/wp/v2/pages/{wp_config['page_id']}", headers=headers,
                             json={"content": full_content})
    if response.status_code in [200, 201]:
        print("Page updated successfully.")
    else:
        print(f"Failed to update page: {response.status_code}, {response.text}")
