import App from './App'
import { createSSRApp } from 'vue'
<<<<<<< HEAD
=======
import api from './frontend/common/api'
>>>>>>> master

// #ifndef VUE3
import Vue from 'vue'
Vue.config.productionTip = false
<<<<<<< HEAD
=======
Vue.prototype.$api = api
>>>>>>> master
App.mpType = 'app'
const app = new Vue({
	...App
})
app.$mount()
// #endif

// #ifdef VUE3
// 不需要登录就能访问的页面
const PUBLIC_PAGES = [
	'/frontend/pages/login/index',
	'/frontend/pages/register/index'
]

// tabbar 页面
const TABBAR_PAGES = [
	'/frontend/pages/tabbar/tabbar-1/tabbar-1',
	'/frontend/pages/tabbar/tabbar-2/tabbar-2',
	'/frontend/pages/tabbar/tabbar-3/tabbar-3',
	'/frontend/pages/tabbar/tabbar-4/tabbar-4',
	'/frontend/pages/tabbar/tabbar-5/tabbar-5',
	'/frontend/pages/home-3-detial/record/record'
]

// 添加路由拦截器
const routeInterceptor = {
	invoke(args) {
		const url = args.url
		const token = uni.getStorageSync('token')
		const isPublicPage = PUBLIC_PAGES.some(page => url.startsWith(page))
		const isTabbarPage = TABBAR_PAGES.some(page => url.startsWith(page))

		if (!token && !isPublicPage && !isTabbarPage) {
			uni.reLaunch({
				url: '/frontend/pages/login/index'
			})
			return false
		}
		return true
	}
}

export function createApp() {
	const app = createSSRApp(App)
<<<<<<< HEAD
	
=======
	app.config.globalProperties.$api = api
>>>>>>> master
	// 添加全局路由拦截
	uni.addInterceptor('navigateTo', routeInterceptor)
	uni.addInterceptor('redirectTo', routeInterceptor)
	uni.addInterceptor('reLaunch', routeInterceptor)
	uni.addInterceptor('switchTab', routeInterceptor)
	
	return {
		app
	}
}
// #endif
