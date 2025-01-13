import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from recognizer import extract_id_card_info, extract_name_from_id_card, extract_birthdate_from_id_card, extract_id_from_id_card, extract_address_from_id_card
from driving import extract_driving_license_info, format_driving_license_info # 导入行驶证识别模块
#按钮边角弧度
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def center_window(window, width=620, height=550):
    """Center a tkinter window on the screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    window.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

# 提取身份证信息的函数
def process_id_card_info(img_path):
    """提取身份证信息"""
    try:
        # 获取提取的身份证信息
        result_data = extract_id_card_info(img_path)

        text.insert(tk.END, f"识别成功！\n")
        
        # 提取姓名
        name = extract_name_from_id_card(result_data)
        if name:
            text.insert(tk.END, f"姓名: {name}\n")
        else:
            text.insert(tk.END, "未能识别姓名。\n")
        
        # 提取出生日期
        birthdate = extract_birthdate_from_id_card(result_data)
        if birthdate:
            birthdate = birthdate.replace("年", "/").replace("月", "/").replace("日", "")
            text.insert(tk.END, f"出生日期: {birthdate}\n")
        else:
            text.insert(tk.END, "未能识别出生日期。\n")
        
        # 提取身份证号
        id_number = extract_id_from_id_card(result_data)
        if id_number:
            text.insert(tk.END, f"身份证号: {id_number}\n")
        else:
            text.insert(tk.END, "未能识别身份证号。\n")
        
        # 提取住址
        address = extract_address_from_id_card(result_data)
        if address:
            address = " ".join(address.split())  # 移除多余的空格
            text.insert(tk.END, f"住址: {address}\n")
        else:
            text.insert(tk.END, "未能识别住址。\n")

    except Exception as e:
        text.insert(tk.END, f"发生错误: {str(e)}\n")

# 提取行驶证信息的函数
def process_driving_license_info(img_path):
    """提取行驶证信息并输出格式化结果"""
    try:
        # 获取提取的行驶证信息
        result_data = extract_driving_license_info(img_path)

        text.insert(tk.END, f"行驶证识别成功！\n")
        
        # 使用格式化函数来格式化结果，返回格式化后的字符串
        formatted_info = format_driving_license_info(result_data)

        # 输出格式化后的字符串，直接插入文本框
        text.insert(tk.END, formatted_info)

    except Exception as e:
        text.insert(tk.END, f"发生错误: {str(e)}\n")




# 打开身份证图片并进行图片识别
def open_image_and_process():
    img_path = filedialog.askopenfilename(title="选择身份证图片", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if img_path:
        process_id_card_info(img_path)

# 打开行驶证图片并进行图片识别
def open_driving_license_and_process():
    img_path = filedialog.askopenfilename(title="选择行驶证图片", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if img_path:
        process_driving_license_info(img_path)

# 复制文本到剪贴板
def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(text.get("1.0", tk.END))
    #messagebox.showinfo("提示", "文本已复制到剪贴板")

# 清空文本区
def clear_text():
    text.delete("1.0", tk.END)

# 创建GUI
def create_gui():
    global text, root
    root = tk.Tk()
    root.title("身份证与行驶证信息提取")
    center_window(root, 620, 550)
     # 设置主窗体背景颜色为白色
    root.configure(background="white")

    frame = tk.Frame(root)
    frame.pack(side=tk.LEFT, padx=0, pady=0, expand=True, fill='both')

    # 文本区
    text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=20, bg="#f0f0f0")
    text.pack(pady=20, expand=True, fill='both')

    # 右侧按钮框
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.RIGHT, padx=10, pady=10)

    # 按钮样式
    button_style = {
        "width": 20,
        "height": 2,
        "bg": "#87cefa",
        "font": ("Arial", 10),

    }



    # 按钮
    open_button = tk.Button(button_frame, text="上传身份证", command=open_image_and_process, **button_style)
    open_button.pack(pady=5)

    open_driving_license_button = tk.Button(button_frame, text="上传行驶证", command=open_driving_license_and_process, **button_style)
    open_driving_license_button.pack(pady=5)

    copy_button = tk.Button(button_frame, text="复制", command=copy_to_clipboard, **button_style)
    copy_button.pack(pady=5)

    clear_button = tk.Button(button_frame, text="清空", command=clear_text, **button_style)
    clear_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
