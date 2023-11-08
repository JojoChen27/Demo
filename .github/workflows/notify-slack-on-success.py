import sys
import json
import os
import subprocess

# 获取环境变量并保存到变量中
slack_webhook = sys.argv[1]
slack_message_title = os.getenv("SLACK_MESSAGE_TITLE")
pr_html_url = os.getenv("PR_HTML_URL")
pr_number = os.getenv("PR_NUMBER")
pr_title = os.getenv("PR_TITLE")
pr_body = os.getenv("PR_BODY")
pr_base_sha = os.getenv("PR_BASE_SHA")
pr_head_sha = os.getenv("PR_HEAD_SHA")

# 获取Body
if not pr_body:
    pr_body = "⭕ 未填写"
pr_body = f"*Description:*\n{pr_body}"
# print(pr_body)

# 获取提交信息
git_command = f'git log --pretty=format:"%H - %s (%an)" {pr_base_sha}..{pr_head_sha}'
commits = subprocess.check_output(git_command, shell=True, text=True)

# 提取每个提交的哈希和消息，并构建链接
formatted_commits = ""
for line in commits.splitlines():
    commit_hash = line.split()[0]
    commit_message = " ".join(line.split()[1:])
    commit_url = f"{pr_html_url}/commits/{commit_hash}"
    formatted_commit = f"<{commit_url}|{commit_message}>"
    formatted_commits += f"{formatted_commit}\n"
formatted_commits = f"*Commits:*\n{formatted_commits}"
# print(formatted_commits)

payload_data = {
    "blocks": [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": slack_message_title,
                "emoji": True
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "点击按钮进行下载"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "下载",
                    "emoji": True
                },
                "url": "http://3.33.146.9:5000/",
                "style": "primary"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"<{pr_html_url}|#{pr_number} {pr_title}>"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": pr_body
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": formatted_commits
            }
        }
    ]
}

# 将payload_data字典转换为JSON字符串
payload_json = json.dumps(payload_data, indent=2)
# print(payload_json)

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