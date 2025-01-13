import os
import sys
from PPOCR_api import GetOcrApi

def extract_id_card_info(img_path):
    """提取身份证信息"""
    try:
        # 获取程序的路径
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))

        # 初始化识别器对象，传入 PaddleOCR-json.exe 的路径
        ocr = GetOcrApi(os.path.join(application_path, r"PaddleOCR-json/PaddleOCR-json.exe"))

        # 调用 OCR 识别图像
        res = ocr.run(img_path)

        if res["code"] == 100 and res["data"]:
            return res["data"]
        else:
            raise Exception("无法识别图片，可能是图片质量问题。")
    except Exception as e:
        raise Exception(f"发生错误: {str(e)}")

def extract_name_from_id_card(result_data):
    """从OCR结果中提取姓名"""
    for item in result_data:
        if "姓名" in item["text"]:
            return item["text"].replace("姓名", "").strip()
    return None

def extract_id_from_id_card(result_data):
    """从OCR结果中提取身份证号"""
    for item in result_data:
        # 使用正则表达式匹配18位字符，包括数字和字母
        match = re.search(r'\b[A-Za-z0-9]{18}\b', item["text"])
        if match:
            return match.group(0)  # 返回提取到的身份证号
    return None

def extract_gender_and_ethnicity_from_id_card(result_data):
    """从OCR结果中提取性别和民族"""
    gender = None
    ethnicity = None
    for item in result_data:
        if "性别" in item["text"]:
            gender = item["text"].replace("性别", "").strip()
        if "民族" in item["text"]:
            ethnicity = item["text"].replace("民族", "").strip()

    # 如果性别和民族被合并成一段文本，手动拆分
    if gender and ethnicity is None:
        if "女" in gender and "汉" in gender:
            gender = "女"
            ethnicity = "汉"

    return gender, ethnicity

def extract_birthdate_from_id_card(result_data):
    """从OCR结果中提取出生日期"""
    for item in result_data:
        if "出生" in item["text"]:
            return item["text"].replace("出生", "").strip()
    return None

import re

def extract_address_from_id_card(result_data):
    """从OCR结果中提取住址"""
    address = []
    address_found = False  # 用于标记是否已找到住址

    for item in result_data:
        if "住址" in item["text"]:
            address.append(item["text"].replace("住址", "").strip())  # 住址字段处理
            address_found = True  # 找到住址
        elif address_found:  # 如果已经找到住址
            # 如果文本为身份证号或其他不相关的内容，则停止合并
            if "公民身份号码" in item["text"]:
                break  # 结束住址提取
            elif item["text"].strip():  # 如果当前文本不为空
                address.append(item["text"].strip())

    # 如果住址有多个部分，合并成一个完整的地址
    if address:
        # 合并所有部分并去掉所有空格
        address_str = "".join(address)
        return address_str.strip()  # 去除前后多余空格
    else:
        return None


