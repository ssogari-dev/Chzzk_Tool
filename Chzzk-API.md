Origianl Article from [Tistory Blog](https://blog.ssogari.dev/25)


최근 [트위치(Twitch) 한국 서비스 종료 공지(\`23. 12. 5.)](https://blog.twitch.tv/ko-kr/2023/12/05/an-update-on-twitch-in-korea/)가 알려진 가운데, 네이버의 새로운 스트리밍 서비스인 '치지직(CHZZK)'의 베타 서비스가 시작되었습니다. 베타 서비스가 시작되며 많은 관심을 끌고 있어 관련 프로그램들의 수요 또한 증가하고 있어 이와 관련한 프로그램을 개발하는 데에 도움이 되고자 **네이버 치지직 API**를 정리합니다.


> API 문서를 같이 작성하실 분을 구합니다. API의 양이 생각보다 많아, 정리하는 데 시간이 다소 소요되고 있습니다.  
> 문서 작성을 함께 하실 분은 Twitter @ssogari\_dev 또는 이메일 admin at ssogari.dev로 알려주시면 모시러 가겠습니다!

---

### **1\. 참고사항**

#### **Authorization**

API를 호출하는 데 별도의 Access Token이나 Auth 절차가 필요하지 않습니다. 다만, 개별 사용자 정보를 기반으로 조회해야하는 팔로우 목록, 팔로잉 정보 등은 NAVER SSO 로그인을 필요로 합니다.  
  
  <br>

#### **HTTP Method**

API 호출은 HTTP 메소드와 URL의 조합으로 이루어지며, 현재까지 확인된 API는 GET 메소드로 호출하여 사용이 가능합니다. 추후 다른 메소드를 이용한 API가 필요한 경우 업데이트 예정입니다.

-   **GET - 리소스 조회**
    -   데이터를 검색하는 API에 사용됩니다.
<br>

#### **Parameter**

API를 호출할 때 리소스를 지정하는 **Path Parameter**가 필요합니다. 특정 리소스를 다루는 API 호출 시 API 요청 URL의 Path parameter에 대상 리소스를 식별하는 파라미터를 포함합니다. 아래의 API 설명에서는 `{parameter}`로 설명합니다.<br><br>

예) 특정 채널의 팔로잉 정보를 조회하는 API

```
GET https://api.chzzk.naver.com/service/v1/channels/{channel_id}/follow
```

이때, 자주 쓰이는 Parameter는 아래와 같습니다.

-   채널 고유 ID (`channel_id`, str)
    -   예: 580ff93d9df2d86549631c92d6141e57
    -   아래 설명에서 이는 **스트리머** 채널의 고유 ID를 나타내며, 사용자의 고유 ID를 설명해야 하는 경우 `user_id`로 나타냄.

---

### **2\. 공통 API Response**

아래에서는 여러 API에서 공통적으로 사용된 API Response을 정리합니다. 검색 API, 채널 API 등에서 공통적으로 사용된 **라이브 스트리밍 정보, VOD 정보**를 위주로 정리합니다. 필요에 따라 이후 설명에서는 다음과 같이 설명을 생략할 수 있습니다.

> 라이브 스트리밍(Live Streaming) Response는 상단의 2-(1) 항목을 참고하여 주십시오.

#### 1) 라이브 API Response
```json
"live": {
            "liveTitle": "",
            "liveImageUrl": "",
            "defaultThumbnailImageUrl": null,
            "concurrentUserCount": 1234,
            "accumulateCount": 12345,
            "openDate": "YYYY-MM-DD HH:MM:SS",
            "liveId": 0000,
            "chatChannelId": "chat_id",
            "categoryType": "GAME",
            "liveCategory": "category",
            "liveCategoryValue": "카테고리",
            "channelId": "channel_id",
            "livePlaybackJson": 
          }
```

-   **API Response**
    -  방송 제목 (`liveTitle`, str)
        -   라이브 스트리밍의 제목을 반환합니다.
    -  썸네일 이미지 (`liveImageUrl`, str)
        -   자동으로 생성된 썸네일 이미지 URL을 반환합니다.
        -   일반적으로 방송 화면을 실시간으로 갈무리한 이미지를 표시하며, `image_{type}.jpg`를 파일 명으로 가집니다. `{type}`에는 해상도 값이 들어갑니다 (Ex. 720, 1080)
    -  기본 썸네일 이미지 (`defaultThumbnailImageUrl`, str)
        -   채널 관리자가 설정한 기본 썸네일 이미지 URL을 반환합니다. 설정된 이미지가 없는 경우 `null`값을 반환합니다.
    -  현재 시청자 수 (`concurrentUserCount`, int)
        -   현재 라이브 스트리밍을 시청 중인 시청자의 수를 반환합니다.
    -  누적 시청자 수 (`accumulateCount`, int)
        -   시청자를 누적 집계한 수를 반환합니다.
    -  방송 시작 시간 (`openDate`, str)
        -   라이브 스트리밍이 시작된 시간을 반환합니다. 시간은 `YYYY-MM-DD HH:MM:SS` 형식으로 표시됩니다.
    -  방송 고유 ID (`liveId`, int)
        -   라이브 스트리밍의 고유 ID 번호를 반환합니다. 같은 채널이라도 각각의 방송을 구별하는 목적으로 사용됩니다.
    -  채팅방 ID (`chatChannelId`, str)
        -   채팅방 식별 ID 번호를 반환합니다. 각각의 채널마다 개별 ID를 부여하여, 같은 채널에서 켜진 스트리밍에서는 동일한 ID를 사용합니다.
    -  1차 카테고리 분류 (`categoryType`, str)
        -   방송 카테고리 대분류입니다. 일반적으로 게임 방송인 경우 `GAME`을 반환하고, 그 외에는 `ETC`를 반환합니다. 카테고리를 설정하지 않은 경우 `null`을 반환합니다.
    -  2차 카테고리 분류 (`liveCategory`, str)
        -   방송 카테고리 소분류입니다. 일반적으로 게임 방송인 경우 해당 게임의 이름을 값으로 가집니다 (예. `League_of_Legends`, `MapleStory_WORLDS` 등)
        -   Twitch에서의 Just Chatting은 `talk`으로 분류됩니다.
        -   1차 카테고리가 `null`인 경우, 해당 Response 또한 `null`을 반환합니다.
    -  2차 카테고리 (`liveCategoryValue`, str)
        -   일반적으로 2차 카테고리 분류의 표시명을 반환합니다. 위의 예시를 순서대로 나열하면 `리그 오브 레전드`, `메이플스토리 월드`, `talk`을 반환합니다.
    -  채널 고유 ID (`channelId`, str)
        -   채널의 고유 식별 ID입니다. 현재는 계정별 해시값을 반환합니다.
    -  스트리밍 HLS 정보 (`livePlaybackJson`, str)
        -   String 형태로 JSON을 반환합니다. 이 내용은 아래의 **2-(4) 항목**에서 설명합니다.
	       
	      <br><br>

#### 2) 비디오 API Response
```json
"videos": [
      {
        "videoNo": 1234,
        "videoId": "video_id",
        "videoTitle": "",
        "videoType": "REPLAY",
        "publishDate": "YYYY-MM-DD HH:MM:SS",
        "thumbnailImageUrl": "",
        "trailerUrl": "",
        "duration": 1234,
        "readCount": 1234,
        "publishDateAt": 123412342134,
        "categoryType": null,
        "videoCategory": null,
        "videoCategoryValue": "",
        "exposure": false,
        "channel": {
          "channelId": "channel_id",
          "channelName": "",
          "channelImageUrl": "",
          "verifiedMark": false,
          "personalData": { "privateUserBlock": false }
        }
      },
```

-   **Path Parameter**
    -  영상 번호 (`videoNo`, int)
        -   영상 식별 번호를 반환합니다. 일반적으로 `https://chzzk.naver.com/video/{videoNo}`의 path와 동일합니다.
    -  영상 ID (`videoId`, str)
        -   API에서 영상을 식별하는 ID입니다. 채널 고유 ID와 마찬가지로 영상의 해시값을 반환합니다.
    -  영상 제목 (`videoTitle`, str)
        -   영상 제목을 반환합니다. 일반적으로 다시보기 영상의 경우 스트리밍 시작 당시의 제목입니다.
    -  영상 유형 (`videoType`, str)
        -   영상 종류를 반환합니다. 다시보기의 경우 `REPLAY`, 직접 업로드한 영상은 `UPLOAD`을 반환합니다.
    -  게시 일자 (`publishDate`, str)
        -   영상이 게시된 날짜와 시간을 반환합니다. `YYYY-MM-DD HH:MM:SS` 형태를 가집니다.
    -  섬네일 URL (`thumbnailImageUrl`, str)
        -   영상의 섬네일 이미지 URL을 반환합니다.
    -  트레일러 영상 URL (`trailerUrl`, str)
        -   영상의 미리보기 트레일러 영상 URL을 반환합니다. 일반적으로 다시보기의 경우 자동 생성됩니다.
    -  영상 길이 (`duration`, int)
        -   영상의 길이를 반환합니다. 초(s) 단위로 되어 있습니다.
    -  조회수 (`readCount`, int)
        -   영상의 조회수를 반환합니다.
    -  게시 일자 (`publishDateAt`, int)
        -   영상이 게시된 날짜와 시간을 UNIX 타임스탬프 형태로 반환합니다. GMT+9 변환 시 `publishDate`와 동일한 값을 가집니다.
    -  1차 카테고리 분류 (`categoryType`, str)
        -   영상 카테고리 대분류입니다. 일반적으로 게임 영상인 경우 `GAME`을 반환하고, 그 외에는 `ETC`를 반환합니다. 카테고리를 설정하지 않은 경우 `null`을 반환합니다.
    -  2차 카테고리 분류 (`videoCategory`, str)
        -   영상 카테고리 소분류입니다. 일반적으로 게임 영상인 경우 해당 게임의 이름을 값으로 가집니다.
        -   차 카테고리가 `null`인 경우, 해당 Response 또한 `null`을 반환합니다.
    -  2차 카테고리 (`videoCategoryValue`, str)
        -   일반적으로 2차 카테고리 분류의 표시명을 반환합니다.
    -  ~~노출~~ (`exposure`, bool)
        -   ~~확인 필요~~
    -  채널 정보 (`channel`) - _**하단의 2-(3) 항목**을 참고하여 주십시오_
<br><br>

#### 3) 채널 정보 API Response
```json
"channel": {
          "channelId": "channel_id",
          "channelName": "channel_name",
          "channelImageUrl": null,
          "verifiedMark": false,
          "channelDescription": "",
          "followerCount": 0,
          "openLive": false,
          "personalData": {
            "following": {
              "following": false,
              "notification": false,
              "followDate": null
            },
            "privateUserBlock": false
}
```
-   **API Response**
	- 채널 고유 ID (`channelId`, str)
		- 채널의 고유 식별 ID입니다. 현재는 계정별 해시값을 반환합니다.
	- 채널 명 (`channelName`, str)
		- 채널 이름입니다. 네이버 게임 닉네임과 동일합니다.
	- 채널 프로필 사진 (`channelImageUrl`, str)
		- 채널 프로필 이미지의 URL을 반환합니다. 등록되지 않은 경우 `null`을 반환합니다.
	- 인증마크 (`verifiedMark`, bool)
		- 공식 인증 마크의 여부를 나타냅니다. 인증된 채널에 등록되는 배지가 표시됩니다.
	- 채널 설명 (`channelDescription`, str)
		- 채널 관리자가 등록한 채널 설명입니다. 등록되지 않은 경우 `""`로 빈 문자열을 반환합니다.
	- 팔로워 수 (`followerCount`, int)
		- 해당 채널을 팔로우한 인원을 반환합니다.
	- 방송 상태 (`openLive`, bool)
		- 해당 채널의 방송 상태를 나타냅니다. 방송이 켜져있는 경우 `true`, 꺼져있는 경우 `false`를 반환합니다.
	- 팔로우 정보 (`personalData`) - _비로그인 상태에서는 표시되지 않습니다_
		- 팔로우 상태 (`following`, bool)
			- 팔로우 여부를 나타냅니다. 팔로우한 경우 `true`, 팔로우하지 않은 경우 `false`를 반환합니다.
		- 알림 여부 (`notification`, bool)
			- 활동 알림 설정 여부를 나타냅니다. 알림을 활성화한 경우 `true`, 비활성화한 경우 `false`를 반환합니다.
		- 팔로우 날짜 (`followDate`, str)
			- 해당 채널을 팔로우한 날짜를 나타냅니다. 팔로우하지 않은 경우 `null`을 반환하며, 팔로우한 경우 `YYYY-MM-DD HH:MM:SS` 형식으로 값을 반환합니다.
	- 차단 여부 (`privateUserBlock`, bool)
		- 해당 채널의 차단 상태를 나타냅니다. 차단한 경우 `true`, 아닌 경우 `false`를 반환합니다.
		- 해당 속성이 `true`인 경우, 위의 모든 값은 정상적으로 불러오나 검색 화면 상에서는 정보가 표시되지 않습니다.
<br><br>

####  4) 스트리밍 HLS API Response

추가 예정.

<br><br>

---

<br><br>


### **3\. 검색 API**

#### 1) 채널 검색 (Search Channel)

```
https://api.chzzk.naver.com/service/v1/search/channels?keyword={keyword}&offset={offset}&size={size}&withFirstChannelContent={withFirstChannelContent}
```

-   **Path Parameter**
    -   검색 키워드 (`keyword`, str)
        -   검색할 키워드를 입력합니다.
    -   시작점 (`offset`, int)
        -   결과 목록의 시작점을 나타냅니다. 일반적으로 0부터 시작하여 결과의 첫 페이지를 가리킵니다.
    -   결과 개수 (`size`, int)
        -   반환할 결과의 수를 나타냅니다. 50이 입력된 경우 처음 50개의 결과를 반환합니다.
    -   첫 번째 채널 컨텐츠 (`withFirstChannelContent`, bool)
        -   첫 번째 결과에 표시된 채널의 컨텐츠(동영상, 라이브)를 표시할 지 여부를 결정합니다. 미입력 시 `false`로 동작합니다.

```json
{
  "code": 200,
  "message": null,
  "content": {
    "size": 50,
    "page": { "next": { "offset": 50 } },
    "data": [
      {
        "channel": {
          "channelId": "channel_id",
          "channelName": "channel_name",
          "channelImageUrl": null,
          "verifiedMark": false,
          "channelDescription": "",
          "followerCount": 0,
          "openLive": false,
          "personalData": {
            "following": {
              "following": false,
              "notification": false,
              "followDate": null
            },
            "privateUserBlock": false
          }
        },
        "content": { "live": null, "videos": null }
      }
}
```

-   **API Response**
    -   API 응답 코드 (`code`, int)
        -   API 호출에 대한 응답 코드를 반환합니다. 일반적으로 검색에 성공하면 200을 반환합니다. 검색 결과가 없는 경우도 200을 반환합니다.
    -   API 응답 메시지 (`message`, str)
        -   API 호출에 대한 응답 메시지를 반환합니다. 일반적으로 `null`을 반환하며, 오류가 발생한 경우 오류 메시지를 반환합니다.
    -   결과 개수 (`size`, int)
        -   반환할 결과의 개수입니다. 일반적으로 Path Parameter에 입력한 값을 반환합니다.
    -   페이지, 시작점 등 (`page`, `next`, `offset`, int)
        -   페이지 정보와 다음 페이지에 대한 offset 정보를 모두 포함합니다.
	- 채널 정보 (`channel`) - _**상단의 2-(3) 항목**을 참고하여 주십시오_
    -   컨텐츠 목록 (`content`) - _Parameter `withFirstChannelContent`이 `True`인 경우 표시합니다_
        -   라이브 정보 - _**상단의 2-(1) 항목**을 참고하여 주십시오._
        -   비디오 정보 - _**상단의 2-(2) 항목**을 참고하여 주십시오._

#### 2) 라이브 검색 (Search Live)

```
https://api.chzzk.naver.com/service/v1/search/lives?keyword={keyword}&offset={offset}&size={size}
```

-   **Path Parameter**
    -   검색 키워드 (`keyword`, str)
        -   검색할 키워드를 입력합니다.
    -   시작점 (`offset`, int)
        -   결과 목록의 시작점을 나타냅니다. 일반적으로 0부터 시작하여 결과의 첫 페이지를 가리킵니다.
    -   결과 개수 (`size`, int)
        -   반환할 결과의 수를 나타냅니다. 50이 입력된 경우 처음 50개의 결과를 반환합니다.

#### 3) 동영상 검색 (Search Video)

다시보기(VOD)를 포함한 클립 영상, 채널에서 게시된 영상 등을 검색합니다.

```
https://api.chzzk.naver.com/service/v1/search/videos?keyword={keyword}&offset={offset}&size={size}
```

-   **Path Parameter**
    -   검색 키워드 (`keyword`, str)
        -   검색할 키워드를 입력합니다.
    -   시작점 (`offset`, int)
        -   결과 목록의 시작점을 나타냅니다. 일반적으로 0부터 시작하여 결과의 첫 페이지를 가리킵니다.
    -   결과 개수 (`size`, int)
        -   반환할 결과의 수를 나타냅니다. 50이 입력된 경우 처음 50개의 결과를 반환합니다.

---

### **4\. 채널 API**

#### 1) 채널 정보 (Channel Info)

```
https://api.chzzk.naver.com/service/v1/channels/{channel_id}
```

-   **Path Parameter**
    -   채널 고유 ID (`keyword`, str)
        -   채널의 고유 ID를 나타냅니다. 네이버 ID를 대신하여 계정의 고유 정보를 가리킵니다.
        -   예: 580ff93d9df2d86549631c92d6141e57
