import json
import os
from googleapiclient.discovery import build

api_key = os.getenv('API_KEY')


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id: str = channel_id
        response = self.get_info()
        youtube = Channel.get_service()
        self.channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title: str = response['items'][0]['snippet']['title']
        self.description: str = response['items'][0]['snippet']['description']
        self.url: str = 'https://www.youtube.com/channel/' + channel_id
        self.subscriber_count = int(self.channel["items"][0]["statistics"]["subscriberCount"])
        self.video_count: int = response['items'][0]['statistics']['videoCount']
        self.view_count: int = response['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f"{self.title}, ({self.url})"

    def __add__(self, redactsiya):
        if isinstance(redactsiya, Channel):
            return self.subscriber_count + redactsiya.subscriber_count
        else:
            raise TypeError("ERROR")

    def __sub__(self, redactsiya):
        if isinstance(redactsiya, Channel):
            return self.subscriber_count - redactsiya.subscriber_count
        else:
            raise TypeError("ERROR")

    def __ge__(self, redactsiya):  # >=
        if isinstance(redactsiya, Channel):
            return self.subscriber_count >= redactsiya.subscriber_count
        else:
            raise TypeError("ERROR")

    def __le__(self, redactsiya):  # <=
        if isinstance(redactsiya, Channel):
            return self.subscriber_count <= redactsiya.subscriber_count
        else:
            raise TypeError("ERROR")

    def __gt__(self, redactsiya):  # >
        if isinstance(redactsiya, Channel):
            return self.subscriber_count > redactsiya.subscriber_count
        else:
            raise TypeError("ERROR")

    def __lt__(self, redactsiya):  # <
        if isinstance(redactsiya, Channel):
            return self.subscriber_count < redactsiya.subscriber_count
        else:
            raise TypeError("ERROR")

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        response = self.get_info()
        print(json.dumps(response, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, filename: str) -> None:
        """
        Сохраняет в файл значения атрибутов экземпляра Channel
        """
        data = dict(map(lambda i: (i[0].removeprefix('_Channel__'), i[1]), self.__dict__.items()))
        with open(filename, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_info(self) -> dict:
        """
        Получает информацию о канале
        """
        response = self.get_service().channels().list(
            id=self.channel_id,
            part='snippet,statistics'
        ).execute()
        return response

    @channel_id.setter
    def channel_id(self, value):
        # self._channel_id = value
        print("AttributeError: property 'channel_id' of 'Channel' object has no setter")
