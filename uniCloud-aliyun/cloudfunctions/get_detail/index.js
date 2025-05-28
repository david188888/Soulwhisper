'use strict';
const db = uniCloud.database()
const $ = db.command.aggregate
exports.main = async (event, context) => {
	const{
		user_id,
		article_id
	} = event
	
	let user = await db.collection('user').doc(user_id).get()
	user = user.data[0]
	let list = await db.collection('article')
	.aggregate()
	.addFields({
		//Whether to follow the author
		is_author_like:$.in(['$author.id',user.author_likes_ids]),
		//Whether to collect the article
		is_like:$.in(['$_id',user.article_likes_ids]),
		//Whether to like or not
		is_thumbs_up:$.in(['$_id',user.thumbs_up_article_ids])
	})
	.match({
		_id:article_id
	})
	.project({
		comments:0
	})
	.end()
	return {
		code:200,
		msg:'The data request was successful.',
		data: list.data[0]
	}
};
