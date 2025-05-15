<template>
	<view class="content">
		<!-- 搜索栏-->
		<!-- <navbar></navbar> -->
		<!--选项卡-->
		<tab :list="tabList" :tabIndex="tabIndex" @tab="tab"></tab>
		<!-- 卡片视图 -->
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
						name:'全部'
					})
					this.tabList = data
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
		.home-list{
			flex: 1;
			box-sizing: border-box;
			// border: 1px red solid;
		}
	}
</style>
