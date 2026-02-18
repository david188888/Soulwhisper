# Visualization Statistics Features

This document describes the visualization and statistics features in SoulWhisper, linking the implementation across backend and frontend.

## Overview

SoulWhisper provides emotional data visualization and statistics to help users understand their emotional patterns over time. The system analyzes diary entries and generates:

1. **Word Cloud** - Visual representation of frequently used words in diaries
2. **Emotion Distribution** - Statistical breakdown of emotion types (happy, sad, angry, neutral)
3. **Weekly Reports** - Aggregated data from the last 7 days

## Backend Implementation

### API Endpoints

All visualization statistics endpoints are defined in `/backend/apps/diary/urls.py`:

#### 1. Diary Statistics API
- **Endpoint**: `/api/diary/statistics/`
- **Method**: GET
- **Authentication**: Required (Token-based)
- **Implementation**: `DiaryStatisticsView` in `/backend/apps/diary/views.py` (lines 348-444)
- **Returns**:
  - `wordcloud`: Base64-encoded PNG image of word cloud
  - `emotion_stats`: Dictionary with emotion type counts (happy, sad, angry, neutral)

**Features**:
- Analyzes diaries from the last 7 days
- Generates word cloud using NLTK tokenization and WordCloud library
- Filters out stop words (articles, conjunctions, prepositions, pronouns, common verbs)
- Only includes words longer than 2 characters
- Counts emotion distribution across all diaries in the time period

#### 2. Emotion Analysis API
- **Endpoint**: `/api/diary/emotion-analysis/`
- **Method**: GET
- **Authentication**: Required
- **Implementation**: `EmotionAnalysisView` in `/backend/apps/diary/views.py` (lines 300-318)
- **Uses**: `EmotionAnalyzer` class from `/backend/apps/diary/emotion_analyzer.py`

#### 3. Word Cloud API
- **Endpoint**: `/api/diary/word-cloud/`
- **Method**: GET
- **Authentication**: Required
- **Implementation**: `WordCloudView` in `/backend/apps/diary/views.py` (lines 320-346)
- **Returns**:
  - `word_cloud`: Base64-encoded word cloud image
  - `keywords`: List of extracted keywords

#### 4. Diary Days API
- **Endpoint**: `/api/diary/days/`
- **Method**: GET
- **Parameters**: `year`, `month`
- **Authentication**: Required
- **Implementation**: `DiaryDaysView` in `/backend/apps/diary/views.py` (lines 446-483)
- **Returns**: List of dates (YYYY-MM-DD format) when user has diary entries

#### 5. Diary Day Detail API
- **Endpoint**: `/api/diary/day_detail/`
- **Method**: GET
- **Parameters**: `date` (YYYY-MM-DD format)
- **Authentication**: Required
- **Implementation**: `DiaryDayDetailView` in `/backend/apps/diary/views.py` (lines 485-542)
- **Returns**: Diary content and emotion data for a specific date

### Dependencies

The visualization features use the following Python libraries:

```python
# From requirements.txt
matplotlib==3.7.1        # For generating charts and images
wordcloud==1.9.2         # For word cloud generation
nltk==3.8.1             # For text tokenization and stop words
numpy==1.24.3           # For numerical operations (used by matplotlib)
```

## Frontend Implementation

### Main Visualization Component

**File**: `/frontend/pages/tabbar/tabbar-2/tabbar-2.vue`

This is the primary UI component for displaying visualization statistics. It shows:

1. **Emotional Keyword Cloud** (lines 7-13)
   - Displays the word cloud image from the backend
   - Shows loading state while fetching data
   - Uses base64-encoded image with proper MIME type

2. **Mood Distribution Pie Chart** (lines 15-24)
   - Uses `qiun-data-charts` component (uni-app chart library)
   - Displays emotion statistics in a pie chart format
   - Configured with custom colors for each emotion type
   - Shows interactive pie chart with active states

### Frontend Logic

**Data Fetching** (lines 64-111):
- `fetchStatistics()` method calls the `/api/diary/statistics/` endpoint
- Requires authentication token from local storage
- Transforms backend data into chart-compatible format
- Maps emotion types to human-readable labels

**Emotion Configuration** (lines 52-57):
```javascript
emotionConfig: {
    happy: { label: 'happy' },
    angry: { label: 'angry' },
    sad: { label: 'sad' },
    neutral: { label: 'neutral' }
}
```

**Chart Configuration** (lines 35-51):
- Custom color palette for different emotions
- Pie chart with active radius and border
- Responsive layout with proper padding

### API Path Configuration

**File**: `/frontend/components/api/apiPath.js`

The visualization statistics endpoint is registered in the API path configuration:
```javascript
diaryStatistics: `${BASE_URL}/api/diary/statistics/`
```

## Data Flow

```
User Opens Statistics Page
        ↓
Frontend (tabbar-2.vue) - onShow() triggered
        ↓
Call fetchStatistics()
        ↓
GET /api/diary/statistics/ (with auth token)
        ↓
Backend DiaryStatisticsView
        ↓
Query MongoDB for last 7 days of diaries
        ↓
Generate Word Cloud (matplotlib + wordcloud)
        ↓
Count Emotion Distribution (Django ORM)
        ↓
Return JSON response:
  - wordcloud: base64 PNG
  - emotion_stats: {happy: n, sad: m, ...}
        ↓
Frontend receives data
        ↓
Display word cloud image
        ↓
Render pie chart with qiun-data-charts
        ↓
User sees visualization
```

## Feature Characteristics

### Time Range
- **Default**: Last 7 days from current date
- Calculated using `timezone.now() - timedelta(days=7)`

### Word Cloud Generation
- **Image Size**: 800x400 pixels
- **Max Words**: 50
- **Font Size Range**: 12-60
- **Background**: White
- **Horizontal Preference**: 70%
- **Output Format**: PNG, Base64-encoded
- **DPI**: 300 (high quality)

### Emotion Statistics
- **Supported Emotions**: happy, sad, angry, neutral
- **Default Values**: All emotions initialized to 0 if no data
- **Counting Method**: Django ORM `Count` aggregation

### Text Processing
- Uses NLTK word tokenizer
- Filters out English stop words (articles, conjunctions, prepositions, pronouns, common verbs)
- Only includes alphanumeric tokens
- Minimum word length: 3 characters

## Error Handling

### Backend
- Returns 404 if no diary data available
- Returns 500 with error message on processing failures
- Logs all errors with detailed traceback

### Frontend
- Shows toast notification for authentication errors
- Displays error messages for network failures
- Shows "Loading..." state during data fetch
- Handles empty data gracefully

## Related Pull Requests

Currently, there are no open pull requests specifically about visualization statistics features. 

- **PR #1** ("修改requirements.txt 尝试pr") - Modified requirements.txt, which may affect visualization dependencies if it updated matplotlib, wordcloud, or nltk versions.

## Future Enhancements

Potential improvements to the visualization statistics system:

1. **Customizable Time Ranges** - Allow users to select different date ranges (30 days, 90 days, all time)
2. **Trend Charts** - Line graphs showing emotion changes over time
3. **Comparative Analysis** - Compare different time periods
4. **Export Functionality** - Download visualizations as images or PDFs
5. **Multiple Language Support** - Word cloud generation for non-English diaries
6. **Interactive Charts** - More detailed filtering and drill-down capabilities
7. **Real-time Updates** - Automatic refresh when new diary entries are added

## Technical Notes

### Authentication
All visualization endpoints require token-based authentication:
```
Authorization: Token <user_token>
```

### Performance Considerations
- Word cloud generation is CPU-intensive; may take 1-2 seconds for large datasets
- Consider caching word clouds if diary content hasn't changed
- Database queries are optimized with date range filters

### Testing
To test visualization features:
1. Ensure MongoDB is running
2. Create diary entries with different emotion types
3. Wait for entries to span multiple days
4. Access the statistics page (tabbar-2)
5. Verify word cloud displays correctly
6. Verify pie chart shows emotion distribution

## Dependencies Graph

```
Frontend (tabbar-2.vue)
    ↓ depends on
qiun-data-charts (chart library)
    ↓ calls
API (/api/diary/statistics/)
    ↓ implemented by
DiaryStatisticsView (Django)
    ↓ depends on
├── matplotlib (chart generation)
├── wordcloud (word cloud generation)
├── nltk (text processing)
├── Django ORM (database queries)
└── Diary Model (data source)
```

## Related Files

### Backend
- `/backend/apps/diary/views.py` - All API view implementations
- `/backend/apps/diary/urls.py` - URL routing configuration
- `/backend/apps/diary/models.py` - Diary model definition
- `/backend/apps/diary/emotion_analyzer.py` - Emotion analysis logic

### Frontend
- `/frontend/pages/tabbar/tabbar-2/tabbar-2.vue` - Main visualization UI
- `/frontend/components/api/apiPath.js` - API endpoint configuration
- `/frontend/common/http.js` - HTTP client configuration

### Configuration
- `/requirements.txt` - Python dependencies
- `/backend/config/settings.py` - Django settings

## Conclusion

The visualization statistics feature provides users with meaningful insights into their emotional patterns through word clouds and emotion distribution charts. The system is built on robust libraries (matplotlib, wordcloud, nltk) and follows RESTful API design principles with proper authentication and error handling.
