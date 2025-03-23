# 日记接口(Diary)

## (1) 获取日记列表 (Get Diary List)
* HTTP Method and Endpoint: GET /api/diary/diaries/
* 数据库操作: 查询 Diary 表，获取所有日记记录
* 响应数据:
```json
[
    {
        "id": "diary_id",
        "content": "Today was a good day...",
        "emotion_type": "happy",
        "emotion_intensity": 8,
        "created_at": "2024-01-01 12:00:00"
    }
]
```

## (2) 创建日记 (Create Diary)
* HTTP Method and Endpoint: POST /api/diary/diaries/create
* 请求体:
```json
{
    "content": "Today was a good day...",
    "emotion_type": "happy",
    "emotion_intensity": 8
}
```
* 数据库操作: 插入 Diary 表，创建新的日记记录
* 响应数据:
```json
{
    "id": "diary_id",
    "content": "Today was a good day...",
    "emotion_type": "happy",
    "emotion_intensity": 8,
    "created_at": "2024-01-01 12:00:00"
}
```

## (3) 获取日记详情 (Get Diary Detail)
* HTTP Method and Endpoint: GET /api/diary/diaries/detail
* 请求体:
```json
{
    "diary_id": "diary_id"
}
```
* 数据库操作: 查询 Diary 表，获取指定 diary_id 的日记详情
* 响应数据:
```json
{
    "id": "diary_id",
    "content": "Today was a good day...",
    "emotion_type": "happy",
    "emotion_intensity": 8,
    "created_at": "2024-01-01 12:00:00"
}
```

## (4) 更新日记 (Update Diary)
* HTTP Method and Endpoint: PUT /api/diary/diaries/update
* 请求体:
```json
{
    "diary_id": "diary_id",
    "content": "Updated diary content...",
    "emotion_type": "sad",
    "emotion_intensity": 3
}
```
* 数据库操作: 更新 Diary 表中指定 diary_id 的记录
* 响应数据:
```json
{
    "id": "diary_id",
    "content": "Updated diary content...",
    "emotion_type": "sad",
    "emotion_intensity": 3,
    "created_at": "2024-01-01 12:00:00"
}
```

## (5) 删除日记 (Delete Diary)
* HTTP Method and Endpoint: DELETE /api/diary/diaries/delete
* 请求体:
```json
{
    "diary_id": "diary_id"
}
```
* 数据库操作: 从 Diary 表中删除指定 diary_id 的记录
* 响应数据: 204 No Content

## (6) 语音识别创建日记 (ASR Create Diary)
* HTTP Method and Endpoint: POST /api/diary/asr/
* 请求体:
```
Content-Type: multipart/form-data
audio_file: [音频文件]
```
* 数据库操作: 处理音频文件，识别文本内容，创建新的日记记录
* 响应数据:
```json
{
    "id": "diary_id",
    "content": "识别的文本内容...",
    "emotion_type": "neutral",
    "emotion_intensity": 5,
    "created_at": "2024-01-01 12:00:00"
}
``` 