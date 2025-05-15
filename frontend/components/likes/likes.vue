<template>
	<view class="icons" @click.stop="likeTap">
		<uni-icons :type="like?'heart-filled':'heart'" size="20px" color="#f07373"></uni-icons>
	</view>
</template>

<script>
	export default{
		data(){
			return{
				like:false
			};
		},
		methods:{
			likeTap(){
				this.like = !this.like
<<<<<<< HEAD
				console.log('收藏成功');
=======
				console.log('�ղسɹ�');
>>>>>>> master
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