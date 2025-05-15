<template>
	<view class="tab">
		<scroll-view class="tab-scroll" scroll-x>
			<view class="tab-scroll_box">
				<view v-for="(item,index) in list" :key="index" class="tab-scroll_item" :class="{active:activeIndex === index}" @click="clickTab(item,index)">
					{{item.name}}
				</view>
			</view>
		</scroll-view>
		<view class="tab-icons">
			<uni-icons type="gear" size="26" color="#666"></uni-icons>
		</view>
	</view>
</template>

<script>
	export default{
		props:{
			list:{
				type: Array,
				default(){
					return[]
				}
			},
			tabIndex:{
				type: Number,
				default: 0
			}
		},
		//可以监听data/props值的变化
		watch:{
			tabIndex(newVal){
				this.activeIndex = newVal
			}
		},
		data(){
			return{
				activeIndex: 0
			};
		},
		methods:{
			clickTab(item,index){
				// console.log(item,index);
				this.activeIndex = index;
				this.$emit('tab',{
					data: item,
					index: index
				});
			}
		}
	}
</script>

<style lang="scss">
	.tab{
		display: flex;
		width: 100%;
		border-bottom: 3px #f5f5f5 solid;
		background-color: #fff;
		box-sizing: border-box;
		.tab-scroll{
			flex: 1;
			overflow: hidden;
			box-sizing: border-box;
			.tab-scroll_box{
				display: flex;
				align-items: center;
				flex-wrap: nowrap;
				height: 45px;
				box-sizing: border-box;
				.tab-scroll_item{
					flex-shrink: 0;
					padding: 0 10px;
					color: #333;
					font-size: 14px;
					&.active{
						color: #8A2BE2;
					}
				}
			}
		}
		.tab-icons{
			position: relative;
			display: flex;
			justify-content: center;
			align-items: center;
			width: 45px;
			&::after{
				content: '';
				position: absolute;
				top: 12px;
				bottom: 12px;
				left: 0;
				width: 1px;
				background-color: #ddd;
			}
		}
	}
</style>