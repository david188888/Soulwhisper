<template>
	<listScroll class="list-scroll" @loadmore="loadmore">
		<listCard1 :item="item" v-for="item in list" :key="item_id"></listCard1>
		<uni-load-more v-if="list.length === 0 || list.length > 5" icon-type="snow" status="load.loading"></uni-load-more>
	</listScroll>
</template>

<script>
	import listScroll from '@/frontend/components/listScroll/listScroll.vue';
	import listCard1 from '@/frontend/components/listCard/listCard1.vue';
	export default {
		components:{
			listScroll,
			listCard1
		},
		props:{
			list:{
				type:Array,
				default(){
					return[]
				}
			},
			load:{
				type: Object,
				default(){
					return{
						loading:"loading"
					}
				}
			}
		},
		methods:{
			loadmore(){
				this.$emit('loadmore')
			}
		}
	}
</script>

<style lang="scss">
	.list-scroll{
		height: 100%;
	}
</style>