import os
import re
import csv


def scan_sensitive_functions(folder, file, extension_exclude=None, report_file=None):
    sensitive_functions = []

    # to get the sensitive functions
    with open(file, 'r', errors='ignore') as f:
        sensitive_functions = [line.strip() for line in f]
    
    # to get the excluded extensions
    excluded_extensions = set()
    if extension_exclude:
        excluded_extensions = set(extension_exclude.split(','))

    # report list
    report = []

    # to walk through the folder
    for root, dirs, files in os.walk(folder):
        for filename in files:
            # check if the file extension is in the excluded list
            _, ext = os.path.splitext(filename)
            if ext.lower() in excluded_extensions:
                continue

            # combine the path
            filepath = os.path.join(root, filename)

            # open file and read lines
            with open(filepath, 'r', errors='ignore') as f:
                lines = f.readlines()
                for line_num, line in enumerate(lines, start=1):
                    # check if the line contains any sensitive function
                    for func_name in sensitive_functions:
                        pattern = r'\b{}\b'.format(re.escape(func_name))
                        if re.search(pattern, line, re.UNICODE | re.IGNORECASE):
                            # check if the function is commented out
                            if is_function_commented(lines, line_num, func_name, ext[1:]):
                                continue

                            report_item = {
                                'Function': func_name,
                                'Content': line.strip(),
                                'Path': filepath,
                                'Line': line_num
                            }
                            report.append(report_item)

    # save report
    if report_file:
        save_report_to_csv(report_file, report)
    else:
        folder_name = os.path.basename(folder)
        save_report_to_csv(f'outputs/scan_func/{folder_name}_scan_func.csv', report)


def is_function_commented(lines, line_num, func_name, ext):
    """
    check if the function is commented out
    """
    if ext == 'py':
        # Python
        for line in reversed(lines[:line_num-1]):
            line = line.strip()
            if line.startswith('#') or line == '':
                continue
            if func_name in line:
                return True
            return False
    elif ext == 'js':
        # JavaScript
        for line in reversed(lines[:line_num-1]):
            line = line.strip()
            if line.startswith('//') or line.startswith('/*') or line == '':
                continue
            if func_name in line:
                return True
            return False
    # ...

    return False


def save_report_to_csv(filename, report):
    sorted_report = sorted(report, key=lambda x: x['Line'])
    if not os.path.dirname(filename):
        filename = os.path.join(os.getcwd(), filename)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', newline='', encoding='utf-8', errors='ignore') as f:
        writer = csv.writer(f)
        writer.writerow(["Function", "Content", "Path", "Line"])
        for item in sorted_report:
            writer.writerow([item['Function'], item['Content'], item['Path'], item['Line']])