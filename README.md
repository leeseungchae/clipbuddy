# ClipBuddy

ClipBuddy는 LLM(GPT)을 사용하여 동영상을 이해하고 대화하는 기능을 제공하는 프로젝트입니다. 이 프로젝트는 프론트엔드, 백엔드 및 PostgreSQL 데이터베이스로 구성되어 있습니다.

## 설치 및 실행 방법

1. 먼저, 이 저장소를 클론합니다:

    ```sh
    git clone https://github.com/leeseungchae/clipbuddy.git
    cd clipbuddy
    ```

2. `clipbuddy` 디렉토리 안에 있는 `.env.example` 파일을 참고하여 `.env` 파일을 생성하고 필요한 변수 값을 추가합니다. 예시:

    ```sh
    cd ..
    cp .env.example .env
    # .env 파일을 열어 필요한 환경 변수를 설정합니다.
    ```

3. Docker Compose를 사용하여 프로젝트를 실행합니다:

    ```sh
    docker-compose up -d
    ```

이제 ClipBuddy가 실행되고 있을 것입니다.

## Docker Compose 구조

이 프로젝트는 다음과 같은 Docker Compose 서비스를 포함하고 있습니다:

- **프론트엔드**: 사용자 인터페이스를 제공
- **백엔드**: 클립보드 데이터를 처리하고 API를 제공
- **PostgreSQL**: 데이터베이스 서버

## 환경 변수 설정

`.env` 파일에 설정해야 하는 주요 환경 변수는 다음과 같습니다:

- `SECRET_KEY`: DJANGO KEY_
- `OPENAI_API_KEY`: OPENAI_API_KEY 


위의 변수 외에도 다른 환경 변수가 필요할 수 있습니다. 자세한 내용은 `.env.example` 파일을 참고하세요.

## 기여

기여를 원하신다면, 포크를 하시고 풀 리퀘스트를 보내주세요. 이 프로젝트에 대한 이슈는 GitHub 이슈 트래커에 등록해주시면 됩니다.

---

이 문서의 내용이 프로젝트의 구조와 설정을 이해하는 데 도움이 되기를 바랍니다. 추가적인 질문이나 도움이 필요하시면 언제든지 문의해주세요.
