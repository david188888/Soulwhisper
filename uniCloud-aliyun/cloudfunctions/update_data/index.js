'use strict';
const db = uniCloud.database()
exports.main = async (event, context) => {
	const collection = db.collection('user')
	const res = await collection.doc('682d74b08a5c782a2b825fdd').update({
		author_likes_ids:["682d74b08a5c782a2b825fde"]
	})
	
	//返回数据给客户端
	return {}
};
