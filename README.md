# audit-helper
🚀👩‍💻 a tool to help you audit your codebase 🚀👩‍💻

#
## Installation
### 1. Clone the repository
```
git clone
```
    
### 2. Change directory
```
cd audit-helper
```

### 3. Run the tool for help
```
python main.py -h
```

## Usage

### 1. Compare
```
python main.py compare [-h] [--target_a TARGET_A] [--target_b TARGET_B] folder_a folder_b
```
example:
```
python main.py compare examples/folder_a examples/folder_b
```

### 2. Scan sensitive functions
```
python main.py scan_func [-h] [--extension_exclude EXTENSION_EXCLUDE]
                         [--target_file TARGET_FILE]
                         folder file
```
example:
```
python main.py scan_func examples/folder_a examples/example_sensitive_func.txt
```

### 3. Scan urls
```
python main.py scan_url [-h] [--extension_exclude EXTENSION_EXCLUDE]
                        [--target_file TARGET_FILE]
                        folder
```
example:
```
python main.py scan_url examples/folder_a --extension_exclude md,json
```
