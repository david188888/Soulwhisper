import $http from "../http.js"

export const get_label = (data) =>{
	return $http({
		url:'get_label',
		data
	})
}

export const get_list = (data) =>{
	return $http({
		url:'get_list',
		data
	})
}

export const update_like = (data) =>{
	return $http({
		url:'update_like',
		data
	})
}

export const get_detail= (data) =>{
	return $http({
		url:'get_detail',
		data
	})
}

export const update_comment= (data) =>{
	return $http({
		url:'update_comment',
		data
	})
}

export const get_comments= (data) =>{
	return $http({
		url:'get_comments',
		data
	})
}

export const update_author= (data) =>{
	return $http({
		url:'update_author',
		data
	})
}

export const update_thumbsup= (data) =>{
	return $http({
		url:'update_thumbsup',
		data
	})
}

export const update_article= (data) =>{
	return $http({
		url:'update_article',
		data
	})
}
