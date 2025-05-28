'use strict';
const db = uniCloud.database()
const $ = db.command.aggregate
exports.main = async (event, context) => {
	const{
		user_id,
		name,
		page = 1,
		pageSize = 6
	} = event
	// var name = event.name the same
	
	let matchObj = {}
	if(name !== 'All'){
		matchObj = {
			classify: name
		}
	}
	
	const userinfo = await db.collection('user').doc(user_id).get()
	const article_likes_ids = userinfo.data[0].article_likes_ids
	
	//aggregation
	const list = await db.collection('article')
	.aggregate()
	// Append fields
	.addFields({
		is_like:$.in(['$_id',article_likes_ids])
	})
	.match(matchObj)
	.project({
		content:0
	})
	.skip(pageSize*(page-1))
	.limit(pageSize)
	.end()
	// Receive the classification for filtering
	// const list = await db.collection('article')
	// .field({
	// 	content:false
	// })
	// .get()
	return {
		code:200,
		msg:'The data request was successful.',
		data: list.data
	}
};
