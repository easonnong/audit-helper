import os
import re
import csv

def extract_url(url_string):
    url_string = re.sub(r'<[^>]+?>|\[[^\]]+?\]|\([^\)]+?\}|\{[^\}]+?\}', '', url_string)
    match = re.search(r'(https?://[^"\',\s]+)', url_string)
    if match:
        url = match.group(1)
        url = url.split()[0]  

        count = 0

        while True:
            pre_url = url
            url = re.sub(r'<[^>]+?>|\[[^\]]+?\]|\([^\)]+?\}|\{[^\}]+?\}', '', url)
            url = re.sub(r'<[^>]+?>', '', url)

            url = url.strip('"\'')

            chinese_regex = r'[\u4e00-\u9fff]+'
            chinese_match = re.search(chinese_regex, url)
            if chinese_match:
                url = url.split(chinese_match.group(0))[0]
            special_chars = ['，','。','！','？','；','：','）']
            for char in special_chars:
                if char in url:
                    url = url.split(char)[0]
                    break
            
            url = extract_content_before_special_characters(url)

            if url.endswith('.') or url.endswith(',') or url.endswith(';'):
                url = url[:-1]

            if '\\' in url:
                url = url.split('\\', 1)[0]
            
            if url.endswith('/'):
                url = url[:-1]

            if pre_url == url:
                count+=1
                if count >= 2:
                    break
        
        return url
    
    return url_string


def scan_url_requests(folder_path, extension_exclude=None, output_filename=None):
    url_patterns = r'(http|https|wss)://([^\s/$.?#].[^\s]*)'
    excluded_extensions = set(extension_exclude.split(',')) if extension_exclude else set()
    urls = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_extension = os.path.splitext(file)[1]
            if not file_extension:
                continue
            file_extension = file_extension[1:]
            if file_extension not in excluded_extensions:
                file_path = os.path.join(root, file)
                with open(file_path, 'r', errors='ignore') as f:
                    lines = f.readlines()
                    for line_number, line in enumerate(lines, start=1):
                        matches = re.findall(url_patterns, line)
                        if matches:
                            for match in matches:
                                if match[1].startswith('github.com'):
                                    continue
                                url = extract_url(match[0] + "://" + match[1])
                                urls.append({
                                    'Requests': url,
                                    'Content': line.strip(),
                                    'Path': file_path,
                                    'Line': line_number
                                })

    if output_filename:
        save_report_to_csv(output_filename, urls)
    else:
        folder_name = os.path.basename(folder_path)
        save_report_to_csv(f'outputs/scan_url/{folder_name}_scan_url.csv', urls)

    return urls


def extract_content_before_special_characters(url_string):
    special_characters = ['(', ')', '[', ']', '{', '}', '`', '<', '>']
    for char in special_characters:
        index = url_string.find(char)
        if index != -1:
            url_string = url_string[:index]
    return url_string


def save_report_to_csv(filename, report):
    sorted_report = sorted(report, key=lambda x: x['Requests'])
    if not os.path.dirname(filename):
        filename = os.path.join(os.getcwd(), filename)
    os.makedirs(os.path.dirname(filename), exist_ok=True)  
    with open(filename, 'w', newline='', encoding='utf-8', errors='ignore') as f:
        writer = csv.writer(f)
        writer.writerow(["Requests", "Content", "Path", "Line"])
        for item in sorted_report:
            writer.writerow([item['Requests'], item['Content'], item['Path'], item['Line']])

