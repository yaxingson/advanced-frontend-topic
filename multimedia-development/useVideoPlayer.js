/**
 * @typedef {{ container:string, src:string, width:number }} VideoPlayOption
 * @param { VideoPlayOption } option 
 */
export function useVideoPlayer(option) {
  const { container, src, width } = option

  const containerEl = document.querySelector(container)
  const videoEl = document.createElement('video')

  const progressBar = document.createElement('div')
  const controlsGroup = document.createElement('div')

  videoEl.src = src

  const initSize = ()=>{
    const aspectRatio = videoEl.clientWidth / videoEl.clientHeight
    videoEl.width = width
    videoEl.height = width/aspectRatio
  }

  videoEl.addEventListener('canplay', initSize)

  videoEl.addEventListener('timeupdate', ev=>{})

  videoEl.addEventListener('')



  containerEl.appendChild(videoEl)

}
