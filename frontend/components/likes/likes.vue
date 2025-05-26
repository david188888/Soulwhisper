<template>
	<view class="icons" @click.stop="likeTap">
		<uni-icons :type="like?'heart-filled':'heart'" size="20px" color="#f07373"></uni-icons>
	</view>
</template>

<script>
	export default{
		props:{
			item:{
				type:Object,
				default(){
					return {}
				}
			}
		},
		data(){
			return{
				like:false
			};
		},
		watch:{
			item(newVal){
				this.like = this.item.is_like
			}
		},
		created() {
			this.like = this.item.is_like
		},
		methods:{
			likeTap(){
				this.like = !this.like
				this.setupdateLike()
				console.log('Saved successfully');
			},
			setupdateLike(){
				uni.showLoading()
				this.$api.update_like({
					user_id:'682d74b08a5c782a2b825fdd',
					article_id: this.item._id
				}).then(res=>{
					uni.hideLoading()
					uni.showToast({
						title:this.like?'Collection Successful':'Cancel Collection',
						// icon:'none'
					})
					console.log(res);
				}).catch(()=>{
					uni.hideLoading()
				})
			}
		}
	}
</script>

<style lang="scss">
	.icons{
		position: absolute;
		right: 0;
		top: 0;
		display: flex;
		justify-content: center;
		align-items: center;
		width: 20px;
		height: 20px;
	}
</style>