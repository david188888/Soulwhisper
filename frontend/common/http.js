export default function $http(options){
	const{
		url,
		data
	} = options
	const dataObj = {
		// If the database is updated, make sure that there is the user_id in the database.
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