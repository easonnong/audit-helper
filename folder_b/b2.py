import requests

def send_http_request(url, method='GET', headers=None, data=None):
    response = requests.request(method, url, headers=headers, data=data)
    return response

# 请求
requests_list = [
    {
        'url': 'https://b1_1.com/api/endpoint1',
        'method': 'GET',
        'headers': {'Content-Type': 'application/json'},
        'data': None
    },
    {
        'url': 'https://a1_2.com/api/endpoint2',
        'method': 'POST',
        'headers': {'Content-Type': 'application/json'},
        'data': '{"key": "value"}'
    },
    {
        'url': 'http://b2_3.com/api/endpoint2',
        'method': 'POST',
        'headers': {'Content-Type': 'application/json'},
        'data': '{"key": "value"}'
    },
    {
        'url': 'https://google.com/api/endpoint',
        'method': 'POST',
        'headers': {'Content-Type': 'application/json'},
        'data': '{"key": "value"}'
    },
    {
        'url': 'https://github.com/api/endpoint',
        'method': 'POST',
        'headers': {'Content-Type': 'application/json'},
        'data': '{"key": "value"}'
    },
]

# 获取响应
for req in requests_list:
    url = req['url']
    method = req['method']
    headers = req['headers']
    data = req['data']
    
    response = send_http_request(url, method, headers, data)
    print(f'Response for {url}:')
    print(f'Status Code: {response.status_code}')
    print(f'Content: {response.content}\n')