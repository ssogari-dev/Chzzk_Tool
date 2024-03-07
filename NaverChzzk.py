import re, json, requests
from streamlink.plugin import Plugin, pluginmatcher
from streamlink.stream import HLSStream, DASHStream
# from streamlink.stream.dash.dash import DASHStream

@pluginmatcher(re.compile(
    r'https?://chzzk\.naver\.com/(?:video/(?P<video_no>\d+)|live/(?P<channel_id>[^/?]+))$',
))
class ChzzkPlugin(Plugin):
    LIVE_INFO = "https://api.chzzk.naver.com/service/v2/channels/{channel_id}/live-detail"
    VOD_URL = "https://apis.naver.com/neonplayer/vodplay/v2/playback/{video_id}?key={in_key}"
    VOD_INFO = "https://api.chzzk.naver.com/service/v2/videos/{video_no}"
    headers = {
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
}
    

    def _get_streams(self):
        channel_id = self.match.group("channel_id")
        video_no = self.match.group("video_no")

        if channel_id:
            return self._get_live_streams(channel_id)
        elif video_no:
            return self._get_vod_streams(video_no)
        
    def _get_live_streams(self, channel_id):
        api_url = self.LIVE_INFO.format(channel_id=channel_id)

        try:
            response = requests.get(api_url, headers=self.headers)
            response.raise_for_status()
        except requests.RequestException as e:
            self.logger.error("Failed to fetch channel information: {0}".format(str(e)))
            return

        if response.status_code == 404:
            self.logger.error("Channel not found")
            return

        try:
            content = response.json().get('content', {})
            status = content.get('status')
            if status != 'OPEN':
                self.logger.error("Channel is not live (status: {0})".format(status))
                return

            self.author = content.get('channel', {}).get('channelName')
            self.category = content.get('liveCategory')
            self.title = content.get('liveTitle')
            stream_info = content.get('livePlaybackJson')
            
            hls_url = json.loads(stream_info).get('media', [{}])[0].get('path')

            yield from HLSStream.parse_variant_playlist(self.session, hls_url).items()

        except json.JSONDecodeError as e:
            self.logger.error("Failed to decode JSON response: {0}".format(str(e)))
            return
        
    def _get_vod_streams(self, video_no):
        api_url = self.VOD_INFO.format(video_no=video_no)

        try:
            response = requests.get(api_url, headers=self.headers)
            response.raise_for_status()
        except requests.RequestException as e:
            self.logger.error("Failed to fetch video information: {0}".format(str(e)))
            return

        if response.status_code == 404:
            self.logger.error("Video not found")
            return
        
        try:
            content = response.json().get('content', {})
            video_id = content.get('videoId')
            in_key = content.get('inKey')
            video_url = self.VOD_URL.format(video_id=video_id, in_key=in_key)

            self.author = content.get('channel', {}).get('channelName')
            self.category = content.get('videoCategory')
            self.title = content.get('videoTitle')
            self.vodDate = content.get('liveOpenDate')[0:10]
            
            for name, stream in DASHStream.parse_manifest(
                self.session, video_url,
                headers={"Accept": "application/dash+xml"}
            ).items():
                if stream.video_representation.mimeType == "video/mp2t":
                    yield name, stream

        except json.JSONDecodeError as e:
            self.logger.error("Failed to decode JSON response: {0}".format(str(e)))
            return

__plugin__ = ChzzkPlugin
