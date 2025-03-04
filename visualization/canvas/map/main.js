import * as echarts from 'https://unpkg.com/echarts@5.6.0/dist/echarts.esm.js'
import genJson from './gen/china.json' assert { type:'json' }

async function loadEnv() {
  const content = await fetch('./.env').then(res=>res.text())
  const entries = content.trim().replace(/"/g, '')
    .split('\r\n').map(row=>row.split('='))
  return Object.fromEntries(entries)
}

function loadScript(src) {
  return new Promise((resolve, reject)=>{
    const script = document.createElement('script')
  
    script.type = 'text/javascript'
    script.src = src

    script.onload = resolve
    script.onerror = reject

    document.body.appendChild(script)
  })
}

const MAP_CONFIG = {
  'gaode':{
    api:'https://webapi.amap.com/maps?v=2.0&plugin=AMap.ToolBar,AMap.Scale,AMap.MapType,AMap.AutoComplete&key=',
    global:'AMap'
  },
  'baidu':{
    api:'https://api.map.baidu.com/api?v=1.0&type=webgl&ak=',
    global:'BMapGL'
  },
  'tengxun':{
    api:'https://map.qq.com/api/gljs?v=1.exp&key=',
    global:'TMap'
  }
}

/**
 * 
 * @param {'gaode'|'baidu'|'tengxun'} type 
 * @param {{secretKey?:string, key:string}} option 
 */
async function createMapGL(type, option) {
  const { secretKey, key } = option

  if(type === 'gaode') {
    window._AMapSecurityConfig = {
      securityJsCode: secretKey
    }
  }

  const { api, global } = MAP_CONFIG[type]

  await loadScript(`${api}${key}&callback=initialize`)

  const mapgl = window[global]

  const map = new mapgl.Map('container', {
    zoom:15,
    viewMode:'2D',
    pitch:75,
    center:[117.225863,39.092505],
    plugins:['AMap.scale']
  })

  const marker = new mapgl.Marker({
    position: [117.225863,39.092505]
  })

  map.add(marker)

  map.addControl(new mapgl.Scale())
  map.addControl(new mapgl.ToolBar())
  map.addControl(new mapgl.MapType())



}

async function bootstrap() {
  const { searchParams } = new URL(location.href)
  const params = new URLSearchParams(searchParams)
  const keyword = params.get('kw')

  const env = await loadEnv()

  const mapgl = createMapGL('gaode', { 
    key:env['GAODE_KEY'], 
    secretKey:env['GAODE_SECURITY_KEY']
  })





}

bootstrap()
