# 多媒体开发

## 背景

## 前置知识

> m3u8格式和WebVTT

常见的视频容器文件格式: `.wav`、`.ogg`、`.aac`、`.mp3`和`.wma`

音频编解码器: 

- AAC
- MPE-3
- OGG
- Vorbis

常见的视频容器文件格式: `.flv`、`.avi`、`.ogg`、`.mp4`和`.webm`

视频编解码器:

- H.264
- VP8
- Theora

## 实现技术

### CSS3

```css
video {
  object-fit:cover;
}

```

### HTML5 Video/Audio

#### Audio

`audio`标签属性:

- src
- controls
- autoplay


`HTMLAudioElement`的属性、方法和事件:

| 属性  | 描述 |
| ---  | ---- |

| 方法    | 描述  |
| -----  | ----- |

| 事件名称  |  描述  |
| -----   | -----  |

#### Video


`video`标签属性:

- src
- width
- height
- controls
- autoplay
- loop
- muted
- poster
- preload


`HTMLVideoElement`的属性、方法和事件:

| 属性  | 描述 |
| ---  | ---- |
| src   |
| width |
| height |
| clientWidth |
| clientHeight |
| paused  |
| muted   |
| currentTime |
| currentSrc  |
| duration  |
| playbackRate |
| volume |
| autoplay |
| buffered |
| controls |
| crossOrigin |
| defaultPlaybackRate |
| defaultMuted |
| loop |
| error |
| ended |
| networkState |
| played |
| preload |
| readyState |
| seekable |
| seeking |

| 方法    | 描述  |
| -----  | ----- |
| requestFullscreen | 
| play  |
| pause |
| canPlayType |
| addTextTrack |
| load |


| 事件名称  |  描述  |
| -----   | -----  |
| canplay |
| ended   |
| timeupdate |
| pause |
| play  |
| abort |
| suspend |

### Web APIs

- `window.AudioContext`
- `window.FileReader`
- `window.Uint8Array`

`AudioContext`对象的属性和方法:

| 方法   | 描述  |
| ----- | ----- |
| createMediaElementSource |
| createBufferSource |
| createAnalyser |
| decodeAudioData |


`AnalyserNode`对象的属性和方法:

| 属性 | 描述 |
| -----  | ----- |
| fftSize |
| frequencyBinCount |

| 方法  | 描述  |
| ----- | ----- |
| getByteFrequencyData |
| getByteTimeDomainData |


### WebRTC

## 库

- [video.js](https://github.com/videojs/video.js)
- [plyr](https://github.com/sampotts/plyr)
- [howler.js](https://github.com/goldfire/howler.js)
- [tone.js](https://github.com/Tonejs/Tone.js)
- [ffmpeg.js](https://github.com/Kagami/ffmpeg.js)
- [SimpleWebRTC](https://github.com/simplewebrtc/SimpleWebRTC)
- [peerjs](https://github.com/peers/peerjs)
- [fabric.js](https://github.com/fabricjs/fabric.js)
- [konva](https://github.com/konvajs/konva)
- [jimp](https://github.com/jimp-dev/jimp)

## 应用

### 流媒体

### 直播

### 音频可视化

## 工具

- <https://www.freeconvert.com/>
