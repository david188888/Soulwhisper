export default function $http(options){
	const{
		url,
		data
	} = options
	const dataObj = {
		user_id:'6826a345652341756209a423',
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