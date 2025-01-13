# 身份证和行驶证内容识别提取

## 项目简介
这是一个基于 `PaddleOCR` 的身份证和行驶证内容识别提取工具。通过调用 OCR 技术，对图片中的文字内容进行解析，支持提取身份证和行驶证中的关键字段，如姓名、身份证号、性别、民族、出生日期、住址等信息。

## 功能
- **身份证识别**
  - 提取姓名、身份证号、性别、民族、出生日期、住址。
- **行驶证识别**
  - 提取车辆相关信息。

## 文件结构
```plaintext
身份证和行驶证内容识别提取/
├── driving.py                # 行驶证信息识别模块
├── recognizer.py             # 身份证信息识别模块
├── PPOCR_api.py              # PaddleOCR 接口封装
├── 身份证和行驶证内容识别提取.py # 主程序入口
├── PaddleOCR-json/           # PaddleOCR-json 程序目录
├── dist/                     # 编译好的程序，使用时和PaddleOCR-json 放在同目录
```

## 环境依赖
- Python 3.10 或以上版本
- `PaddleOCR-json`
- 需要在系统中安装以下 Python 包：
  - `re`
  - `os`
  - `sys`
  - 第三方依赖：
  - Pillow==9.1.1
  - ttkbootstrap（可选，当前未使用）

## 安装与运行

### 1. 克隆代码仓库
```bash
git clone https://github.com/suguangnet/ID-and-Driving-Extractor.git
cd ID-and-Driving-Extractor
```

### 2. 安装依赖
确保已安装 Python 3.10.7 及其它版本。安装所需依赖：
```bash
pip install -r requirements.txt
```

### 3. 配置 PaddleOCR-json
- 下载并解压 [PaddleOCR-json](https://github.com/hiroi-sora/PaddleOCR-json)。
- 本项目已包含。

### 4. 运行程序
```bash
python 身份证和行驶证内容识别提取.py
```

## 使用说明
1. 将身份证或行驶证的图片保存在本地。
2. 运行程序，根据提示上传图片。
3. 程序将自动识别图片中的内容，并输出识结果。

## 贡献
欢迎提交代码贡献或报告问题。你可以通过以下步骤贡献代码：
1. Fork 本仓库。
2. 创建你的功能分支：`git checkout -b feature/your-feature-name`。
3. 提交更改：`git commit -am 'Add some feature'`。
4. 推送分支：`git push origin feature/your-feature-name`。
5. 创建 Pull Request。

## 许可证
本项目基于 [MIT License](LICENSE)。

## 联系方式
速光网络软件开发 15120086569（vx同步）

##识别截图
![QQ截图20250113160357](https://github.com/user-attachments/assets/ae6b2a8a-cf7b-42b2-ae19-7ebbc2f0b0d4)
![QQ截图20250113160457](https://github.com/user-attachments/assets/31c0507c-270c-4d5f-a096-61e25fe5979d)

