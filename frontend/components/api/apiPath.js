const baseUrl = 'http://127.0.0.1:8000/';
<<<<<<< HEAD
=======
const diaryListUrl = 'http://127.0.0.1:8000/';
>>>>>>> master

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
<<<<<<< HEAD
    chatEnd: `${baseUrl}api/chat/end/`
=======
    chatEnd: `${baseUrl}api/chat/end/`,
	community: `${baseUrl}api/community/daily-content/`,
	comment: `${baseUrl}api/community/diaries/{diary_id}/comments/`,
	createComment: `${baseUrl}api/community/diaries/{diary_id}/comments/create/`,
	updateComment: `/api/community/comments/{comment_id}/update/`,
	deleteComment: `/api/community/comments/{comment_id}/delete/`,
>>>>>>> master
}