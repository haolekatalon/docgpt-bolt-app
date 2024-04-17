import re

# Define the pattern for Markdown links
pattern = r'\[([^\]]+)\]\(([^)]+)\)'

# Your input text containing Markdown links
input_text = "[Schedule a Test Suite](https://docs.katalon.com/katalon-platform/create-tests/create-tests-using-katalon-cloud-studio-beta/execute-katalon-cloud-studio-beta-tests/schedule-a-test-suite)"

# Function to replace Markdown links with <link|link text> pattern
def replace_markdown_links(match):
    link_text = match.group(1)
    link_url = match.group(2)
    return f'<{link_url}|{link_text}>'

# Perform the substitution
output_text = re.sub(pattern, replace_markdown_links, input_text)

print(output_text)
