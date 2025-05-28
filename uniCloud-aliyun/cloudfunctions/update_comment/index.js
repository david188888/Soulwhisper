'use strict';
const db = uniCloud.database()
const $ = db.command.aggregate
const dbCmd = db.command

exports.main = async (event, context) => {
	const{
		user_id,
		article_id='682d74aec3b5c9ba15dda8ef',
		content,
		comment_id='',
		reply_id="",
		is_reply = false
	} = event
	
	let user = await db.collection('user').doc(user_id).get()
	user = user.data[0]
	// Get the current article
	const article = await db.collection('article').doc(article_id).get()
	// Get all the comments under the article
	const comments = article.data[0].comments
	
	let commentObj = {
		comment_id:genID(5),
		comment_content:content,
		create_time: new Date().getTime(),
		is_reply:is_reply,
		author:{
			author_id:user._id,
			author_name:user.author_name,
			avatar:user.avatar,
			professional:user.professional
		},
		replys:[]
	}
	
	// Comment on the article
	if (comment_id === ''){
		commentObj.replys = []
		commentObj = dbCmd.unshift(commentObj)
	}else{
		// Reply to the comments on the article
		// Get the comment index
		let commentIndex = comments.findIndex(item => item.comment_id === comment_id)
		//
		let commentAuthor = ''
		if(is_reply){
			// Sub-reply
			commentAuthor = comments[commentIndex].replys.find(item=>item.comment_id === reply_id)
		}else{
			// Main reply
			// Obtain author information
			commentAuthor = comments.find(item => item.comment_id === comment_id)
		}
		commentAuthor = commentAuthor.author.author_name
		commentObj.to = commentAuthor		
		// Update the reply information
		commentObj = {
			[commentIndex]: {
				replys: dbCmd.unshift(commentObj)
			}
		}
	}
	
	await db.collection('article').doc(article_id).update({
		comments:commentObj
	})
	
	return {
		code:200,
		msg:'The data request was successful.'
	}
};

function genID(length){
	return Number(Math.random().toString().substring(3,length) +Date.now()).toString(36)
}
