from langserve import RemoteRunnable

client = RemoteRunnable('http://localhost:8080/translate')

response = client.invoke({
  'language':'法语',
  'content':'人生苦短，我用Python'
})

print(response)
