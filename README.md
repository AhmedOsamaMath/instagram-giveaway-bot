# Instagram Giveaway Bot

A Python script that automates posting comments on an Instagram post for a giveaway, with configurable settings and rate limit handling.

## Features

- Automatically posts comments on a specified Instagram post
- Supports configurable comment texts and rate limits
- Handles Instagram's rate limits to avoid getting banned
- Randomizes the delay between comments to appear more natural

## Getting Started

### Prerequisites

- Python 3.7 or newer
- `requests`, `yaml`, and `dataclasses` Python libraries

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/AhmedOsamaMath/instagram-giveaway-bot.git
   ```
2. Create a `config.yaml` file in the project directory with the following configuration:
   ```yaml
   session_id: your_instagram_session_id
   csrf_token: your_instagram_csrf_token
   post_id: id_of_the_instagram_post_to_comment_on
   comment_texts:
     - "Great giveaway!"
     - "I want to win!"
     - "Good luck everyone!"
   max_comments_per_hour: 20
   max_comments_per_day: 100
   ```
3. Run the script:
   ```
   python giveaway.py
   ```

## How it Works

The script uses the Instagram web API to post comments on a specified post. It reads the configuration from a YAML file and handles rate limits to avoid getting banned by Instagram.

The main steps are:

1. Load the configuration from the `config.yaml` file.
2. Create an `InstagramBot` instance with the loaded configuration.
3. Run the `run()` method, which will continuously post comments until the daily limit is reached.
4. Between each comment, the script sleeps for a random amount of time (between 30 and 90 seconds) to appear more natural.
5. If the hourly or daily limit is reached, the script pauses until the next hour or day, respectively.

## Contributing

If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
