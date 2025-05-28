'use strict';
const db = uniCloud.database()
const $ = db.command.aggregate
exports.main = async (event, context) => {
	const{
		user_id,
		article_id,
		pageSize=5,
		page = 1
	} = event
	const list = await db.collection('article')
	.aggregate()
	.match({
		_id:article_id
	})
	.unwind('$comments')
	.project({
		_id:0,
		comments:1
	})
	.replaceRoot({
		newRoot:'$comments'
	})
	.skip(pageSize*(page-1))
	.limit(pageSize)
	.end()
	
	return {
		code:200,
		msg:'The data request was successful.',
		data:list.data
	}
};
