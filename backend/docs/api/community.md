# 社区接口(Community)

## 每日内容 (Daily Content)

### 获取每日内容 (Get Daily Content)
- HTTP Method and Endpoint: GET /api/community/daily-content
- 数据库操作: 从 DailyKeyword、HealingQuote 和 HealingActivity 表中随机获取一条活跃记录
- 响应数据:
```json
{
    "date": "2024-01-01",
    "keyword": {
        "id": "keyword_id",
        "keyword": "关键词",
        "description": "关键词描述"
    },
    "quote": {
        "id": "quote_id",
        "content": "治愈短句内容",
        "author": "作者"
    },
    "activity": {
        "id": "activity_id",
        "title": "活动标题",
        "description": "活动描述",
        "duration": 30,
        "difficulty": "easy"
    }
}
```

## 每日关键词 (Daily Keywords)

### (1) 获取关键词列表 (Get Keyword List)
- HTTP Method and Endpoint: GET /api/community/keywords/list
- 数据库操作: 查询 DailyKeyword 表，获取所有关键词
- 响应数据:
```json
[
    {
        "id": "keyword_id",
        "keyword": "关键词",
        "description": "关键词描述",
        "is_active": true,
        "created_at": "2024-01-01 12:00:00"
    }
]
```

### (2) 创建关键词 (Create Keyword)
- HTTP Method and Endpoint: POST /api/community/keywords/create
- 请求体:
```json
{
    "keyword": "关键词",
    "description": "关键词描述"
}
```
- 数据库操作: 插入 DailyKeyword 表，创建新的关键词
- 响应数据:
```json
{
    "id": "keyword_id",
    "keyword": "关键词",
    "description": "关键词描述",
    "is_active": true,
    "created_at": "2024-01-01 12:00:00"
}
```

### (3) 获取关键词详情 (Get Keyword Detail)
- HTTP Method and Endpoint: GET /api/community/keywords/detail
- 请求体:
```json
{
    "keyword_id": "keyword_id"
}
```
- 数据库操作: 查询 DailyKeyword 表，获取指定 keyword_id 的关键词详情
- 响应数据:
```json
{
    "id": "keyword_id",
    "keyword": "关键词",
    "description": "关键词描述",
    "is_active": true,
    "created_at": "2024-01-01 12:00:00"
}
```

### (4) 更新关键词 (Update Keyword)
- HTTP Method and Endpoint: PUT /api/community/keywords/update
- 请求体:
```json
{
    "keyword_id": "keyword_id",
    "keyword": "更新后的关键词",
    "description": "更新后的描述",
    "is_active": true
}
```
- 数据库操作: 更新 DailyKeyword 表中指定 keyword_id 的记录
- 响应数据:
```json
{
    "id": "keyword_id",
    "keyword": "更新后的关键词",
    "description": "更新后的描述",
    "is_active": true,
    "created_at": "2024-01-01 12:00:00"
}
```

### (5) 删除关键词 (Delete Keyword)
- HTTP Method and Endpoint: DELETE /api/community/keywords/delete
- 请求体:
```json
{
    "keyword_id": "keyword_id"
}
```
- 数据库操作: 从 DailyKeyword 表中删除指定 keyword_id 的记录
- 响应数据: 204 No Content

## 治愈短句 (Healing Quotes)

### (1) 获取短句列表 (Get Quote List)
- HTTP Method and Endpoint: GET /api/community/quotes/list
- 数据库操作: 查询 HealingQuote 表，获取所有治愈短句
- 响应数据:
```json
[
    {
        "id": "quote_id",
        "content": "治愈短句内容",
        "author": "作者",
        "is_active": true,
        "created_at": "2024-01-01 12:00:00"
    }
]
```

### (2) 创建短句 (Create Quote)
- HTTP Method and Endpoint: POST /api/community/quotes/create
- 请求体:
```json
{
    "content": "治愈短句内容",
    "author": "作者"
}
```
- 数据库操作: 插入 HealingQuote 表，创建新的治愈短句
- 响应数据:
```json
{
    "id": "quote_id",
    "content": "治愈短句内容",
    "author": "作者",
    "is_active": true,
    "created_at": "2024-01-01 12:00:00"
}
```

### (3) 获取短句详情 (Get Quote Detail)
- HTTP Method and Endpoint: GET /api/community/quotes/detail
- 请求体:
```json
{
    "quote_id": "quote_id"
}
```
- 数据库操作: 查询 HealingQuote 表，获取指定 quote_id 的短句详情
- 响应数据:
```json
{
    "id": "quote_id",
    "content": "治愈短句内容",
    "author": "作者",
    "is_active": true,
    "created_at": "2024-01-01 12:00:00"
}
```

### (4) 更新短句 (Update Quote)
- HTTP Method and Endpoint: PUT /api/community/quotes/update
- 请求体:
```json
{
    "quote_id": "quote_id",
    "content": "更新后的短句内容",
    "author": "更新后的作者",
    "is_active": true
}
```
- 数据库操作: 更新 HealingQuote 表中指定 quote_id 的记录
- 响应数据:
```json
{
    "id": "quote_id",
    "content": "更新后的短句内容",
    "author": "更新后的作者",
    "is_active": true,
    "created_at": "2024-01-01 12:00:00"
}
```

### (5) 删除短句 (Delete Quote)
- HTTP Method and Endpoint: DELETE /api/community/quotes/delete
- 请求体:
```json
{
    "quote_id": "quote_id"
}
```
- 数据库操作: 从 HealingQuote 表中删除指定 quote_id 的记录
- 响应数据: 204 No Content

## 治愈活动 (Healing Activities)

### (1) 获取活动列表 (Get Activity List)
- HTTP Method and Endpoint: GET /api/community/activities/list
- 数据库操作: 查询 HealingActivity 表，获取所有治愈活动
- 响应数据:
```json
[
    {
        "id": "activity_id",
        "title": "活动标题",
        "description": "活动描述",
        "duration": 30,
        "difficulty": "easy",
        "is_active": true,
        "created_at": "2024-01-01 12:00:00"
    }
]
```

### (2) 创建活动 (Create Activity)
- HTTP Method and Endpoint: POST /api/community/activities/create
- 请求体:
```json
{
    "title": "活动标题",
    "description": "活动描述",
    "duration": 30,
    "difficulty": "easy"
}
```
- 数据库操作: 插入 HealingActivity 表，创建新的治愈活动
- 响应数据:
```json
{
    "id": "activity_id",
    "title": "活动标题",
    "description": "活动描述",
    "duration": 30,
    "difficulty": "easy",
    "is_active": true,
    "created_at": "2024-01-01 12:00:00"
}
```

### (3) 获取活动详情 (Get Activity Detail)
- HTTP Method and Endpoint: GET /api/community/activities/detail
- 请求体:
```json
{
    "activity_id": "activity_id"
}
```
- 数据库操作: 查询 HealingActivity 表，获取指定 activity_id 的活动详情
- 响应数据:
```json
{
    "id": "activity_id",
    "title": "活动标题",
    "description": "活动描述",
    "duration": 30,
    "difficulty": "easy",
    "is_active": true,
    "created_at": "2024-01-01 12:00:00"
}
```

### (4) 更新活动 (Update Activity)
- HTTP Method and Endpoint: PUT /api/community/activities/update
- 请求体:
```json
{
    "activity_id": "activity_id",
    "title": "更新后的活动标题",
    "description": "更新后的活动描述",
    "duration": 45,
    "difficulty": "medium",
    "is_active": true
}
```
- 数据库操作: 更新 HealingActivity 表中指定 activity_id 的记录
- 响应数据:
```json
{
    "id": "activity_id",
    "title": "更新后的活动标题",
    "description": "更新后的活动描述",
    "duration": 45,
    "difficulty": "medium",
    "is_active": true,
    "created_at": "2024-01-01 12:00:00"
}
```

### (5) 删除活动 (Delete Activity)
- HTTP Method and Endpoint: DELETE /api/community/activities/delete
- 请求体:
```json
{
    "activity_id": "activity_id"
}
```
- 数据库操作: 从 HealingActivity 表中删除指定 activity_id 的记录
- 响应数据: 204 No Content 