from flask import Flask, request, send_from_directory, jsonify
import requests
import asyncio
import time


loop = asyncio.get_event_loop()
app = Flask(__name__, static_url_path='')

@app.route('/data/<path:path>')
def send_json(path):
    return send_from_directory('data', path)


@app.route('/')
def index():
    sources = [
        'http://localhost:5000/data/third.json',
        'http://localhost:5000/data/first.json',
        'http://localhost:5000/data/second.json'
    ]
    result = loop.run_until_complete(get_data(sources))
    print(result)
    return jsonify(result)

async def get_data(sources):
    loop = asyncio.get_event_loop()
    futures = list()
    responses = list()
    result = list()
    for source in sources:
        def req():
            response = requests.get(source, timeout=2)
            if response.status_code != 200:
                return None
            else:
                return response
        future = loop.run_in_executor(None, req)
        futures.append(future)
    for future in futures:
        response = await future
        if response is not None:
            responses.append(response)
    for response in responses:
        for item in response.json():
            result.append(item)
    return sorted(result, key = lambda i: i['id'])
    


if __name__ == '__main__':
    app.run()
