<template>
	<view class="aichat-container">
		<!-- 顶部介绍区 -->
		<view class="header">
			<image class="avatar" src="\frontend\static\img\chat.png" mode="aspectFill"></image>
			<view class="info">
				<text class="title">Focus on mental health companionship</text>
				<view class="tags">
					<text class="tag">Psychological companionship</text>
					<text class="tag">AI chat</text>
					<text class="tag">Emotional guidance</text>
				</view>
				<text class="desc">I am your AI mental health companion, always here to listen.</text>
			</view>
		</view>

		<!-- 聊天消息区 -->
		<scroll-view class="chat-list" scroll-y="true" :scroll-into-view="scrollToView">
			<view v-for="(msg, idx) in messages" :key="idx" :id="'msg'+idx" :class="['msg-item', msg.role]">
				<view class="msg-bubble">{{ msg.content }}</view>
			</view>
			<view v-if="loading" class="msg-item assistant">
				<view class="msg-bubble">AI is typing...</view>
			</view>
		</scroll-view>

		<!-- Bottom Input Area -->
		<view class="input-bar">
			<input v-model="inputText" class="input" placeholder="Feel free to describe your concerns in detail~" @confirm="sendMessage"/>
			<button class="send-btn" @click="sendMessage" :disabled="loading || !inputText.trim()">Send</button>
		</view>
	</view>
</template>

<script>
import { api } from '../../../components/api/apiPath.js';

export default {
	data() {
		return {
			messages: [],
			inputText: '',
			sessionId: '',
			loading: false,
			scrollToView: ''
		}
	},
	onLoad() {
		// when page load, automatically send welcome message
		this.messages.push({
			role: 'assistant',
			content: 'Hello, I am your AI mental health companion. What would you like to talk about?'
		});
		this.scrollToBottom();
	},
	methods: {
		scrollToBottom() {
			this.$nextTick(() => {
				this.scrollToView = 'msg' + (this.messages.length - 1);
			});
		},
		async sendMessage() {
			if (!this.inputText.trim() || this.loading) return;
			const userMsg = this.inputText.trim();
			this.messages.push({ role: 'user', content: userMsg });
			this.inputText = '';
			this.loading = true;
			this.scrollToBottom();

			try {
				const userInfo = uni.getStorageSync('userInfo');
				if (!userInfo || !userInfo.token) {
					uni.showToast({ title: 'Please login first', icon: 'none' });
					this.loading = false;
					return;
				}

				let url = '';
				let data = {};
				// if there is no sessionId, first start
				if (!this.sessionId) {
					url = api.chatStart;
					data = { diary_content: userMsg };
				} else {
					url = api.chatMessage;
					data = { message: userMsg };
				}

				const res = await uni.request({
					url,
					method: 'POST',
					header: {
						'Authorization': `Token ${userInfo.token}`,
						'Content-Type': 'application/json'
					},
					data
				});

				if (res.statusCode === 200 && res.data) {
					if (res.data.session_id) this.sessionId = res.data.session_id;
					const reply = res.data.response || 'AI could not respond, please try again later.';
					this.messages.push({ role: 'assistant', content: reply });
				} else {
					this.messages.push({ role: 'assistant', content: res.data?.error || 'AI service error' });
				}
			} catch (e) {
				this.messages.push({ role: 'assistant', content: 'Network error, please try again later.' });
			}
			this.loading = false;
			this.scrollToBottom();
		},
		// Optional: End chat session
		async endChat() {
			try {
				const userInfo = uni.getStorageSync('userInfo');
				if (!userInfo || !userInfo.token) return;
				await uni.request({
					url: api.chatEnd,
					method: 'POST',
					header: {
						'Authorization': `Token ${userInfo.token}`,
						'Content-Type': 'application/json'
					}
				});
				this.sessionId = '';
				this.messages.push({ role: 'assistant', content: 'Session ended. Please enter a new message to continue.' });
				this.scrollToBottom();
			} catch (e) {}
		}
	}
}
</script>

<style scoped>
.aichat-container {
	display: flex;
	flex-direction: column;
	height: 100vh;
	background: #f8fafc;
}
.header {
	display: flex;
	align-items: center;
	padding: 20px 16px 10px 16px;
	background: linear-gradient(135deg, #a559f7 0%, #62a3fa 100%);
	border-radius: 0 0 20px 20px;
}
.avatar {
	width: 60px;
	height: 60px;
	border-radius: 30px;
	margin-right: 16px;
}
.info {
	flex: 1;
}
.title {
	font-size: 18px;
	color: #fff;
	font-weight: bold;
}
.tags {
	margin: 6px 0;
}
.tag {
	display: inline-block;
	background: #fff;
	color: #a559f7;
	border-radius: 10px;
	padding: 2px 10px;
	font-size: 12px;
	margin-right: 8px;
}
.desc {
	color: #fff;
	font-size: 13px;
}
.chat-list {
	flex: 1;
	padding: 10px 16px 80px 16px;
	overflow-y: auto;
}
.msg-item {
	display: flex;
	margin-bottom: 12px;
	width: 100%;
}
.msg-item.assistant {
	justify-content: flex-start;
}
.msg-item.user {
	justify-content: flex-end;
}
.msg-bubble {
max-width: 90%; /* 或者 calc(100% - 16px) */
  padding: 10px 16px;
  border-radius: 16px;
  font-size: 15px;
  line-height: 1.6;
  background: #fff;
  color: #333;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  word-break: break-all;
  box-sizing: border-box;
}
.msg-item.user .msg-bubble {
	background: #a559f7;
	color: #fff;
	margin-left: auto;
	margin-right: 24px;
}
.msg-item.assistant .msg-bubble {

}
.input-bar {
	position: fixed;
	left: 0; right: 0; bottom: 0;
	display: flex;
	align-items: center;
	background: #fff;
	padding: 8px 10px;
	box-shadow: 0 -2px 8px rgba(0,0,0,0.04);
}
.input {
	flex: 1;
	border: none;
	outline: none;
	font-size: 15px;
	padding: 8px 12px;
	border-radius: 20px;
	background: #f3f3f3;
	margin-right: 8px;
}
.send-btn {
	background: linear-gradient(135deg, #a559f7 0%, #62a3fa 100%);
	color: #fff;
	border: none;
	border-radius: 20px;
	padding: 0 18px;
	font-size: 15px;
	height: 36px;
}
</style>
