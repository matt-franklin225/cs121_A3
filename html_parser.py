import re

"""
    Parse HTML content (as a str) and extract important text
    (i.e. bolded, title, etc)
"""
def parse_html_important_words(content: str) -> list:
    important_text = []

    bold_text = (re.findall(r'<b>(.*?)</b>', content)
                 + re.findall(r'<strong>(.*?)</strong>', content))

    headings = (re.findall(r'<h1>(.*?)</h1>', content)
                + re.findall(r'<h2>(.*?)</h2>', content)
                + re.findall(r'<h3>(.*?)</h3>', content)
                + re.findall(r'<h4>(.*?)</h4>', content))

    title = re.findall(r'<title>(.*?)</title>', content)

    important_text.extend(bold_text)
    important_text.extend(headings)
    important_text.extend(title)
    return important_text