import re
from streamlink.plugin import Plugin, pluginmatcher
from streamlink.stream import HLSStream

@pluginmatcher(re.compile("https://chzzk.naver.com/live/(?P<id>[^/]+)"))
class NaverLivePlugin(Plugin):

    def __init__(self):
        super().__init__()
        self.id = self.match.group("id")

    def get_stream_url(self):
        # 스트림 URL을 반환합니다.
        response = self.session.get(
            f"https://api.chzzk.naver.com/service/v1/channels/{self.id}/live-detail"
        )
        if response.status_code == 200:
            data = response.json()
            if data["content"]["status"] == "OPEN":
                for media in data["live"]["media"]:
                    if media["mediaId"] == "HLS":
                        return media["path"]
                return None
        return None

    def on_open(self):
        # 스트림이 열렸을 때 호출됩니다.
        response = self.session.get(
            f"https://api.chzzk.naver.com/service/v1/channels/{self.id}/live-detail"
        )
        if response.status_code == 200:
            data = response.json()
            # print(f"채널 {data['content']['channelName']}({self.id})의 방송이 시작되었습니다.")
            # print(f"스트림 URL: {self.get_stream_url()}")
            # print(f"방송 제목: {data['content']['liveTitle']}")
            # print(f"방송 카테고리: {data['content']['liveCategory']}")
            self.stream = HLSStream(self.get_stream_url())
            self.stream.start(filename=f"{data['content']['channelName']}_{data['content']['liveTitle']}_{data['content']['liveStartTime']}.ts")

    def on_close(self):
        # 스트림이 닫혔을 때 호출됩니다.
        if self.stream:
            self.stream.stop()
            print(f"채널 {self.id}의 방송이 종료되었습니다.")

__plugin__ = NaverLivePlugin
