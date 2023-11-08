import sys
import json
import os
import subprocess

slack_webhook = sys.argv[1]

# 定义要发送的JSON数据
payload_data = {
    "blocks": [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": os.getenv("SLACK_MESSAGE_TITLE"),
                "emoji": True
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "点击按钮查看运行错误"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "查看",
                    "emoji": True
                },
                "url": f"{os.getenv('GITHUB_SERVER_URL')}/{os.getenv('GITHUB_REPOSITORY')}/actions/runs/{os.getenv('GITHUB_RUN_ID')}",
                "style": "danger"
            }
        }
    ]
}

# 将payload_data字典转换为JSON字符串
payload_json = json.dumps(payload_data, indent=2)
print(payload_json)

# 使用subprocess执行curl命令
curl_command = [
    "curl",
    "-X", "POST",
    "-H", "Content-type: application/json",
    "--data", payload_json,
    slack_webhook
]

# 执行curl命令
try:
    subprocess.run(curl_command, check=True)
    print("JSON数据已成功发送到Slack Webhook。")
except subprocess.CalledProcessError as e:
    print(f"发送JSON数据到Slack Webhook时发生错误: {e}")
    exit(1)
