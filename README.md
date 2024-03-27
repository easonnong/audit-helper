# audit-helper
🚀👩‍💻 a tool to help you audit your codebase 🚀👩‍💻

#
## Installation
### 1. Clone the repository
```
git clone https://github.com/easonnong/audit-helper.git
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
python main.py compare [-h] [-a TARGET_A] [-b TARGET_B] folder_a folder_b
```
example:
```
python main.py compare examples/folder_a examples/folder_b
```

**说明：此命令用于比较并记录 `folder_a` 目录和 `folder_b` 目录中各种特有的 HTTP/HTTPS 请求**

_必填参数_：
- folder_a & folder_b

_可选参数_：
- **-a** 指定 folder_a 中独特的 HTTP/HTTPS 请求的输出文件。文件应为 CSV 格式，可以包含文件路径
- **-b** 指定 folder_b 中独特的 HTTP/HTTPS 请求的输出文件。文件应为 CSV 格式，可以包含文件路径

_如果未提供 **-a** 和 **-b**，输出文件将默认存储在 `outputs/compare` 目录中_

### 2. Scan sensitive functions
```
python main.py scan_func [-h] [-e EXTENSION_EXCLUDE]
                         [-t TARGET_FILE]
                         folder file
```
example:
```
python main.py scan_func examples/folder_a examples/example_sensitive_func.txt
```
**说明：此命令用于从 `folder_a` 目录中提取敏感函数的信息。`file` 参数应指定包含要提取的函数名称的文本文件**

_必填参数_：
- **folder** 指定要扫描的目标目录
- **file** 指定包含要提取的函数名称的文件
  
_可选参数_：
- **-e** 指定要排除处理的文件扩展名。用法：_-e md,json,lock_
- **-t** 指定生成结果的输出文件。文件应为 CSV 格式，可以包含文件路径
  
_如果未提供 **-t**，输出文件将默认存储在 `outputs/scan_func` 目录中_

### 3. Scan urls
```
python main.py scan_url [-h] [-e EXTENSION_EXCLUDE]
                        [-t TARGET_FILE]
                        folder
```
example:
```
python main.py scan_url examples/folder_a -e md,json
```

**说明：此命令用于从 `folder` 目录中提取 HTTP/HTTPS/WSS 请求**

_必填参数_：
- `folder` 指定要扫描的目标目录
  
_可选参数_：
- **-e** 指定要排除处理的文件扩展名。用法：_-e md,json,lock_
- **-t** 指定生成结果的输出文件。文件应为 CSV 格式，可以包含文件路径

_如果未提供 **-t**，输出文件将默认存储在 `outputs/scan_url` 目录中_
