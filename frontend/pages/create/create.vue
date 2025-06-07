<template>
	<view>
		<view class="title">Title：</view>
			<view class="title-content">
				<textarea class="text" v-model="title" maxlength="100" placeholder="Please Enter Title..."></textarea>
			</view>
		<view class="content">Content:</view>
			<view class="content-content">
				<textarea class="text" v-model="content" maxlength="5000" placeholder="At this moment..."></textarea>
			</view>
			<view class="title">Add picture: </view>
			<view class="image-box">
				<view class="item" v-for="(item,index) in imageLists" :key="index">
					<view class="close-icon" @click="del(index)">
						<uni-icons type="close" size="20" color="#fff"></uni-icons>
					</view>
					<view class="box">
						<image :src="item.url" mode="aspectFill"></image>
					</view>
				</view>
				<view v-if="imageLists.length < 1" class="item" @click="addImage">
					<view class="box">
						<uni-icons type="plusempty" size="50" color="#eee"></uni-icons>
					</view>
				</view>
			</view>
			<button class="button" type="primary" @click="submit">Publish</button>
	</view>
</template>

<script>
	export default{
		data(){
			return{
				title:'',
				content:'',
				imageLists:[]
			}
		},
		methods:{
			del(index){
				this.imageLists.splice(index,1)
			},
			addImage(){
				const count = 1 - this.imageLists.length
				uni.chooseImage({
					count:count,
					success: (res)=> {
						const tempfilepaths = res.tempFilePaths
						tempfilepaths.forEach((item,index)=>{
							//Handling the situation of multiple selections in H5
							if(index<count){
								this.imageLists.push({
									url:item
							})
						  }	
						})
						console.log(res)
					}
				})
			},
			async submit(){
				let imagesPath = []
				uni.showLoading()
				for(let i = 0 ; i < this.imageLists.length ; i++){
					const filePath = this.imageLists[i].url
					const uploadPath = await this.uploadFiles(filePath)
					imagesPath.push(uploadPath)
				}
				// console.log(imagesPath);
				this.updateArticle({
					title: this.title,
					content: this.content,
					cover: imagesPath
				})
			},
			async uploadFiles(filePath){
				const cloudPath = `images/${Date.now()}.jpg`;
				const result = await uniCloud.uploadFile({
					filePath: filePath,
					cloudPath:cloudPath
				})
				console.log(result);
				return result.fileID
			},
			updateArticle({
				title,
				content,
				cover
			}){
				this.$api.update_article({
					title,
					content,
					cover
				}).then(res=>{
					uni.hideLoading()
					uni.showToast({
						title:"Published Successfully",
						icon:'success'
					})
					setTimeout(()=>{
						uni.switchTab({
							url:'/frontend/pages/tabbar/tabbar-4/tabbar-4'
						})
					},2000)
				}).catch(()=>{
					uni.hideLoading()
					uni.showToast({
						title:"published Failed",
						icon:"fail"
					})
				})
			}
		}
	}
</script>

<style lang="scss">
	.title{
		margin:15px;
		margin-bottom: 0;
		font-size: 14px;
		color: #666;
	}
	.title-content{
		height: 80px;
		width: 100%;
		margin:15px;
		padding: 10px;
		box-sizing: border-box;
		border: 1px #eee solid;
		border-radius: 20px;
		.text{
			font-size: 15px;
		}
	}
	.content{
		margin:15px;
		margin-bottom: 0;
		font-size: 14px;
		color: #666;
	}
	.content-content{
		height: 30%;
		width: 100%;
		margin:15px;
		padding: 10px;
		box-sizing: border-box;
		border: 1px #eee solid;
		border-radius: 20px;
		.text{
			font-size: 15px;
		}
	}
	.image-box{
		display: flex;
		flex-wrap: wrap;
		padding: 10px;
		.item{
			position: relative;
			width: 33.33%;
			height: 0;
			padding-top: 33.33%;
			box-sizing: border-box;
			// border: 1px red solid;
			.close-icon{
				display: flex;
				justify-content: center;
				align-items: center;
				position: absolute;
				right: 0;
				top: 0;
				width: 16px;
				height: 16px;
				border-radius: 50%;
				background-color: #ff5a5f;
				z-index: 2;
			}
			.box{
				display: flex;
				justify-content: center;
				align-items: center;
				position: absolute;
				top: 5px;
				right: 5px;
				bottom: 5px;
				left: 5px;
				border: 1px #eee solid;
				border-radius: 5px;
				overflow: hidden;
				image{
					width: 100%;
					height: 100%;
				}
			}
		}
	}
	.button{
		margin: 0 20px;
		border-radius: 30px;
		background:linear-gradient(135deg, #A18BFF 0%, #7B89F9 100%) ;
	}
</style>