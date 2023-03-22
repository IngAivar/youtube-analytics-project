import os
from googleapiclient.discovery import build

api_key = os.getenv('API_KEY')


class Video:
    def __init__(self, video_id: str) -> None:
        response = self._get_info(video_id)
        self.__video_id: str = video_id
        self.__title: str = response['items'][0]['snippet']['title']
        self.__url: str = 'https://youtu.be/' + video_id
        self.__view_count: int = int(response['items'][0]['statistics']['viewCount'])
        self.__like_count: int = int(response['items'][0]['statistics']['likeCount'])

    def __str__(self) -> str:
        return f'{self.__title}'

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
