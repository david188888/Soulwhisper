<template>
	<view class="content">
		<!-- 搜索栏-->
		<!-- <navbar></navbar> -->
		<!--选项卡-->
		<!-- <tab></tab> -->
		<!-- 卡片视图 -->
		<listScroll>
			<!-- <listCard mode="base"></listCard>
			<listCard mode="image"></listCard>
			<listCard mode="column"></listCard>
			<listCard mode="image"></listCard>
			<listCard mode="column"></listCard>
			<listCard mode="base"></listCard>
			<listCard mode="column"></listCard> -->
			<listCard1></listCard1>
			<listCard1></listCard1>
			<listCard1></listCard1>
			<listCard1></listCard1>
			<listCard1></listCard1>
			<listCard1></listCard1>
		</listScroll>
	</view>
</template>

<script>
	import listScroll from '@/frontend/components/listScroll/listScroll.vue'
	import listCard from '@/frontend/components/listCard/listCard.vue';
	import listCard1 from '@/frontend/components/listCard/listCard1.vue';
	// import navbar from '@/frontend/components/navbar/navbar.vue';
	// import tab from '@/frontend/components/tab/tab.vue'
	export default {
		components:{
			// navbar,
			// tab
			listScroll,
			listCard,
			listCard1
		},
		data() {
			return {
				title: 'Hello'
			}
		},
		onLoad() {

		},
		methods: {

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
	}
</style>
