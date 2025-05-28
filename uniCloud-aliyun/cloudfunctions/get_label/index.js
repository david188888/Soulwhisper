'use strict';
const db = uniCloud.database()
exports.main = async (event, context) => {
	
	let label = await db.collection('label').get()

	return {
		code:200,
		msg:'The data request was successful.',
		data: label.data
	}
};
