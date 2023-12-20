
# Chzzk Tool (치지직 관련 도구)

스트리밍 서비스 '네이버 치지직(CHZZK)'과 관련한 여러 도구를 제작합니다.
> **Note:** 네이버 측의 요청이 있는 경우 코드가 삭제되거나 비공개될 수 있습니다.

<br/>

*Developer Contact Info.*

 - Email - admin at ssogari.dev
 - Twitter - ssogari_dev

## Python

아래 도구는 Python으로 제작되었습니다. Python 3.11 버전에 최적화 되어있으며, 필요한 모듈은 파일 명과 함께 작성하였습니다.
<br/><br/>

### Streamlink Plugin (NaverChzzk.py)
Streamlink를 이용한 치지직(Chzzk) 방송 정보를 얻는 플러그인입니다.
<br><br>아래의 예시 명령어를 이용하면 실시간 방송 다운로드도 가능합니다.
<br>화질 정보 및 Output 파일 정보를 입력하지 않으면, 방송 정보 조회만 가능합니다.<br>
> **Note:**  사용 전 Python과 Streamlink 설치가 필요합니다.

```
streamlink "https://chzzk.naver.com/live/{고유ID}" {화질} -o {내보낼 파일 명}
```

<br>Streamlink 디렉터리(`%APPDATA%\Streamlink\plugins`)에 해당 파이썬 파일을 저장하여 주십시오.
<br><br>
| metadata | Description |
|--|--|
| {title} | Streaming Title |
| {category} | Streaming Category (usu. Korean) |
| {author} | Channel Name |




<br/><br/><br/>
### Twitter Alert Bot (Twitter_Alert_Chzzk.py)
스트리머가 방송을 켜면 Twitter(현 X)에 자동으로 트윗을 게시하는 코드입니다.
> **Note:** Twitter Developer Portal 에서 Access Token, Consumer Key를 발급받아 사용해야 합니다.
>
>  (추후 업데이트를 통해 로그인을 통해 API 값 받아올 수 있도록 기능 개선 예정)

`channel_id`에 알림을 발송하고자 하는 스트리머의 고유 채널 ID를 입력해주십시오.


실행 후에는 방송이 켜지면 자동으로 알림을 발송하고, 방송이 켜지지 않은 경우 10초에 한 번씩 방송 상태를 확인합니다.
