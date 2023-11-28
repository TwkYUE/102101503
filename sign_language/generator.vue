<script>
import { mapState } from "vuex";
import axios from 'axios';
const MediaRecorder = window.MediaRecorder;
const URL = window.URL || window.webkitURL;

export default {
	data() {
		return {
			isPlaying: false, // 标识视频是否正在播放
			videoSrc: "../assets/video1.mp4", // 视频文件路径
			mediaRecorder: null, // 媒体录制对象
			recordedBlob: null, // 录制的音频文件Blob对象
			audioURL: null, // 用于在左侧div框内展示录制音频
			recording: false, // 标识是否正在录制
			speechResult: "", // 存储生成的文字内容
			counter: 0, // 记录当前生成到第几个字
			recognition: null, // 语音识别对象
			recordedMediaRecorder: null, // 用于存储录制的音频
			is_focus:false,
			pending_gen_text:"",
			tmp_txt:''
		};
	},
	computed: {
		...mapState(["theme_is_light"]),
	},
	methods: {
		setFocus(){
			this.is_focus = true;
		},
		setBlur(){
			if(this.tmp_txt.length==0)
			this.is_focus = false;
			else{
				this.pending_gen_text = this.tmp_txt
			}
			console.log(this.pending_gen_text)
		},
		startTextGeneration() {
			this.counter = 0; // 初始化计数器
			this.text = ""; // 清空生成的文字内容
			
			// 每隔一段时间（这里设置500毫秒）执行一次生成文字的操作
			this.textGenerationInterval = setInterval(() => {
				// 获取完整的文字内容
				const fullText = this.speechResult;
				// console.log("111");
				// 每次生成一个字
				this.text += fullText[this.counter];

				// 更新计数器
				this.counter++;

				// 如果计数器超过文字长度，停止生成文字
				if (this.counter >= fullText.length) {
					clearInterval(this.textGenerationInterval);
				}
			}, 150);
		},
		startRecording() {
			navigator.mediaDevices
				.getUserMedia({ audio: true })
				.then((stream) => {
					this.mediaRecorder = new MediaRecorder(stream);
					this.chunks = [];

					this.mediaRecorder.addEventListener("dataavailable", (event) => {
						if (event.data.size > 0) {
							this.chunks.push(event.data);
						}
					});

					this.mediaRecorder.addEventListener("stop", () => {
						this.recordedBlob = new Blob(this.chunks, { type: "audio/webm" });
						this.audioURL = URL.createObjectURL(this.recordedBlob);
					});

					this.mediaRecorder.start();
					this.recording = true;

					// Add speech recognition code here
					this.recognition = new webkitSpeechRecognition();
					this.recognition.lang = "zh-CN";

					this.recognition.onresult = (event) => {
						this.speechResult = event.results[0][0].transcript;
						this.pending_gen_text = this.speechResult;
						//this.startTextGeneration();
						console.log(this.speechResult);
					};

					this.recognition.onerror = (event) => {
						if (event.error === 'no-speech') {
							console.log('No speech detected');
							// Handle the case where no speech is detected
						} else {
							console.error(event.error);
						}
					};

					this.recognition.start();
				})
				.catch((error) => {
					console.error("Error accessing microphone:", error);
				});
		},
		stopRecording() {
			if (this.mediaRecorder && this.recording) {
				this.mediaRecorder.stop();
				this.recording = false;
				        // 在停止录制音频后开始语音识别
				//this.startSpeechRecognition();
			}
		},

		playVideo() {
			if(this.tmp_txt.length>0) this.pending_gen_text = this.tmp_txt
			// axios.post('http://your-server-endpoint', {
			// text: this.text,
			// })
			// .then(response => {
			// console.log(response.data); // 处理服务器响应
			// })
			// .catch(error => {
			// console.error('Error sending text to server:', error);
			// });
			fetch('/generator',{
				method:'POST',
				headers:{
					'Content-Type':'application/json'
				},
				body:JSON.stringify({
					sentence:this.pending_gen_text
				})
			}).then(response=>response.blob())
			.then(async(blob)=>{
				this.isPlaying = true;
				let videoUrl = URL.createObjectURL(blob)

				// await new Promise(resolve=>{setTimeout(resolve,100)})
				if (this.$refs.videoPlayer) {
					console.log(videoUrl);
					console.log(this.$refs.videoPlayer);
					this.$refs.videoPlayer.src = videoUrl;
        			// 调用play()方法开始播放
        			this.$refs.videoPlayer.play();
			}})
			
		},
	},
};
</script>

<template>
	<div style="text-align: center">
		<div style="margin: 30px">
			<strong
				class="text"
				style="font-size: 55px"
				:style="{ color: !theme_is_light ? 'white' : 'rgb(71, 71, 71)' }"
			>
				手语生成
			</strong>
			<div
				class="text"
				style="font-size: 15px; letter-spacing: 10px; margin: 5px"
				:style="{ color: !theme_is_light ? 'white' : 'rgb(71, 71, 71)' }"
			>
				SIGN LANGUAGE GENERATION
			</div>
			<div style="display: flex; justify-content: center">
				<button
					class="sign"
					style="background-image: linear-gradient(to right, #81dcf8, #187fdc);
						color: white;"
					@click="startRecording"
					:disabled="recording"
					v-if="!recording"
				>
					开始录音
				</button>
				<button
					class="sign"
					style="
						background-image: linear-gradient(to right, #81dcf8, #187fdc);
						color: white;
					"
					@click="stopRecording"
					:disabled="!recording"
					v-else
				>
					结束录音
				</button>
			</div>
		</div>
		<div style="display: flex">
			<div
				style="
					display: flex;
					flex-direction: column;
					justify-content: center;
					align-items: center;
					width: 46%;
					height: 400px;
					padding: 20px;
				"
			>
				<div
					id="video-placeholder"
					class="bk_linear"
					style="width: 80%; height: 80%; margin-top: 25px; position: relative"
					:style="{
						boxShadow: this.$store.state.theme_is_light
							? '0 10px 50px 0 #bfbfbf'
							: '0 10px 50px 0 #000',
					}"
				>
					<div>
						<!-- <div style="margin-top: 20px; color: rgb(123, 123, 123)">
							这里是录制的音频
						</div> -->
						<div class="audio-player-container">
							<div class="audio-player">
								<audio controls :src="audioURL"></audio>
								<div class="play-button"></div>
								<div class="pause-button"></div>
							</div>
						</div>
					</div>
					<div style="display: flex; justify-content: center">
						<button
							class="sign"
							style="
								background-image: linear-gradient(to right, #81dcf8, #187fdc);
								color: white;
								margin: 15px auto;
								width: 140px;
							"
							@click="startTextGeneration"
						>
							语音转文字
						</button>
					</div>
					<div style="display: flex; justify-content: center">
					<div
						style="
							background-color: rgba(255, 255, 255, 0.5);
							width: 80%;
							height: 128px;
							border-radius: 2.5%;
						"
					>
						<div
							style="
								display: flex;
								align-items: center;
								justify-content: center;
								color: rgb(123, 123, 123);
								height: 100%;
								position: relative;
							"
							v-if="!counter"
						>
							{{ is_focus ? "" : '现在还没有转成文本的音频哦~' }}
							<textarea @focus="setFocus" @blur="setBlur" v-model="tmp_txt" style="position: absolute; width: 100%; height: 100%; background-color: transparent; border: none; resize: none; outline: none;"></textarea>
						</div>
						<div style="text-align: left; padding: 10px 20px" v-else>
							{{ pending_gen_text }}
						</div>
					</div>
				</div>

				</div>
			</div>
			<div
				style="
					display: flex;
					justify-content: center;
					align-items: center;
					width: 8%;
					height: 400px;
				"
			>
				<button
					class="circle-button"
					style="
						background-image: linear-gradient(to right, #81dcf8, #187fdc);
						color: white;
						cursor: pointer;
					"
					@click="playVideo"
				>
					开始生成
				</button>
			</div>
			<div
				style="
					display: flex;
					justify-content: center;
					align-items: center;
					width: 46%;
					height: 400px;
					padding: 20px;
				"
			>
				<div
					class="bk_linear"
					style="width: 80%; height: 80%; margin-top: 25px"
					:style="{
						boxShadow: this.$store.state.theme_is_light
							? '0 10px 50px 0 #bfbfbf'
							: '0 10px 50px 0 #000',
					}"
				>
					<div class="video-placeholder" v-show="!isPlaying">
						<img
							class="video_sign"
							src="../assets/video_sign.png"
							alt="png图像"
							style="width: 100px; margin-top: 80px"
						/>
						<div style="color: rgb(123, 123, 123)">现在还没有生成的视频哦~</div>
					</div>
					<!-- 视频元素 -->
					<div
						style="
							overflow: hidden;
							width: 100%;
							height: 100%;
							border-radius: 20px;
						"
						v-show="isPlaying"
					>
						<video
							ref="videoPlayer"
							class="video-player"
							style="
								width: 100%;
								height: 100%;
								object-fit: cover;
							"
						></video>
					</div>

				</div>
			</div>
		</div>
	</div>
</template>

<style scoped>
.sign {
	display: flex;
	margin: auto 10px;
	justify-content: center;
	align-items: center;
	cursor: pointer;
	background: none;
	border: none;
	box-sizing: border-box;
	padding: 0px 30px;
	border-radius: 13px;
	font-weight: bold;
	font-size: 16px;
	height: 25px;
	width: 124px;
	line-height: 17px;
	margin-top: 3px;
	transform: scale(0.95);
	transition: transform 0.3s ease;
}
.sign:hover {
	transform: scale(1.02);
}
.bk_linear {
	background: linear-gradient(135deg, #f4fcff, #e3f2ff, #e3e7ff);
	background-size: 200% 200%;
	animation: gradient-move 10s ease infinite;
	border-radius: 20px;
}

@keyframes gradient-move {
	0% {
		background-position: 0% 0%;
	}
	50% {
		background-position: 100% 100%;
	}
	100% {
		background-position: 0% 0%;
	}
}
.circle-button {
	display: flex;
	justify-content: center;
	align-items: center;
	background: none;
	border: none;
	box-sizing: border-box;
	border-radius: 50%;
	font-weight: bold;
	font-size: 16px;
	padding: 0 20px;
	height: 80px;
	width: 80px;
	line-height: 17px;
	transform: scale(1);
	transition: transform 0.3s ease;
}
.circle-button:hover {
	transform: scale(1.1);
}
.audio-player-container {
	display: flex;
	justify-content: center;
	align-items: center;
	margin-top: 20px;
}

.audio-player {
	position: relative;
	width: 80%;
	height: 60px;
	background-color: transparent;
	overflow: hidden;
	display: flex;
	align-items: center;
}

.audio-player audio {
	flex: 1;
	height: 100%;
	outline: none;
	background-color: transparent;
}

.play-button,
.pause-button {
	position: absolute;
	top: 50%;
	left: 50%;
	transform: translate(-50%, -50%);
	font-size: 30px;
	color: white;
}
</style>
