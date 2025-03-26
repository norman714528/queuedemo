from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from azure.storage.queue import QueueServiceClient
import os
from dotenv import load_dotenv
import base64

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Azure Queue Storage 設定
connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
queue_name = os.getenv('QUEUE_NAME', 'myqueue')

def get_queue_service_client():
    return QueueServiceClient.from_connection_string(connection_string)

def get_queue_client():
    queue_service_client = get_queue_service_client()
    queue_client = queue_service_client.get_queue_client(queue_name)
    return queue_client

def get_all_queues():
    queue_service_client = get_queue_service_client()
    queues = []
    try:
        queues = list(queue_service_client.list_queues())
    except Exception as e:
        print(f"獲取 Queue 列表時發生錯誤：{str(e)}")
    return queues

def ensure_queue_exists():
    queue_service_client = get_queue_service_client()
    try:
        queue_client = queue_service_client.get_queue_client(queue_name)
        queue_client.get_queue_properties()
        print(f"Queue '{queue_name}' 已存在")
    except Exception:
        queue_service_client.create_queue(queue_name)
        print(f"已創建新的 Queue '{queue_name}'")

def get_message_content(message):
    try:
        # 使用 content 屬性來獲取訊息內容
        if hasattr(message, 'content'):
            return message.content
        # 如果沒有 content 屬性，嘗試使用 message_text
        elif hasattr(message, 'message_text'):
            return message.message_text
        # 如果都沒有，返回原始訊息
        else:
            return str(message)
    except Exception as e:
        print(f"獲取訊息內容時發生錯誤：{str(e)}")
        return "無法讀取訊息內容"

def get_messages():
    queue_client = get_queue_client()
    messages = []
    try:
        messages = queue_client.peek_messages(max_messages=32)
        # 獲取訊息內容
        for message in messages:
            message.content = get_message_content(message)
    except Exception as e:
        print(f"獲取訊息時發生錯誤：{str(e)}")
    return messages

@app.route('/')
def index():
    messages = get_messages()
    queues = get_all_queues()
    return render_template('index.html', messages=messages, queues=queues, current_queue=queue_name)

@app.route('/read')
def read_page():
    return render_template('read.html')

@app.route('/read/next')
def read_next():
    queue_client = get_queue_client()
    try:
        # 接收一筆訊息，設定隱藏時間為 1 秒
        messages = queue_client.receive_messages(visibility_timeout=1)
        # 將迭代器轉換為列表
        message_list = list(messages)
        if message_list:
            message = message_list[0]
            # 獲取訊息內容
            message_content = get_message_content(message)
            # 刪除已讀取的訊息
            queue_client.delete_message(message)
            return jsonify({
                'success': True,
                'message': {
                    'id': message.id,
                    'content': message_content
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': '沒有更多訊息'
            })
    except Exception as e:
        print(f"讀取訊息時發生錯誤：{str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/refresh')
def refresh():
    messages = get_messages()
    try:
        messages_data = [{'id': msg.id, 'content': msg.content} for msg in messages]
        return jsonify({'messages': messages_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add', methods=['POST'])
def add_message():
    message = request.form.get('message')
    if message:
        queue_client = get_queue_client()
        try:
            # 直接發送訊息，不需要編碼
            queue_client.send_message(message)
            flash('訊息已成功新增！', 'success')
        except Exception as e:
            flash(f'錯誤：{str(e)}', 'error')
    return redirect(url_for('index'))

@app.route('/delete/<message_id>')
def delete_message(message_id):
    queue_client = get_queue_client()
    try:
        # 使用 peek_messages 來查看訊息，這樣不會影響訊息的可見性
        messages = queue_client.peek_messages(max_messages=32)
        for message in messages:
            if message.id == message_id:
                # 找到要刪除的訊息後，使用 receive_messages 來獲取並刪除它
                received_messages = queue_client.receive_messages()
                for received_message in received_messages:
                    if received_message.id == message_id:
                        queue_client.delete_message(received_message)
                        flash('訊息已成功刪除！', 'success')
                        break
                break
    except Exception as e:
        flash(f'錯誤：{str(e)}', 'error')
    return redirect(url_for('index'))

@app.route('/change_queue', methods=['POST'])
def change_queue():
    global queue_name
    new_queue = request.form.get('queue_name')
    if new_queue:
        queue_name = new_queue
        ensure_queue_exists()
        flash(f'已切換到 Queue：{new_queue}', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    ensure_queue_exists()
    app.run(debug=True) 