const baseUrl = 'http://127.0.0.1:8000/';

export const api = {
    register: `${baseUrl}api/account/register/`,
    login: `${baseUrl}api/account/login/`,
    asr: `${baseUrl}api/diary/asr/`,
    dairyCreate: `${baseUrl}api/diary/diaries/create/`,
    diaryStatistics: `${baseUrl}api/diary/statistics/`,
    diaryDays: `${baseUrl}api/diary/days/`,
    diaryDayDetail: `${baseUrl}api/diary/day_detail/`,
}