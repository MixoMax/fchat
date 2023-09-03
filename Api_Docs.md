# FChat API Documentation

## Table of Contents

- User handling Apis
- Chat Apis
- Message Apis

## User handling Apis
### /api/user/create
Creates a new user and returns the user id and the auth token.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| username | string | The username of the user |
|Email | string | The email of the user |
| password | string | The password of the user |

### /api/user/login
Logs in a user and returns the user id and the auth token.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| username or email | string | The username or email of the user |
| password | string | The password of the user |

return:
auth_token: string
user_id: int

## Chat Apis
### /api/chat/create
Creates a new chat and returns the chat id.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| name | string | The name of the chat |