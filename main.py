import sys
import os
import re
import csv

# 文件类型
valid_extensions = ['.js', '.ts', '.java', '.tsx']

def has_image_extension(url_string):
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    for extension in image_extensions:
        if url_string.lower().endswith(extension):
            return True
    return False


def extract_content_before_special_characters(url_string):
    special_characters = ['(', ')', '[', ']', '{', '}', '`', '<', '>']
    for char in special_characters:
        index = url_string.find(char)
        if index != -1:
            url_string = url_string[:index]
    return url_string


def extract_url(url_string):
    # 去除尖括号、方括号、圆括号、花括号包裹的代码
    url_string = re.sub(r'<[^>]+?>|\[[^\]]+?\]|\([^\)]+?\}|\{[^\}]+?\}', '', url_string)
    match = re.search(r'(https?://[^"\',\s]+)', url_string)
    if match:
        url = match.group(1)
        url = url.split()[0]  # 提取第一个空格前的内容

        count = 0

        while True:
            pre_url = url
            # 去除所有HTML标签
            url = re.sub(r'<[^>]+?>|\[[^\]]+?\]|\([^\)]+?\}|\{[^\}]+?\}', '', url)
            url = re.sub(r'<[^>]+?>', '', url)

            # 去除双引号和单引号包裹代码
            url = url.strip('"\'')

            # 提取中文字符前的部分
            chinese_regex = r'[\u4e00-\u9fff]+'
            chinese_match = re.search(chinese_regex, url)
            if chinese_match:
                url = url.split(chinese_match.group(0))[0]
            # 补充，如果 URL 中间包含特殊字符（例如逗号、句点等）
            special_chars = ['，','。','！','？','；','：','）']
            for char in special_chars:
                if char in url:
                    url = url.split(char)[0]
                    break
            
            url = extract_content_before_special_characters(url)

            # 如果 URL 结尾是句点或逗号，去掉它
            if url.endswith('.') or url.endswith(',') or url.endswith(';'):
                url = url[:-1]

            # 如果 URL 中包含反斜杠，去除反斜杠及其后面的部分
            if '\\' in url:
                url = url.split('\\', 1)[0]
            
            # 如果 URL 结尾是斜杠，去掉它
            if url.endswith('/'):
                url = url[:-1]

            if pre_url == url:
                count+=1
                if count >= 2:
                    break
        
        return url
    
    return url_string


def extract_unique_requests(folder_a, folder_b):
    requests_a = set()
    requests_b = set()
    log_a = []
    log_b = []
    pattern = r'(https?://[^"\',\s]+)'

    def has_valid_extension(file_path):
        _, extension = os.path.splitext(file_path)
        return extension.lower() in valid_extensions

    def process_folder(folder, requests, log):
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                if has_valid_extension(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        for line_num, line in enumerate(lines, start=1):
                            matches = re.findall(pattern, line)
                            if matches:
                                for match in matches:
                                    url = extract_url(match.split()[0])
                                    if url not in requests and not has_image_extension(url):
                                        requests.add(url)
                                        log.append((url, line.strip(), file_path, line_num))

    process_folder(folder_a, requests_a, log_a)
    process_folder(folder_b, requests_b, log_b)

    unique_requests_a = requests_a - requests_b
    unique_requests_b = requests_b - requests_a

    def generate_report(requests, log):
        log_index = {entry[0]: entry for entry in log}
        report = [log_index[request] for request in requests if request in log_index]
        return report

    report_a = generate_report(unique_requests_a, log_a)
    report_b = generate_report(unique_requests_b, log_b)

    folder_a_name = os.path.basename(folder_a)
    folder_b_name = os.path.basename(folder_b)

    def save_report_to_csv(filename, report):
        sorted_report = sorted(report, key=lambda x: x[0])
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Requests", "Content", "Path", "Line"])
            writer.writerows(sorted_report)

    save_report_to_csv(f'{folder_a_name}.csv', report_a)
    save_report_to_csv(f'{folder_b_name}.csv', report_b)


if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[1] != "analyze":
        print("Usage: python main.py analyze folder_a folder_b")
    else:
        folder_a = sys.argv[2]
        folder_b = sys.argv[3]
        extract_unique_requests(folder_a, folder_b)