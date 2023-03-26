import os
import isodate
from googleapiclient.discovery import build
import datetime

API_KEY = os.getenv('API_KEY')


class PlayList:
    """
    Класс, который инициализируется id плейлиста
    """

    def __init__(self, pl_id: str):
        self.__pl_id = pl_id
        response = self._get_pl_info()  # информация о плейлисте по его id
        self.title = response['items'][0]['snippet']['title']  # название плейлиста
        self.url = 'https://www.youtube.com/playlist?list=' + pl_id  # ссылка на плейлист
        videos_id = self._get_pl_items()  # информация о всех видео в плейлисте - список из id видео
        self.__videos = self._get_video_items(videos_id)  # информация по всем видео из списка с id

    @property
    def total_duration(self) -> datetime.timedelta:
        """
        Возвращает объект timedelta с суммарной длительностью плейлиста
        """
        total_duration = datetime.timedelta()
        for video in self.__videos['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self) -> str:
        """
        Возвращает ссылку на самое популярное видео из плейлиста по количеству лайков
        """
        max_likes = 0
        video_id = ''
        for video in self.__videos['items']:
            likes = int(video['statistics']['likeCount'])
            if likes > max_likes:
                video_id = video['id']
                max_likes = likes
        return 'https://youtu.be/' + video_id

    @staticmethod
    def get_service():
        """
        Возвращает объект для работы с YouTube API
        """
        return build('youtube', 'v3', developerKey=API_KEY)

    def _get_video_items(self, video_id_list) -> dict:
        """
        Получает информацию по всем видео из списка с id
        """
        response = self.get_service().videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_id_list)
                                                    ).execute()
        return response

    def _get_pl_items(self) -> list:
        """
        Получает информацию о всех видео в плейлисте, формируем список из id видео
        """
        response = self.get_service().playlistItems().list(playlistId=self.__pl_id,
                                                           part='contentDetails,snippet',
                                                           maxResults=50,
                                                           ).execute()
        video_ids = [video['contentDetails']['videoId'] for video in response['items']]
        return video_ids

    def _get_pl_info(self) -> dict:
        """
        Получает информацию о плейлисте по его id
        """
        response = self.get_service().playlists().list(id=self.__pl_id,
                                                       part='snippet',
                                                       ).execute()
        return response
