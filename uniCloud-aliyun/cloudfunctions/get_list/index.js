'use strict';
//获取数据库引用
const db = uniCloud.database()
const $ = db.command.aggregate
exports.main = async (event, context) => {
	const{
		user_id,
		name,
		page = 1,
		pageSize = 6
	} = event
	// var name = event.name 一样的
	
	let matchObj = {}
	if(name !== 'All'){
		matchObj = {
			classify: name
		}
	}
	
	const userinfo = await db.collection('user').doc(user_id).get()
	const article_likes_ids = userinfo.data[0].article_likes_ids
	
	//聚合
	const list = await db.collection('article')
	.aggregate()
	//追加字段
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
	//接收分类进行筛选
	// const list = await db.collection('article')
	// .field({
	// 	content:false
	// })
	// .get()
	return {
		code:200,
		msg:'数据请求成功',
		data: list.data
	}
};
