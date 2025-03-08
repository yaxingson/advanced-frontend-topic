async function call() {
  endpoint = 'https://api.deepseek.com/chat/completions'

  const response = await fetch(endpoint, {
    method:'POST',
    headers:{
      'Content-Type':'application/json',
      'Authorization':`Bearer sk-2694520577a04934b1ba83e42a8d30ed`
    },
    body:JSON.stringify({
      model:'deepseek-chat',
      messages:[
        {role:'user', content:'为什么天空是蓝色的？'}
      ],
      stream:false,
      temperature:1.3
    })
  })

  const result = await response.json()

  console.log(result.choices[0].message)
}
