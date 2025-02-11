# django-travelog

Travelog - Django로 만든 여행 블로그

Django를 활용한 여행 블로그 플랫폼으로, 사용자별 채널과 구독 기능을 통해 여행 포스트를 작성하고 공유할 수 있는 서비스입니다.

## 주요 기능

1. 사용자/채널 시스템

- 회원가입/로그인 (닉네임 = 채널명)
- 채널명 변경 기능
- 비밀번호 변경 기능
- 나의 구독 채널 리스트

2. 포스트 시스템

- 일반/구독자 전용 포스트 작성
- 포스트 조회수 추적
- 연재물(시리즈) 생성
- 카테고리 분류(여행 지역)
- 댓글 기능
- 대댓글 기능
- 태그 달기
- 검색 기능

3. 채널 관리 기능

- 나의 구독자 목록 조회
- 인기 포스트 TOP 3 노출(조회수 기준)
- 연재물 목록 표시
- 포스트 목록 표시

## 기술 스택

- Backend: Python >= 3.11, Django
- Frontend: Django Template + Bootstrap, TinyMCE(에디터 기능), django-taggit(태그 기능)
- Database: PostgreSQL

## API 명세

### 계정 관련 API

| 메서드 | URL 패턴                   | 기능                | 인증 필요 | Parameter/Body                                                |
| ------ | -------------------------- | ------------------- | --------- | ------------------------------------------------------------- |
| POST   | /accounts/register/        | 회원가입            | No        | 폼: `username`, `password1`, `password2`, `nickname`, `email` |
| POST   | /accounts/login/           | 로그인              | No        | 폼: `username`, `password`                                    |
| POST   | /accounts/logout/          | 로그아웃            | Yes       | -                                                             |
| GET    | /accounts/profile/         | 프로필 조회         | Yes       | -                                                             |
| POST   | /accounts/password/change/ | 비밀번호 변경       | Yes       | 폼: `old_password`, `new_password1`, `new_password2`          |
| POST   | /accounts/nickname/change  | 닉네임(채널명) 변경 | Yes       | 폼: `nickname`                                                |

### 블로그 관련 API

| 메서드 | URL 패턴           | 기능             | 인증 필요 | Parameter/Body                                                                               |
| ------ | ------------------ | ---------------- | --------- | -------------------------------------------------------------------------------------------- |
| GET    | /blog              | 포스트 목록 조회 | No        | Query: `q` (검색어, optional)                                                                |
| GET    | /blog/{pk}/        | 포스트 상세 조회 | No\*      | -                                                                                            |
| POST   | /blog/write/       | 새 포스트 작성   | Yes       | 폼: `title`, `content`, `category`, `series`, `thumbnail_img`, `is_subscribers_only`, `tags` |
| POST   | /blog/edit/{pk}/   | 포스트 수정      | Yes\*\*   | 폼: `title`, `content`, `category`, `series`, `thumbnail_img`, `is_subscribers_only`, `tags` |
| POST   | /blog/delete/{pk}/ | 포스트 삭제      | Yes\*\*   | -                                                                                            |

\* 구독자 전용 포스트는 구독자만 접근 가능
\*\* 작성자만 가능

### 채널 관련 API

| Method | URL Pattern              | Description    | Auth Required | Parameters/Body |
| ------ | ------------------------ | -------------- | ------------- | --------------- |
| GET    | /blog/channel/{nickname} | 특정 채널 조회 | No            | -               |
| POST   | /blog/subscribe/         | 채널 구독      | Yes           | 폼: `nickname`  |
| POST   | /blog/unsubscribe/       | 채널 구독 취소 | Yes           | 폼: `nickname`  |

### 연재물 관련 API

| 메서드 | URL 패턴                  | 기능           | 인증 필요 | Parameter/Body            |
| ------ | ------------------------- | -------------- | --------- | ------------------------- |
| POST   | /blog/series/write/       | 새 연재물 생성 | Yes       | 폼: `name`, `description` |
| POST   | /blog/series/edit/{pk}/   | 연재물 수정    | Yes\*     | 폼: `name`, `description` |
| POST   | /blog/series/delete/{pk}/ | 연재물 삭제    | Yes\*     | -                         |

\* 작성자만 가능

### 댓글 API

| 메서드 | URL 패턴                       | 기능      | 인증 필요 | Parameter/Body |
| ------ | ------------------------------ | --------- | --------- | -------------- |
| POST   | /blog/{post_pk}/comments/write | 댓글 작성 | Yes       | 폼: `content`  |
| POST   | /blog/comments/{pk}/edit       | 댓글 수정 | Yes\*     | 폼: `content`  |
| POST   | /blog/comments/{pk}/delete     | 댓글 삭제 | Yes\*     | -              |

\* 작성자만 가능

### 대댓글 API

| 메서드 | URL 패턴                       | 기능        | 인증 필요 | Parameter/Body |
| ------ | ------------------------------ | ----------- | --------- | -------------- |
| POST   | /blog/comments/{post_pk}/write | 대댓글 작성 | Yes       | 폼: `content`  |
| POST   | /blog/reply/{pk}/edit          | 대댓글 수정 | Yes\*     | 폼: `content`  |
| POST   | /blog/reply/{pk}/delete        | 대댓글 삭제 | Yes\*     | -              |

\* 작성자만 가능
