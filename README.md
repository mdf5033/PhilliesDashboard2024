# Phillies Dashboard

The **Phillies Dashboard** is a Python-based project designed to analyze the Philadelphia Phillies' season performance, including their win-loss record, upcoming schedule, and relevant game statistics. The project fetches data from an API and processes it to provide insights into the team's progress throughout the season. The dashboard can be integrated with a WordPress site to display the analysis in a user-friendly format.

## Features

- **Season Record Analysis**: Provides an overview of the Phillies' current win-loss record and other key season statistics.
- **Upcoming Games**: Displays the schedule for the Phillies' next games, including opponents, dates, and venues.
- **Streaks and Trends**: Analyzes recent performance, including winning and losing streaks.
- **Team Performance Metrics**: Tracks various metrics over the season to highlight the team's progress.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mdf5033/PhilliesDashboard.git
   ```

2. **Install Required Dependencies**:
   Make sure you have Python 3 installed. The script requires the following Python modules:
   - `http.client`
   - `json`
   - `datetime`

   Install any additional dependencies if needed.

3. **Set Up Your API Key**:
   - Obtain an API key from the baseball data provider.
   - Replace `YOUR_API_KEY` in the code with your actual API key.

## Usage

1. **Analyzing the Phillies' Record**:
   The function `fetch_current_record` retrieves the team's win-loss record and other statistics. Example usage:

   ```python
   from data_fetching import fetch_current_record
   
   record_data = fetch_current_record()
   print(f"The Phillies' current record is {record_data['wins']} wins and {record_data['losses']} losses.")
   ```

2. **Fetching the Upcoming Schedule**:
   The function `fetch_upcoming_schedule` retrieves the next few games for the Phillies, showing opponents, dates, and game locations. Example usage:

   ```python
   from data_fetching import fetch_upcoming_schedule
   
   schedule = fetch_upcoming_schedule()
   for game in schedule:
       print(f"Next game: {game['opponent']} on {game['date']} at {game['venue']}")
   ```

3. **Running the Main Script**:
   You can run the main script from the command line to analyze the team's performance and generate insights:
   ```bash
   python main.py
   ```

## Configuration

- **API Endpoint**: Replace `"api.example.com"` in the `fetch_current_record` and `fetch_upcoming_schedule` functions with the actual API endpoint for the data provider.
- **Game Filters**: You can configure filters to analyze specific time frames (e.g., last 10 games) by modifying the relevant function parameters.

## File Structure

```
PhilliesDashboard/
│
├── data_fetching.py       # Contains functions for fetching team data from the API
├── main.py                # Main script to run the program
└── README.md              # Project documentation
```

## Error Handling

If any issues arise with network requests or data fetching, the script will log appropriate error messages. Ensure your API key and endpoints are correctly configured.

## Contributing

1. **Fork the Repository**
2. **Create a New Branch**
   ```bash
   git checkout -b feature-name
   ```
3. **Commit Your Changes**
   ```bash
   git commit -m "Add new feature"
   ```
4. **Push to the Branch**
   ```bash
   git push origin feature-name
   ```
5. **Open a Pull Request**

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgments

- [Tank01 MLB Live In-Game]([https://api.example.com](https://rapidapi.com/tank01/api/tank01-mlb-live-in-game-real-time-statistics/playground/apiendpoint_ace7dee9-2aab-4836-be4b-95e483cdb8e5)) - For providing team data.
- Python Community - For helpful resources and documentation.
