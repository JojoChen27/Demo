#!/bin/bash

# 获取PR信息
pr_url="$PR_HTML_URL"
pr_number="$PR_NUMBER"
pr_title="$PR_TITLE"

# 获取Body
pr_body="$PR_BODY"
escaped_pr_body="${pr_body//$'\n'/\\n}"
if [ -z "$escaped_pr_body" ]; then
  escaped_pr_body="未填写⭕"
fi
escaped_pr_body="*Description:*\n$escaped_pr_body"

# 获取提交信息
commits=$(git log --pretty=format:"%H - %s (%an)" "$PR_BASE_SHA..$PR_HEAD_SHA")
# 提取每个提交的哈希和消息，并构建链接
formatted_commits=""
while read -r line; do
  commit_hash=$(echo "$line" | awk '{print $1}')
  commit_message=$(echo "$line" | awk '{$1=""; print $0}')
  commit_url="$pr_url/commits/$commit_hash"
  formatted_commit="<$commit_url|${commit_message}>"
  formatted_commits="${formatted_commits}${formatted_commit}\n"
done <<< "$commits"
formatted_commits="*Commits:*\n$formatted_commits"

curl -X POST -H 'Content-type: application/json' --data @- $SLACK_WEBHOOK <<CURL_DATA
{
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "$SLACK_MESSAGE_TITLE",
        "emoji": true
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
          "emoji": true
        },
        "url": "http://3.33.146.9:5000/",
        "style": "primary"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "<$pr_url|#$pr_number $pr_title>"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "$escaped_pr_body"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "$formatted_commits"
      }
    }
  ]
}
CURL_DATA