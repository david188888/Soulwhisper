<template>
	<swiper class="home-swiper" :current="activeIndex" @change="change">
		<swiper-item v-for="(item,index) in tab" :key="index" class="swiper-item">
			<listItem :list="listCatchData[index]" :load="load[index]" @loadmore="loadmore"></listItem>
		</swiper-item>
	</swiper>
</template>

<script>
	import listItem from '../list/listItem.vue'
	export default {
		components:{
			listItem
		},
		props:{
			tab:{
				type: Array,
				default(){
					return[]
				}
			},
			activeIndex:{
				type: Number,
				default:0
			}
		},
		data(){
			return{
				list :[],
				listCatchData:{},
				load:{},
				pageSize:6
			};
		},
		watch:{
			tab(newVal){
				if(newVal.length === 0) return
				this.getList(this.activeIndex)
			}
		},
		created(){
			// this.getList(0)
		},
		methods:{
			loadmore(){
				if(this.load[this.activeIndex].loading === 'noMore') return
				this.load[this.activeIndex].page++
				console.log('触发上拉')
				this.getList(this.activeIndex)
			},
			change(e){
				const {current} = e.detail
				this.$emit('change',current)
				//当数据不存在或长度为0，才请求数据
				if(!this.listCatchData[current] || this.listCatchData[current].length === 0){
					this.getList(current)
				}
			},
			getList(current){
				if(!this.load[current]){
					this.load[current] = {
						page: 1,
						loading: 'loading'
					}
				}
				this.$api.get_list({
					name:this.tab[current].name,
					page:this.load[current].page,
					pageSize:this.pageSize
					}).then(res=>{
					console.log(res);
					const{data} = res
					// this.list = data
					// this.listCatchData[current] = data
					if(data.length === 0){
						let oldLoad = {}
						oldLoad.loading = 'noMore'
						oldLoad.page = this.load[current].page
						this.$set(this.load,current,oldLoad)
						//强制渲染
						this.$forceUpdate()
						return
					}
					let oldList = this.listCatchData[current] || []
					oldList.push(...data)
					//懒加载
					this.$set(this.listCatchData,current,oldList)
				})
			}
		}
	}
</script>

<style lang="scss">
	.home-swiper{
		height: 100%;
		.swiper-item{
			height: 100%;
			overflow: hidden;
			.list-scroll{
				height: 100%;
			}
		}
	}
</style>