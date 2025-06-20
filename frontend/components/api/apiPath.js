const baseUrl = 'http://43.133.190.180:8000/';

export const api = {
    register: `${baseUrl}api/account/register/`,
    login: `${baseUrl}api/account/login/`,
    asr: `${baseUrl}api/diary/asr/`,
    dairyCreate: `${baseUrl}api/diary/diaries/create/`,
    diaryStatistics: `${baseUrl}api/diary/statistics/`,
    diaryDays: `${baseUrl}api/diary/days/`,
    diaryDayDetail: `${baseUrl}api/diary/day_detail/`,
    chatStart: `${baseUrl}api/chat/start/`,
    chatMessage: `${baseUrl}api/chat/message/`,
    chatEnd: `${baseUrl}api/chat/end/`,
	community: `${baseUrl}api/community/daily-content/`,
	comment: `${baseUrl}api/community/diaries/{diary_id}/comments/`,
	createComment: `${baseUrl}api/community/diaries/{diary_id}/comments/create/`,
	updateComment: `/api/community/comments/{comment_id}/update/`,
	deleteComment: `/api/community/comments/{comment_id}/delete/`,
	dailyContent: `${baseUrl}api/community/daily-content/`,
}