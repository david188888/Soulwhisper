'use strict';
const db = uniCloud.database()
exports.main = async (event, context) => {
	const{
		name,
		page = 1,
		pageSize = 6
	} = event
	// var name = event.name 一样的
	
	let matchObj = {}
	if(name !== '全部'){
		matchObj = {
			classify: name
		}
	}
	
	//聚合
	const list = await db.collection('article')
	.aggregate()
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
