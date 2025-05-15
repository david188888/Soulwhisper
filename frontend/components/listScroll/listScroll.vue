<template>
	<view class="scroll">
<<<<<<< HEAD
		<scroll-view class="list-scroll" scroll-y>
=======
		<scroll-view class="list-scroll" scroll-y @scrolltolower="loadmore">
>>>>>>> master
			<view>
				<slot></slot>
			</view>
		</scroll-view>
	</view>
</template>

<script>
<<<<<<< HEAD
=======
	export default {
		data(){
			return{
				
			};
		},
		methods:{
			loadmore(){
				this.$emit('loadmore')
			}
		}
	}
>>>>>>> master
</script>

<style lang="scss">
	.scroll{
		flex: 1;
		overflow: hidden;
		box-sizing: border-box;
		.list-scroll{
			height: 100%;
			display: flex;
			flex-direction: column;
		}
	}
</style>