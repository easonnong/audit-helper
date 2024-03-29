import os
import re
import csv
from tqdm import tqdm

def scan_sensitive_functions(folder, file, extension_exclude=None, report_file=None):
    sensitive_functions = []

    # to get the sensitive functions
    if not os.path.isabs(file):
        file = os.path.join(os.getcwd(), file)

    file_path = os.path.dirname(file)
    if not os.path.exists(file_path):
        os.makedirs(file_path, exist_ok=True)

    if not os.path.exists(file):
        open(file, 'w').close()
    else:
        with open(file, 'r', errors='ignore') as f:
            sensitive_functions = [line.strip() for line in f]
    
    # to get the excluded extensions
    excluded_extensions = set()
    if extension_exclude:
        excluded_extensions = {f".{ext.strip()}" for ext in extension_exclude.split(',')}

    # report list
    report = []

    progress_bar = tqdm(total=len(list(os.walk(folder))))

    # to walk through the folder
    for root, dirs, files in os.walk(folder):
        for filename in files:
            # check if the file extension is in the excluded list
            _, ext = os.path.splitext(filename)
            if not ext:
                continue
            if ext.lower() in excluded_extensions:
                continue

            # combine the path
            filepath = os.path.join(root, filename)

            # open file and read lines
            with open(filepath, 'r', errors='ignore') as f:
                lines = f.readlines()
                for line_num, line in enumerate(lines, start=1):
                    # remove redundant code
                    if len(line) > 1000:
                        continue
                    # check if the line contains any sensitive function
                    for func_name in sensitive_functions:
                        if is_partial_match(func_name, line):
                            # check if the function is commented out
                            if is_function_commented(line, func_name, ext[1:]):
                                continue

                            report_item = {
                                'Function': func_name,
                                'Content': line.strip(),
                                'Path': filepath,
                                'Line': line_num
                            }
                            report.append(report_item)
            
        progress_bar.update(1)

    progress_bar.close()

    # save report
    if report_file:
        save_report_to_csv(report_file, report)
    else:
        folder_name = os.path.basename(folder)
        save_report_to_csv(f'outputs/scan_func/{folder_name}_scan_func.csv', report)


def is_function_commented(line, func_name, ext):
    comment_syntax = {
        "py": r"^\s*(#|'''|\"\"\").*{}",
        "ts": r"^\s*(/\*|\*|//|`).*{}",
        "js": r"^\s*(/\*|\*|//|`).*{}",
        "mjs": r"^\s*(/\*|\*|//|`).*{}",
        "h": r"^\s*(/\*|\*|//|`).*{}",
        "c": r"^\s*(/\*|\*|//|`).*{}",
        "cpp": r"^\s*(/\*|\*|//|`).*{}",
        "java": r"^\s*(/\*|\*|//|`).*{}",
        # ...
    }

    comment_pattern = comment_syntax.get(ext)

    if comment_pattern:
        pattern = comment_pattern.format(func_name)

        if re.search(pattern, line, re.IGNORECASE):
            return True

    return False


def is_partial_match(substring, text):
    # . or [] or ()
    # pattern = r"(?<![a-zA-Z-])" + re.escape(substring) + r"(?=(?:\.|\[|\())"   
    # () 
    pattern = r"(?<![a-zA-Z-])" + re.escape(substring) + r"(?=(?:\())"    
    matches = re.findall(pattern, text, re.IGNORECASE)
    return any(match == substring for match in matches)


def save_report_to_csv(filename, report):
    sorted_report = sorted(report, key=lambda x: x['Function'])
    if not os.path.dirname(filename):
        filename = os.path.join(os.getcwd(), filename)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', newline='', encoding='utf-8', errors='ignore') as f:
        writer = csv.writer(f)
        writer.writerow(["Function", "Content", "Path", "Line"])
        for item in sorted_report:
            writer.writerow([item['Function'], item['Content'], item['Path'], item['Line']])