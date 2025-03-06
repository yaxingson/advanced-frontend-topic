export function isSupportType() {
  /**@type { HTMLVideoElement|HTMLAudioElement }*/
  const tag = document.createElement('')

  tag.canPlayType()

}

export function parseTime(second) {}
