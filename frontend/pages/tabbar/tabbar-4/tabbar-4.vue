<template>
	<view class="content">
		<view class="header">
			<view class="add-btn" @click="create">
				<uni-icons type="plus" size="35" color="#8A2BE2"></uni-icons>
			</view>
		</view>
		<!-- Search bar -->
		<!-- <navbar></navbar> -->
		<!-- Tab options -->
		<!-- <tab :list="tabList" :tabIndex="tabIndex" @tab="tab"></tab> -->
		<!--Card View -->
		<view class="home-list">
			<list :tab="tabList" :activeIndex="activeIndex" @change="change"></list>
		</view>
	</view>
</template>

<script>
	import tab from '@/frontend/components/tab/tab.vue';
	import list from '@/frontend/components/list/list.vue'
	export default {
		components:{
			tab,
			list
		},
		data() {
			return {
				title: 'Hello',
				tabList:[],
				tabIndex:0,
				activeIndex:0,
			}
		},
		onLoad() {
			this.getLabel()
		},
		methods: {
			change(current){
				this.tabIndex = current;
				// this.activeIndex = current
				// console.log('now',current);
			},
			tab({data,index}){
				console.log(data,index);
				this.activeIndex = index;
			},
			getLabel(){
				this.$api.get_label({
					name:'get_label'
				}).then((res)=>{
					const{
						data
					}=res
					data.unshift({
						name:'All'
					})
					this.tabList = data
				})
			},
			create(){
				uni.navigateTo({
					url:'/frontend/pages/create/create',
				})
			}
		}
	}
</script>

<style lang="scss">
	page{
		height: 100%;
		display: flex;
	}
	.content{
		display: flex;
		flex-direction: column;
		flex: 1;
		// border: 1px red solid;
		overflow: hidden;
		.header{
			display: flex;
			background-color:#fff;
			height: 40px;
			width: 100%;
			.add-btn {
				position: absolute;
				margin: 5px 10px;
				right: 20px;
				// top: -40px;
				z-index: 9999;
			}
		}
		.home-list{
			flex: 1;
			box-sizing: border-box;
			// border: 1px red solid;
		}
	}
</style>
