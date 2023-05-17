# coding: utf-8
from fastapi import FastAPI, Request, Body, Response
from fastapi.middleware.cors import CORSMiddleware
from requests import get
# from uvicorn import run
import docker


client = docker.from_env()


app = FastAPI(
    title='docker',
    version='1.0.0',
    description='docker api',
    debug=True
)

app.add_middleware(
	CORSMiddleware,
	# 允许跨域的源列表，例如 ["http://www.example.org"] 等等，["*"] 表示允许任何源
	allow_origins=["*"],
	# 跨域请求是否支持 cookie，默认是 False，如果为 True，allow_origins 必须为具体的源，不可以是 ["*"]
	allow_credentials=False,
	# 允许跨域请求的 HTTP 方法列表，默认是 ["GET"]
	allow_methods=["*"],
	# 允许跨域请求的 HTTP 请求头列表，默认是 []，可以使用 ["*"] 表示允许所有的请求头
	# 当然 Accept、Accept-Language、Content-Language 以及 Content-Type 总之被允许的
	allow_headers=["*"],
	# 可以被浏览器访问的响应头, 默认是 []，一般很少指定
	# expose_headers=["*"]
	# 设定浏览器缓存 CORS 响应的最长时间，单位是秒。默认为 600，一般也很少指定
	# max_age=1000
)

def query_ip():
    try:
        res = get('http://ip-api.com/json', timeout=10)
        result = res.json()
        return result.get('query', 'docker.ip')
    except Exception:
        return 'timeout'

def tasks():
    ip = query_ip()
    for i in client.containers.list():
        print(i.stop())
        print(i.remove())
#     l = '-----'.join([str(i) for i in client.images.list()])
#     if not "traffmonetizer/cli:latest" in l:
#         client.images.pull('traffmonetizer/cli:latest')
    # res = client.containers.run("traffmonetizer/cli", "start accept --token jniTVESOzawsUvbUbprTL++Flag1g+CWwryIpJgGIK8= --device-name docker-1")

    res = client.containers.run(
        image="traffmonetizer/cli:latest", 
        command=f"-d --name tm start accept --token jniTVESOzawsUvbUbprTL++Flag1g+CWwryIpJgGIK8= --device-name {ip}",
        # volumes=["somevolume:/insidecontainer"],
        detach=True
    )
    return f'{str(res)}-{ip}'

@app.get('/')
def index():
    ip = query_ip()
    return {'ip': ip}

@app.get('/dockers')
def dockers():
    result = tasks()
    return Response(content=result,status_code=200, media_type='application/text; charset=utf-8')

# if __name__ == '__main__':
#     run(app='main:app', host= '0.0.0.0', port=1080,  reload=True)
