'use strict';
const db = uniCloud.database()
const dbCmd = db.command;
exports.main = async (event, context) => {
	const{
		user_id,
		content = '',
		title,
	    classify,
		cover = []
	} = event
	
	    const userRes = await db.collection('user').doc(user_id).get();
	    if (!userRes.data || userRes.data.length === 0) {
	      return {
	        code: 404,
	        msg: 'User not found'
	      };
	    }
	    const user = userRes.data[0];

	    const articleId = `A${Date.now().toString().slice(2)}`;
	
	    const now = new Date();
	    const createTime = `${now.getFullYear()}.${(now.getMonth() + 1).toString().padStart(2, '0')}.${now.getDate().toString().padStart(2, '0')} ${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
	
	    // Build article data
	    const articleData = {
	      id: articleId,
	      title,
	      browse_count: 0,
	      collection_count: 0,
	      comments_count: [],
	      author: {
	        id: user_id,
	        author_name: user.username,
	        avatar: user.avatar || '',
	        status: user.status || 'normal'
	      },
	      classify,
	      thumbs_up_count: 0,
	      create_time: createTime,
	      content,
	      cover,
	    };
	
	    //Insert article data
	    const addResult = await db.collection('article').add(articleData);
		
	return{
			code:200,
			msg:'The data request was successful.'
	}
};
