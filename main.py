from compare import extract_unique_requests
from scan_url import scan_url_requests
from scan_func import scan_sensitive_functions
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="main.py", description="Command-line tool")

    subparsers = parser.add_subparsers(dest="command")

    compare_parser = subparsers.add_parser("compare", help="Compare and retrieve unique HTTP/HTTPS requests from two directories")
    compare_parser.add_argument("folder_a", help="First directory path")
    compare_parser.add_argument("folder_b", help="Second directory path")
    compare_parser.add_argument("-a", "--target_a", help="Optional target file to save output A")
    compare_parser.add_argument("-b", "--target_b", help="Optional target file to save output B")

    scan_func_parser = subparsers.add_parser("scan_func", help="Perform sensitive function name scanning")
    scan_func_parser.add_argument("folder", help="Target directory")
    scan_func_parser.add_argument("file", help="Sensitive function names to be detected")
    scan_func_parser.add_argument("-e", "--extension_exclude", help="Comma-separated list of file extensions to be excluded")
    scan_func_parser.add_argument("-t", "--target_file", help="Optional target file to save output")

    scan_url_parser = subparsers.add_parser("scan_url", help="Scan for URL patterns (http/https/wss)")
    scan_url_parser.add_argument("folder", help="Target directory")
    scan_url_parser.add_argument("-e", "--extension_exclude", help="Comma-separated list of file extensions to be excluded")
    scan_url_parser.add_argument("-t", "--target_file", help="Optional target file to save output")

    help_parser = subparsers.add_parser("help", help="Show usage instructions")

    args = parser.parse_args()

    command = args.command
    if command == "compare":
        extract_unique_requests(args.folder_a, args.folder_b, args.target_a, args.target_b)
    elif command == "scan_func":
        scan_sensitive_functions(args.folder, args.file, args.extension_exclude, args.target_file)
    elif command == "scan_url":
        scan_url_requests(args.folder, args.extension_exclude, args.target_file)
    elif command == "help":
        parser.print_help()
    else:
        print("Invalid command. Type 'python main.py help' for usage instructions.")