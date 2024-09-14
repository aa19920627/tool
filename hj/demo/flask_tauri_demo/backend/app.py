from flask import *
from flask_cors import *  # 导入 CORS

app = Flask(__name__)
CORS(app)  # 启用 CORS


@app.route('/api/generate-list', methods=['POST'])
def generate_list():
    # 获取请求数据
    data = request.get_json()
    print(f"Received data: {data}")  # 打印接收到的数据进行调试

    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    # 模拟根据 URL 返回的列表
    items = [
        "选择1",
        "选择2",
        "选择3"
    ]

    return jsonify({'items': items})


if __name__ == '__main__':
    app.run()
