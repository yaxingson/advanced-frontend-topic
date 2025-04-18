"use strict"
import { useVideoPlayer } from './useVideoPlayer.js'

let isInit = false
let isPlaying = false

/**@type { AnalyserNode } */
let analyser = null

/**@type { Uint8Array } */
let dataArray = null

const videoEl = document.querySelector('video')
const audioEl = document.querySelector('audio')

const canvas = document.querySelector('canvas')
const ctx = canvas.getContext('2d')

function paint() {
  requestAnimationFrame(paint)

  ctx.clearRect(0, 0, canvas.width, canvas.height)

  analyser.getByteFrequencyData(dataArray)


}

videoEl.width = 700
videoEl.poster = ''


audioEl.addEventListener('play', ev=>{
  if(!isInit) {
    const ctx = new AudioContext()

    const source = ctx.createMediaElementSource(audioEl)
    analyser = ctx.createAnalyser()

    source.connect(analyser)

    analyser.connect(ctx.destination)
    analyser.fftSize = 512

    dataArray = new Uint8Array(analyser.frequencyBinCount)

    isInit = true
  }

  if(isPlaying) paint()
})

audioEl.addEventListener('pause', ev=>{

})

videoEl.addEventListener('canplay', ev=>{})
videoEl.addEventListener('ended', ev=>{})
videoEl.addEventListener('timeupdate', ev=>{})


document.addEventListener('keypress', ev=>{
  if(ev.key === ' ') {
    // alert(videoEl.buffered.start(0), videoEl.buffered.end(0))
    // alert(videoEl.currentSrc)
    // alert(videoEl.currentTime)
    // alert(videoEl.defaultPlaybackRate)
    // alert(videoEl.duration)
    // alert(videoEl.loop)
    // alert(videoEl.networkState)
    // alert(videoEl.readyState)
    // alert(videoEl.volume)
    // alert(videoEl.canPlayType('video/mp4'))

    videoEl.paused ? videoEl.play(): videoEl.pause()

  }
})


useVideoPlayer({
  container:'#container',
  src:'./assets/video/ocean.mp4',
  width:700,
  



})

