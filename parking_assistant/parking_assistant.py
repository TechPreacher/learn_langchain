import feedparser
import json

# Zurich parking API
parking_api_url = "https://www.pls-zh.ch/plsFeed/rss"

class Parking:
    def __init__(self, name: str, spaces: int, open: bool) -> None:
        self.name = name
        self.spaces = spaces
        self.open = open

    @staticmethod
    def list_parkings() -> str:
        """List parkings available in Zurich.
        """
        parkings = Parking._parse_feed()
        parking_names = [parking.name for parking in parkings]
        return json.dumps(parking_names)

    @staticmethod
    def search_parking_spaces(parking_name: str) -> str:
        """Find available parking in the specified parking.

        Args:
            parking_name: the name of the parking
        """
        parkings = Parking._parse_feed()
        parking = Parking._find_parking(parkings, parking_name)
        return parking

    @staticmethod
    def _parse_feed() -> list:
        feed = feedparser.parse(parking_api_url)
        parkings = [
            Parking(
                name=entry["title"].split('/')[0].strip(),
                spaces=Parking._extract_spaces(entry["summary"].split('/')[1].strip()),
                open=Parking._extract_open(entry["summary"].split('/')[0].strip())
            )
            for entry in feed["entries"]
        ]
        return parkings

    @staticmethod
    def _extract_spaces(spaces_str: str) -> int:
        try:
            return int(spaces_str)
        except ValueError:
            return 0

    @staticmethod
    def _extract_open(open_str: str) -> bool:
        return open_str.lower() == 'open'

    @staticmethod
    def _find_parking(parkings: list, search: str) -> str:
        for parking in parkings:
            if search.lower() in parking.name.lower():
                return json.dumps(parking.__dict__)
        return f'Parking {search} not found in Zurich.'

