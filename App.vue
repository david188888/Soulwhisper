<script>
export default {
	onLaunch: function() {
		console.log('App Launch');

		// 检查登录状态
		const token = uni.getStorageSync('token');
		const currentPages = getCurrentPages();
		const currentPage = currentPages.length > 0 ? currentPages[currentPages.length - 1] : null;
		const isLoginPage = currentPage && currentPage.route === 'frontend/pages/login/index';
		const isRegisterPage = currentPage && currentPage.route === 'frontend/pages/register/index';

		if (!token && !isLoginPage && !isRegisterPage) {
			uni.reLaunch({
				url: '/frontend/pages/login/index'
			});
		}

		setTimeout(() => {
			uni.setTabBarBadge({
				// index: 1,
				// text: ''
			});
			uni.showTabBarRedDot({
				// index: 3
			});
			uni.setLocale('en')
		}, 1000);
	},
	onShow: function() {
		console.log('App Show');
	},
	onHide: function() {
		console.log('App Hide');
	}
};
</script>

<style>
page {
	font-family: "Futura";
}

text, view, button, input, textarea {
	font-family: inherit;
}

.uni-tabbar {
/*.uni-tabbar__item:nth-last-child(3) 修改倒数第三个 也就是中间的图标 我这边底部栏是五个*/
		.uni-tabbar__item:nth-last-child(3) {
			.uni-tabbar__bd {
			/*.uni-tabbar__icon 去掉原图标大小，强制为自适应宽高*/
				.uni-tabbar__icon {
					width: auto !important;
					height: auto !important;
				}
				/*图标大小 !important 强制覆盖*/
				img {
					height: 60px !important;
					width: 60px !important;
					top:-20px;
					position:relative;
				}
			}
		}
	}
.uni-calendar__weeks-item {
   width: 48rpx
}
</style>
