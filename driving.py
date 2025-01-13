import re
import os
import sys
from PPOCR_api import GetOcrApi

def extract_driving_license_info(img_path):
    """提取行驶证信息"""
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
'''
def format_driving_license_info(result_data):
    """通过正则表达式格式化行驶证信息"""
    formatted_info = {}

    # 将识别出的文本合并为一个字符串
    all_text = " ".join([item["text"] for item in result_data])

    # 正则表达式匹配各个字段
    license_plate_pattern = r"号牌号码\s*([A-Za-z0-9]+)"
    vehicle_type_pattern = r"车辆类型\s*([^\s]+)"
    owner_pattern = r"所有人\s*([^\s]+)"
    model_pattern = r"品牌型号\s*([^\s]+)"
    vin_pattern = r"车辆识别代号\s*([A-Za-z0-9]+)"
    engine_no_pattern = r"发动机号码\s*([A-Za-z0-9]+)"
    reg_date_pattern = r"注册日期\s*([0-9]{4}-[0-9]{2}-[0-9]{2})"
    issue_date_pattern = r"发证日期\s*([0-9]{4}-[0-9]{2}-[0-9]{2})"

    # 提取匹配的内容
    license_plate = re.search(license_plate_pattern, all_text)
    vehicle_type = re.search(vehicle_type_pattern, all_text)
    owner = re.search(owner_pattern, all_text)
    model = re.search(model_pattern, all_text)
    vin = re.search(vin_pattern, all_text)
    engine_no = re.search(engine_no_pattern, all_text)
    reg_date = re.search(reg_date_pattern, all_text)
    issue_date = re.search(issue_date_pattern, all_text)

    # 保存结果
    if license_plate:
        formatted_info["号牌号码"] = license_plate.group(1)
    if vehicle_type:
        formatted_info["车辆类型"] = vehicle_type.group(1)
    if owner:
        formatted_info["所有人"] = owner.group(1)
    if model:
        formatted_info["品牌型号"] = model.group(1)
    if vin:
        formatted_info["车辆识别代号"] = vin.group(1)
    if engine_no:
        formatted_info["发动机号码"] = engine_no.group(1)
    if reg_date:
        formatted_info["注册日期"] = reg_date.group(1)
    if issue_date:
        formatted_info["发证日期"] = issue_date.group(1)

    return formatted_info
'''
import re

def format_driving_license_info(result_data):
    """格式化行驶证信息，去除不需要的字段和字样"""
    if not isinstance(result_data, list):
        raise ValueError("输入的数据格式应为列表！")

    all_info = []  # 用于保存全部识别的文本信息

    # 定义模糊匹配的模式（去除一般字段和信息）
    unwanted_patterns = [
        r"中华人民共和国机动车行驶证",  # 去除行驶证标题
        r"Vehicle License of the People's Republic of China",  # 英文行驶证标题
        r"PlateNo[.]*",  # 去除 号牌号码
        r"VehicleType",  # 去除 车辆类型
        r"所有人",  # 去除 所有人
        r"住",  # 去除 地址中的住字
        r"址",  # 去除 地址中的址字
        r"Addres",  # 去除 地址相关字段
        r"使用性质",  # 去除 使用性质
        r"UseCharacter",  # 去除 使用性质相关字段
        r"Model",  # 去除 品牌型号
        r"VIN",  # 去除 车辆识别代号
        r"EngineNo",  # 去除 发动机号码
        r"^\.\.-\.\.$",  # 去除 "..-.."
        r"^\s*$",  # 去除空白行
        r"注册日期",  # 去除 注册日期
        r"发证日期",  # 去除 发证日期
        r"RegisterDate",  # 去除 注册日期
        r"IssueDate",  # 去除 发证日期
        #r"^\d{4}-\d{2}-\d{2}$",  # 去除日期格式
        r"^\D*省\D*市?.*$",  # 模糊匹配并去除省市地址信息
        r"^\D*区\D*$",  # 去除区域信息
        r"^\D*县\D*$",  # 去除县信息
        r"^\D*号$",  # 去除包含“号”的信息（常见于地址字段）
        r"^\D*Type$",
        r"^\D*Owner$",
        r"^\D*非营运$",
        r"^\D*市公安局交$",
        r"^\D*发动机号码$",
        r"^\D*通警察支队$",
        r"^\D*车辆类型$",
        r"^\D*号牌号码$",
        r"^\D*Republic$",
        r"^\D*Republic$",
    
    ]

    # 提取所有识别到的文本信息
    for item in result_data:
        if isinstance(item, dict):  # 确保每一项是字典
            text = item.get("text", "").strip()
            if text:  # 确保文本不为空
                # 使用正则表达式过滤掉不需要的字样
                for pattern in unwanted_patterns:
                    text = re.sub(pattern, "", text)

                if text:  # 如果去除后的文本仍然有内容，才加入
                    all_info.append(text)
        else:
            raise ValueError(f"列表中的元素应为字典，但检测到 {type(item)} 类型！")

    # 打印到控制台
    print("全部识别信息:")
    for idx, info in enumerate(all_info, 1):
        print(f"{idx}: {info}")

    # 返回格式化的字符串，用于文本区域显示
    return "\n".join(all_info)  # 将所有文本用换行符分隔拼接成字符串
