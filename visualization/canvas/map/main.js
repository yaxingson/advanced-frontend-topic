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
    api:'https://webapi.amap.com/maps?v=2.0&plugin=AMap.ToolBar,AMap.Scale,AMap.MapType&key=',
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

const addrInput = document.getElementById('address')


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

  if(type === 'gaode') {
    const map = new mapgl.Map('container', {
      zoom:15,
      viewMode:'2D',
      pitch:75,
      center:[117.225863,39.092505],
    })
  
    const marker = new mapgl.Marker({
      position: [117.225863,39.092505]
    })
  
    map.add(marker)
  
    map.addControl(new mapgl.Scale())
    map.addControl(new mapgl.ToolBar())
    map.addControl(new mapgl.MapType())

    const infoWin = new mapgl.InfoWindow({
      isCustom:true,
      content:`
      <div style="width:300px;height:180px;padding:10px;background-color:#fff;">
        hello,world
      </div>
      `   
    })

    marker.on('click', e => {
      infoWin.open(map, e.target.getPosition())
    })

    map.add(new mapgl.Polyline({
      path:[
        [117.225,39.092],
        [117.226,39.091],
        [117.227,39.090],
        [117.227,39.089],
        [117.227,39.088],
      ],
      strokeColor:'green',
      strokeWeight: 5,
      strokeStyle:'dashed'
    }))

    mapgl.plugin(['AMap.AutoComplete'], ()=>{
      const autoComplete = new mapgl.AutoComplete()
    })

    const address = '天津市河西区隆昌路科技馆公交站'
    const key = ''

    fetch(`https://restapi.amap.com/v3/geocode/geo?address=${address}&key=${key}`)
      .then(res=>res.json())
      .then(res=>{
        const pos = res.geocodes[0].location.split(',')

        map.setCenter(pos)

      })

  } else if(type === 'baidu') {
    setTimeout(()=>{
      const map = new mapgl.Map('container')
      const center = new mapgl.Point(117.22, 39.08)

      map.centerAndZoom(center, 15)
      map.enableScrollWheelZoom(true)

      map.addControl(new mapgl.LocationControl())
      map.addControl(new mapgl.ZoomControl())
      map.addControl(new mapgl.ScaleControl())

      const icon = new mapgl.Icon('./marker.png', new mapgl.Size(45, 50))
      const marker = new mapgl.Marker(center, { icon }) 

      marker.onclick = () => {
        const win = new mapgl.InfoWindow('当前位置', {
          width: 300,
          height: 180,
          title:'标题'
        })
        
        map.openInfoWindow(win, center)

      }

      map.addOverlay(marker)

      const geoCoder = new mapgl.Geocoder()
      const address = addrInput.value

      geoCoder.getPoint('天津市河西区隆昌路科技馆公交站', point=>{
        if(point) {
          map.centerAndZoom(point, 15)
          map.addOverlay(new mapgl.Marker(point, { icon }))
          map.removeOverlay(marker)
        } else {
          alert('您选择的地址没有解析到结果！')
        }
      }, '天津市')

      geoCoder.getLocation(new mapgl.Point(116.364, 39.993), result => {      
        if (result){      
          alert(result.address)
        }      
      })


    }, 500)
  
  } else {
    const map = new mapgl.Map('container')

  }

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
