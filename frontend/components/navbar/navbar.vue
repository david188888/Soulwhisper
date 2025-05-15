<template>
	<view class="navbar">
		<view class="navbar-fixed">
			<!--状态栏-->
			<view :style="{height:statusBarHeight+'px'}"></view>
			<!--导航栏内容-->
			<view class="navbar-content" :style="{height:navBarHeight+'px',width:windowWidth+'px'}">
				<view class="navbar-search">
					<view class="navbar-search_icon">
						<uni-icons type="search" size="18" color="#999"></uni-icons>
					</view>
					<view class="navbar-search_text">uniapp</view>
				</view>
			</view>
		</view>
		<view :style="{height: statusBarHeight+navBarHeight+'px'}"></view>
	</view>
</template>

<script>
	export default{
		data(){
			return{
				statusBarHeight:20,
				navBarHeight:45,
				windowWidth:375
			};
		},
		created(){
			//获取手机系统信息
			const info = uni.getSystemInfoSync()
			//设置状态栏高度
			this.statusBarHeight = info.statusBarHeight
			this.windowWidth = info.windowWidth
			//小程序格式调试
			//#ifndef H5||APP-PLUS||MP-ALIPAY
			//获取胶囊位置
			const menuButtonInfo = uni.getMenuButtonBoundingClientRect()
			console.log(menuButtonInfo);
			//导航栏高度
			this.navBarHeight = (menuButtonInfo.bottom - info.statusBarHeight) + (menuButtonInfo.top - info.statusBarHeight)
			this.windowWidth = menuButtonInfo.left
			//#endif
		}
	}
</script>

<style lang="scss">
	.navbar{
		.navbar-fixed{
			position: fixed;
			top: 0;
			left: 0;
			z-index: 99;
			width: 100%;
			background-image: linear-gradient(135deg, #a559f7 0%, #62a3fa 100%);
			.navbar-content{
				display: flex;
				justify-content: center;
				align-items: center;
				padding: 0 15px;
				height: 45px;
				box-sizing: border-box;
				.navbar-search{
					display: flex;
					align-items: center;
					padding: 0 10px;
					width: 100%;
					height: 30px;
					border-radius: 30px;
					background-color: #fff;
					.navbar-search_icon{
						margin-right: 10px;
					}
					.navbar-search_text{
						font-size: 12px;
						color: #999;
					}
				}

			}
		}
	}
</style>