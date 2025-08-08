# mp3-analyze

![](test.webp)

React - FastAPI(docker) 로컬 서비스

멀티미디어(음원) 파일을 사용하므로 호스팅 사이트 계획은 폐기되었습니다

대응하는 파일: mp3, wav, flac

## 구성

### client

- api(axios)

  서버와 통신 규격 간략하게, POST만 사용해 requests.js는 미사용

- components

  웹의 불변하는 부분, 파일 submit 버튼을 분리

  css에 크게 복잡한 부분이 없어 전부 styled-components로 통일할 수도 있으나, 후술할 styles에서 상속받는 부분이 있어 일단 유지

- contexts

  멀티미디어 파일이 들어가는 file을 프로젝트 전역에 useState 선언하고 공유

- pages

  메인 화면과 측정 화면을 분리, 로딩창은 메인에서 작동

- styles

  css 전역에 사용될 공통 요소: 스타일 리셋, 색상 선언, 페이지 속성(유사성 높음)

### docker-compute

FastAPI 베이스

- librosa

  https://librosa.org/doc/main/index.html

  음악을 분석하는 메인 모듈입니다.

- matplotlib

  https://matplotlib.org/stable/

  데이터를 그래프로 시각화합니다.

- pydub

  https://www.pydub.com/

  오디오 파일 작업을 간편하게 개선합니다. 음악 분석 전 mp3로 변환시키는 역할입니다.

## 기능

- 곡의 길이

  분:초 표기입니다.

- bpm & 리듬 밀도

  bpm/곡의 길이 -> 곡의 조밀함을 측정합니다.

- 크레스트 팩터 & 믹싱 강도

  믹싱의 볼륨 편차를 측정합니다.

- 피치 분석 그래프

  곡에서 어느 노트가 가장 많이/적게 나왔는지 표시합니다.

- 비트 분석 그래프

  곡의 에너지 분포와 드럼 비트 분포를 표시합니다.
