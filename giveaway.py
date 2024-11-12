
import requests, time, random, yaml
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class Config:
    """Configuration class to store all settings"""
    session_id: str
    csrf_token: str
    post_id: str
    comment_texts: List[str]
    max_comments_per_hour: int = 20
    max_comments_per_day: int = 100

    @classmethod
    def from_yaml(cls, path: str) -> 'Config':
        """Load configuration from YAML file"""
        with open(path, 'r') as file:
            config_data = yaml.safe_load(file)
        return cls(**config_data)

class InstagramBot:
    BASE_URL = "https://www.instagram.com/api/v1/web"

    def __init__(self, config: Config):
        self.session_id = config.session_id
        self.csrf_token = config.csrf_token
        self.post_id = config.post_id
        self.comment_texts = config.comment_texts
        self.max_comments_per_hour = config.max_comments_per_hour
        self.max_comments_per_day = config.max_comments_per_day
        self.comments_posted_today = 0

    def _get_headers(self) -> Dict[str, str]:
        return {
            'x-csrftoken': self.csrf_token,
        }

    def _get_cookies(self) -> Dict[str, str]:
        return {
            'sessionid': self.session_id,
        }

    def post_comment(self) -> requests.Response:
        url = f"{self.BASE_URL}/comments/{self.post_id}/add/"

        # Randomly select a comment text from the list
        comment_text = random.choice(self.comment_texts)
        comment_text = f"{comment_text} #{str(random.randint(100000, 999999))}"
        data = {'comment_text': comment_text}

        response = requests.post(
            url,
            cookies=self._get_cookies(),
            headers=self._get_headers(),
            data=data
        )
        if response.status_code == 200:
            self.comments_posted_today += 1
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"Posted comment: {comment_text}. Total comments today: {self.comments_posted_today}")
            print(f"Time: {current_time}")
        else:
            print(f"Failed to post comment. Status code: {response.status_code}")

    def random_delay(self, min_seconds: int = 30, max_seconds: int = 90):
        delay = random.randint(min_seconds, max_seconds)
        print(f"Sleeping for {delay} seconds to avoid spam detection.")
        time.sleep(delay)

    def check_rate_limits(self):
        current_time = datetime.now()
        if self.comments_posted_today >= self.max_comments_per_day:
            print("Daily comment limit reached. Pausing until the next day.")
            while datetime.now().day == current_time.day:
                time.sleep(60)  # Sleep for 1 minute, then check again

    def run(self):
        while self.comments_posted_today < self.max_comments_per_day:
            self.check_rate_limits()
            self.post_comment()
            
            # Sleep for a random time between 30 and 90 seconds
            self.random_delay()

            # If more than max_comments_per_hour have been posted, pause
            if self.comments_posted_today % self.max_comments_per_hour == 0:
                print("Hourly comment limit reached. Pausing for 10-20 minutes.")
                time.sleep(random.randint(600, 1200))  # Pause between 10 and 20 minutes

if __name__ == "__main__":
    config = Config.from_yaml('config.yaml')
    bot = InstagramBot(config)
    bot.run()