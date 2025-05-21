export default function $http(options){
	const{
		url,
		data
	} = options
	const dataObj = {
		//如果更新数据库，确保有这个user_id
		user_id:'682d74b08a5c782a2b825fdd',
		...data
	}
	return new Promise((reslove,reject)=>{
		uniCloud.callFunction({
			name:url,
			data:dataObj
		}).then((res)=>{
			if(res.result.code === 200){
				reslove(res.result)
			}else{
				reject(res.result)
			}
		}).catch((err)=>{
			reject(err)
		})
	})
}