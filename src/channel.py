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
        self.title: str = response['items'][0]['snippet']['title']
        self.description: str = response['items'][0]['snippet']['description']
        self.url: str = 'https://www.youtube.com/channel/' + channel_id
        self.subscribers: int = response['items'][0]['statistics']['subscriberCount']
        self.video_count: int = response['items'][0]['statistics']['videoCount']
        self.view_count: int = response['items'][0]['statistics']['viewCount']

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
