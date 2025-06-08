'use strict';
const db = uniCloud.database()
exports.main = async (event, context) => {
	const collection = db.collection('user')
	const res = await collection.doc('6843f546fe975fd64c494da7').update({
		author_likes_ids:["682d74b08a5c782a2b825fde"]
	})

	return {}
};
