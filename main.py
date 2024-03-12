import sys
import os
import re
import csv

def extract_unique_requests(folder_a, folder_b):
    requests_a = set()
    requests_b = set()
    log_a = []
    log_b = []
    pattern = r'(https?://[^"\',\s]+)'

    def process_folder(folder, requests, log):
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line_num, line in enumerate(lines, start=1):
                        matches = re.findall(pattern, line)
                        if matches:
                            url = matches[0].split()[0]
                            if url not in requests:
                                requests.add(url)
                                log.append((url, line.strip(), file_path, line_num))

    process_folder(folder_a, requests_a, log_a)
    process_folder(folder_b, requests_b, log_b)

    unique_requests_a = requests_a - requests_b
    unique_requests_b = requests_b - requests_a

    def generate_report(requests, log):
        report = []
        for request in requests:
            for log_entry in log:
                if log_entry[0] == request:
                    report.append(log_entry)
                    break
        return report

    report_a = generate_report(unique_requests_a, log_a)
    report_b = generate_report(unique_requests_b, log_b)

    folder_a_name = os.path.basename(folder_a)
    folder_b_name = os.path.basename(folder_b)

    def save_report_to_csv(filename, report):
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Requests", "Content", "Path", "Line"])
            writer.writerows(report)

    save_report_to_csv(f'{folder_a_name}.csv', report_a)
    save_report_to_csv(f'{folder_b_name}.csv', report_b)


if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[1] != "analyze":
        print("Usage: python main.py analyze folder_a folder_b")
    else:
        folder_a = sys.argv[2]
        folder_b = sys.argv[3]
        extract_unique_requests(folder_a, folder_b)