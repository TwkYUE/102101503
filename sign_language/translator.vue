<script>
import { mapState } from "vuex";

export default {
	data() {
		return {
			mediaRecorder: null,
			recordedBlobUrl: null,
			isRecording: false,
			recognitionResult: "",
			recordedChunks: [],
			mediaSource: null,
			translatedText: "",
			translate: false,
			audioURL: "",
			text: "",
			counter: 0,
			formdata: null,
			pending_translate_text:""
		};
	},
	computed: {
		...mapState(["theme_is_light"]),
	},
	methods: {
		startRecording() {
			this.isRecording = true;
			this.recordedBlobUrl = null;
			this.translate = false;
			this.translatedText = "";
			navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
				this.$refs.videoElement.srcObject = stream;
				this.$refs.videoElement.play();
				this.mediaRecorder = new MediaRecorder(stream);
				this.mediaRecorder.ondataavailable = (event) => {
					if (event.data && event.data.size > 0) {
						this.recordedChunks.push(event.data);
					}
				};
				this.mediaRecorder.start();
			});
		},
		async stopRecording() {
			this.isRecording = false;
			this.recordedBlobUrl = "1";

			if (this.mediaRecorder) {
				this.mediaRecorder.stop();
				await new Promise((resolve) => setTimeout(resolve, 1000));
				// 添加检查，确保 srcObject 不为 null 或 undefined
				if (this.$refs.record.srcObject) {
					const tracks = this.$refs.record.srcObject.getTracks();
					tracks.forEach((track) => track.stop());
				}
				const blob = new Blob(this.recordedChunks, { type: "video/mp4" });				
				this.recordedBlobUrl = URL.createObjectURL(blob);
				this.$refs.record.src = this.recordedBlobUrl;
				// 发送录制的视频数据到服务器进行保存
				// const formData = new FormData();
				// formData.append("mp4File", blob, "recorded_video.mp4");
				this.formdata = new FormData();
				this.formdata.append("mp4File", blob, "recorded_video.mp4");

        		// formData.append('mp4File', file);


				// fetch("/save-video", {
				// 	method: "POST",
				// 	body: formData,
				// })
				// 	.then((response) => response.json())
				// 	.then((data) => {
				// 		console.log("录制的视频已保存");
				// 		console.log(data); // 这里可以处理服务器返回的结果
				// 	})
				// 	.catch((error) => {
				// 		console.error("保存录制视频时出错", error);
				// 	});

				}
		},

		startTranslation() {

			fetch('/translator', {
            method: 'POST',
            body: this.formdata
        }).then(response => response.json())
            .then(json => {
				// console.log(json);
				return json['sentence']
			})
			.then( fullText => {
				if(fullText.length==0){
					fullText = "很抱歉，暂时没有识别到任何手语，请重试。"
				}else{
						// this.translatedText = fullText
				}
			this.pending_translate_text = fullText
			this.counter = 0; // 初始化计数器
			this.text = ""; // 清空生成的文字内容

			// 每隔一段时间（这里设置500毫秒）执行一次生成文字的操作
			this.textGenerationInterval = setInterval(() => {
			// 获取完整的文字内容(从服务器端返回)

			// const fullText =
			// 	"很抱歉我迟到了";

			// 每次生成一个字
			this.text += fullText[this.counter];

			// 更新计数器
			this.counter++;

			// 如果计数器超过文字长度，停止生成文字
			if (this.counter >= fullText.length) {
				clearInterval(this.textGenerationInterval);
				// 在生成文字完成后调用方法将文字转换为语音
			//  this.textToSpeech(this.text);
			}
			}, 150);
			})
			
		},

		blobFromSpeechSynthesis(utterance) {
		const blob = new Blob([new Uint8Array(utterance.audioBuffer)], { type: 'audio/webm' });
		return URL.createObjectURL(blob);
		},

		textToSpeech() {
		// const text = "你要合成的文本";

		const utterance = new SpeechSynthesisUtterance(this.pending_translate_text);
		// const utterance = new SpeechSynthesisUtterance("很高兴遇见你");

		// 清空之前的音频
		this.$refs.audioControler.src = "";
		window.speechSynthesis.cancel();

		// 监听语音合成结束事件
		utterance.onend = () => {
			// 将合成的语音绑定到音频播放器
			const audioURL = this.blobFromSpeechSynthesis(utterance); // 获取 URL
			this.$refs.audioControler.src = audioURL; // 设置音频播放器的 src
			// 播放音频
			this.$refs.audioControler.play();
		};

		// 开始语音合成
		window.speechSynthesis.speak(utterance);
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
				手语翻译
			</strong>
			<div
				class="text"
				style="font-size: 15px; letter-spacing: 10px; margin: 5px"
				:style="{ color: !theme_is_light ? 'white' : 'rgb(71, 71, 71)' }"
			>
				SIGN LANGUAGE TRANSLATION
			</div>
			<div style="display: flex; justify-content: center">
				<button
					class="sign"
					style="
						background-image: linear-gradient(to right, #81dcf8, #187fdc);
						color: white;
					"
					@click="startRecording"
					v-if="!isRecording"
				>
					开始录制
				</button>
				<button
					class="sign"
					style="
						background-image: linear-gradient(to right, #81dcf8, #187fdc);
						color: white;
					"
					@click="stopRecording"
					v-else
				>
					结束录制
				</button>
			</div>
		</div>
		<div style="display: flex">
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
					id="video-placeholder"
					class="bk_linear"
					style="width: 80%; height: 80%; margin-top: 25px; position: relative"
					:style="{
						boxShadow: this.$store.state.theme_is_light
							? '0 10px 50px 0 #bfbfbf'
							: '0 10px 50px 0 #000',
					}"
				>
					<div
						class="video-placeholder"
						v-if="!isRecording && !recordedBlobUrl"
					>
						<img
							class="video_sign"
							src="../assets/video_sign.png"
							alt="png图像"
							style="width: 100px; margin-top: 80px"
						/>
						<div style="color: rgb(123, 123, 123)">现在还没有录制的视频哦~</div>
					</div>
					<!-- 视频元素 -->
					<div
						style="
							overflow: hidden;
							width: 100%;
							height: 100%;
							border-radius: 20px;
						"
						v-else
					>
						<video
							video
							ref="videoElement"
							class="video-player"
							style="width: 100%"
							autoplay
							v-if="!recordedBlobUrl"
						></video>
						<video
							v-else
							ref="record"
							class="video-player"
							style="width: 100%"
							autoplay
							controls
						></video>
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
					@click="startTranslation"
				>
					开始翻译
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
				<!-- <div
					class="bk_linear"
					style="width: 80%; height: 80%; margin-top: 25px"
					:style="{
						boxShadow: this.$store.state.theme_is_light
							? '0 10px 50px 0 #bfbfbf'
							: '0 10px 50px 0 #000',
					}"
				> <div
						style="
							display: flex;
							align-items: center;
							justify-content: center;
							color: rgb(123, 123, 123);
							height: 100%;
						"
						v-if="!translate"
					>
						现在还没有翻译的文本信息哦~
					</div>
					<div style="margin: 20px 35px; font-size: 20px; height: 100%" v-else>
						<div style="text-align: left; height: 60%; width: 100%">
							{{ translatedText }}
						</div>
						<div style="height: 60%; width: 100%">
							<audio controls :src="audioURL"></audio>
						</div>
					</div>
					
				</div>
				--->
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
						<div class="audio-player-container">
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
									"
									v-if="!counter"
								>
									现在还没有翻译的文本哦~
								</div>
								<div style="text-align: left; padding: 10px 20px" v-else>
									{{ text }}
								</div>
							</div>
						</div>
					</div>
					<div style="display: flex; justify-content: center">
						<div
							class="sign"
							style="
								background-image: linear-gradient(to right, #81dcf8, #187fdc);
								color: white;
								margin: 15px auto;
								width: 160px;
							"
							@click="textToSpeech"
							
						>
							语音听读
						</div>
						 <!-- 音频播放器 -->
					</div>
					<div style="display: flex; justify-content: center">
						<div style="width: 100%; height: 50px">
							<audio
								style="width: 80%; height: 100%"
								controls
								:src="audioURL"
								ref="audioControler"
							></audio>
							<div class="play-button"></div>
							<div class="pause-button"></div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<style scoped>
.audio-player-container {
	width: 100%;
	display: flex;
	justify-content: center;
	margin-top: 30px;
}

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
.vedio_sign {
	position: absolute;
	top: 50%; /* 将组件垂直居中 */
	left: 50%; /* 将组件水平居中 */
	transform: translate(-50%, -50%); /* 通过平移来调整组件的中心点 */
}
</style>
