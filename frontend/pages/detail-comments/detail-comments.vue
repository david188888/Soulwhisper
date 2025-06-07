<template>
	<view>
		<view>
			<view class="comments-content" v-for="item in commentsList" :key="item.comment_id">
				<commentsBox :comments="item"></commentsBox>
			</view>
		</view>
		<uni-load-more v-if="commentsList.length === 0 || commentsList.length >5 " :icon-type="snow" :status="onload"></uni-load-more>
	</view>
</template>

<script>
	import commentsBox from '@/frontend/components/commentsBox/commentsBox.vue';
	export default{
		components:{
			commentsBox,
		},
		data(){
			return{
				commentsList:[],
				article_id:'',
				page:1,
				pageSize:5,
				onload:'loading'
			}
		},
		onLoad(query){
			this.article_id = query.id
			console.log(query);
			this.getComments()
		},
		onReachBottom() {
			if(this.onload = 'noMore') return
			this.page++
			this.getComments()
			console.log('Pull up and touch the bottom');
		},
		methods:{
			getComments(){
				this.$api.get_comments({
					article_id:this.article_id,
					page:this.page,
					pageSize:this.pageSize
				}).then(res=>{
					const {data} = res
					console.log(res);
					if(data.length === 0){
						this.onload = 'noMore'
						return
					}
					// Object copying
					let oldFromData = JSON.parse(JSON.stringify(this.commentsList))
					oldFromData.push(...data)
					this.commentsList = oldFromData
				})
			}
		}
	}
</script>

<style lang="scss">
	.comments-content{
		padding: 0 15px;
	}
</style>