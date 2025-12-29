#!/usr/bin/env python3

import json
import html
from datetime import datetime

# Read the conversation
conversation_file = '~/.claude/projects/-home-user-aoc-2025/5f87f76f-5c36-4c91-ab04-38acb5bcf7a9.jsonl'
conversation_file = conversation_file.replace('~', '/root')

messages = []
with open(conversation_file, 'r') as f:
    for line in f:
        if line.strip():
            messages.append(json.loads(line))

# Generate HTML
html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advent of Code 2025 Day 12 - Conversation Transcript</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
            line-height: 1.6;
        }
        .message {
            margin: 20px 0;
            padding: 15px;
            border-radius: 8px;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .user-message {
            border-left: 4px solid #007bff;
        }
        .assistant-message {
            border-left: 4px solid #28a745;
        }
        .system-message {
            border-left: 4px solid #ffc107;
            background-color: #fff9e6;
        }
        .message-header {
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
        }
        .message-content {
            color: #555;
        }
        .tool-use {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 4px;
            padding: 10px;
            margin: 10px 0;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }
        .tool-result {
            background-color: #e7f3ff;
            border: 1px solid #b3d9ff;
            border-radius: 4px;
            padding: 10px;
            margin: 10px 0;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }
        .timestamp {
            font-size: 0.8em;
            color: #999;
            margin-top: 10px;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        pre {
            white-space: pre-wrap;
            word-wrap: break-word;
        }
    </style>
</head>
<body>
    <h1>Advent of Code 2025 Day 12 - Conversation Transcript</h1>
'''

for msg in messages:
    msg_type = msg.get('type', '')

    if msg_type == 'user':
        content = msg.get('message', {}).get('content', '')
        if isinstance(content, str):
            timestamp = msg.get('timestamp', '')
            html_content += f'''
    <div class="message user-message">
        <div class="message-header">User</div>
        <div class="message-content">{html.escape(content)}</div>
        <div class="timestamp">{timestamp}</div>
    </div>
'''
        elif isinstance(content, list):
            # Tool results
            for item in content:
                if item.get('type') == 'tool_result':
                    tool_content = item.get('content', '')
                    html_content += f'''
    <div class="message user-message">
        <div class="message-header">Tool Result</div>
        <div class="tool-result"><pre>{html.escape(str(tool_content))}</pre></div>
    </div>
'''

    elif msg_type == 'assistant':
        message = msg.get('message', {})
        content = message.get('content', '')

        if isinstance(content, list):
            text_parts = []
            tool_uses = []

            for item in content:
                if item.get('type') == 'text':
                    text_parts.append(item.get('text', ''))
                elif item.get('type') == 'tool_use':
                    tool_uses.append(item)

            if text_parts or tool_uses:
                timestamp = msg.get('timestamp', '')
                html_content += f'''
    <div class="message assistant-message">
        <div class="message-header">Claude</div>
'''
                if text_parts:
                    html_content += f'        <div class="message-content">{html.escape(" ".join(text_parts))}</div>\n'

                for tool in tool_uses:
                    tool_name = tool.get('name', 'Unknown')
                    tool_input = tool.get('input', {})
                    html_content += f'''        <div class="tool-use">
            <strong>Tool:</strong> {html.escape(tool_name)}<br>
            <strong>Input:</strong> <pre>{html.escape(json.dumps(tool_input, indent=2))}</pre>
        </div>
'''

                html_content += f'''        <div class="timestamp">{timestamp}</div>
    </div>
'''

    elif msg_type == 'system':
        # System messages (like hook feedback)
        html_content += f'''
    <div class="message system-message">
        <div class="message-header">System</div>
        <div class="message-content">{html.escape(str(msg))}</div>
    </div>
'''

html_content += '''
</body>
</html>
'''

# Write to file
output_file = '/home/user/aoc_2025/12/conversation.html'
with open(output_file, 'w') as f:
    f.write(html_content)

print(f"Conversation transcript saved to {output_file}")
