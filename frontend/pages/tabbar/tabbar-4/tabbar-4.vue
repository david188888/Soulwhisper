<template>
	<view class="content">
		<!--搜索栏-->
		<navbar></navbar>
		<!--选项卡-->
		<tab></tab>
		<!-- <view v-for="item in 50">
			{{item}}hahahahahaha
		</view> -->
	</view>
</template>

<script>
	import navbar from '@/frontend/components/navbar/navbar.vue';
	import tab from '@/frontend/components/tab/tab.vue'
	export default {
		components:{
			navbar,
			tab
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
</style>
