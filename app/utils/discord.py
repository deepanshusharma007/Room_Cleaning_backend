import requests
# import logging
from app.utils.logger import logging
from app.config import DISCORD_WEBHOOK_URL

logger = logging.getLogger(__name__)


def send_cleaning_to_discord(cleaner_name, room_number, image_url):

    payload = {
        "embeds": [
            {
                "title": "🧹 Room Cleaned",
                "color": 5814783,
                "fields": [
                    {
                        "name": "Cleaner",
                        "value": cleaner_name,
                        "inline": True
                    },
                    {
                        "name": "Room",
                        "value": room_number,
                        "inline": True
                    }
                ],
                "image": {
                    "url": image_url
                }
            }
        ]
    }

    try:

        response = requests.post(
            DISCORD_WEBHOOK_URL,
            json=payload,
            timeout=5
        )

        if response.status_code != 204:
            logger.error(
                f"Discord webhook failed: {response.status_code} {response.text}"
            )

    except Exception as e:

        logger.error(f"Discord webhook error: {str(e)}")