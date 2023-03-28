import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from src.channel import Channel

api_key = os.getenv('API_KEY')


class Video:
    def __init__(self, video_id: str) -> None:
        """
        Инициализатор объекта класса на основе google api client с необходимыми атрибутами
        """

        self.__video_id: str = video_id
        try:
            Channel.get_video(self.__video_id)['items'][0]
        except IndexError:
            self.video_id = None
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None
        else:
            response = self._get_info(video_id)
            self.video_id: str = video_id
            self.title: str = response['items'][0]['snippet']['title']
            self.url: str = 'https://youtu.be/' + video_id
            self.view_count: int = int(response['items'][0]['statistics']['viewCount'])
            self.like_count: int = int(response['items'][0]['statistics']['likeCount'])

    def __str__(self) -> str:
        return f'{self.title}'

    @staticmethod
    def get_service():
        return build('youtube', 'v3', developerKey=api_key)

    def _get_info(self, video_id: str) -> dict:
        response = self.get_service().videos().list(
            part='snippet,statistics,contentDetails,topicDetails',
            id=video_id
        ).execute()
        return response


class PLVideo(Video):
    """
    Класс для плейлиста
    """
    def __init__(self, video_id: str, pl_id: str):
        if self._get_pl_info(pl_id, video_id):
            super().__init__(video_id)
            self.__pl_id: str = pl_id

    def _get_pl_info(self, pl_id: str, video_id: str) -> dict | None:  # получает информацию о плейлисте
        try:
            response = self.get_service().playlistItems().list(playlistId=pl_id, part='contentDetails',
                                                               maxResults=1, videoId=video_id).execute()
            return response
        except Exception as e:
            print(e)
