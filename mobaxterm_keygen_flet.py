# -*- coding: utf-8 -*-
import zipfile
import flet as ft
from io import BytesIO
from flet import (FilePicker, FilePickerResultEvent, TextField, Column, Text, ElevatedButton)

# MobaXterm许可证生成的核心代码
VariantBase64Table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
VariantBase64Dict = {i: VariantBase64Table[i] for i in range(len(VariantBase64Table))}

class LicenseType:
    Professional = 1
    Educational = 3
    Personal = 4

def VariantBase64Encode(bs: bytes):
    result = b''
    blocks_count, left_bytes = divmod(len(bs), 3)
    for i in range(blocks_count):
        coding_int = int.from_bytes(bs[3 * i:3 * i + 3], 'little')
        block = VariantBase64Dict[coding_int & 0x3f]
        block += VariantBase64Dict[(coding_int >> 6) & 0x3f]
        block += VariantBase64Dict[(coding_int >> 12) & 0x3f]
        block += VariantBase64Dict[(coding_int >> 18) & 0x3f]
        result += block.encode()
    if left_bytes == 0:
        return result
    elif left_bytes == 1:
        coding_int = int.from_bytes(bs[3 * blocks_count:], 'little')
        block = VariantBase64Dict[coding_int & 0x3f]
        block += VariantBase64Dict[(coding_int >> 6) & 0x3f]
        result += block.encode()
        return result
    else:
        coding_int = int.from_bytes(bs[3 * blocks_count:], 'little')
        block = VariantBase64Dict[coding_int & 0x3f]
        block += VariantBase64Dict[(coding_int >> 6) & 0x3f]
        block += VariantBase64Dict[(coding_int >> 12) & 0x3f]
        result += block.encode()
        return result

def EncryptBytes(key: int, bs: bytes):
    result = bytearray()
    for i in range(len(bs)):
        result.append(bs[i] ^ ((key >> 8) & 0xff))
        key = result[-1] & key | 0x482D
    return bytes(result)

def GenerateLicense(Type: LicenseType, Count: int, UserName: str, MajorVersion: int, MinorVersion: int):
    assert (Count >= 0)
    LicenseString = '%d#%s|%d%d#%d#%d3%d6%d#%d#%d#%d#' % (
        Type, UserName, MajorVersion, MinorVersion, Count,
        MajorVersion, MinorVersion, MinorVersion,
        0, 0, 0)
    EncodedLicenseString = VariantBase64Encode(EncryptBytes(0x787, LicenseString.encode())).decode()
    
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        zip_file.writestr('Pro.key', data=EncodedLicenseString)
    
    return zip_buffer.getvalue(), "Custom.mxtpro"

# Flet应用主函数
def main(page: ft.Page):
    page.title = "MobaXterm 许可证生成器"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme = ft.Theme(font_family="Microsoft YaHei")
    
    page.window.width = 290
    page.window.height = 400
    page.window.resizable = False
    page.window.maximizable = False
    page.update()
    
    username_input = TextField(label="用户名", value="User", width=200, hint_text="例如: User")
    version_input = TextField(label="版本号", value="25.2", width=200, hint_text="例如: 25.2")
    count_input = TextField(label="授权数量", value="1", width=200, hint_text="默认: 1")
    
    status_message = Text(value="", color="green", size=12, font_family="SimHei")
    
    save_file_dialog = FilePicker()
    page.overlay.append(save_file_dialog)
    
    def generate_license(e):
        try:
            username = username_input.value.strip()
            version = version_input.value.strip()
            count = int(count_input.value.strip())
            
            try:
                MajorVersion, MinorVersion = version.split('.')[0:2]
                MajorVersion = int(MajorVersion)
                MinorVersion = int(MinorVersion)
            except Exception:
                status_message.value = "版本号格式错误，请使用X.Y格式"
                status_message.color = "red"
                page.update()
                return
            
            license_content, suggested_filename = GenerateLicense(
                LicenseType.Professional, count, username, MajorVersion, MinorVersion
            )
            
            status_message.value = "许可证已生成，准备保存"
            status_message.color = "green"
            page.update()
            
            save_file_dialog.save_file(
                file_name=suggested_filename,
                allowed_extensions=["mxtpro"],
                dialog_title="保存许可证文件"
            )
            
            page.user_data = {"license_content": license_content}
            
        except Exception as ex:
            status_message.value = f"生成失败: {str(ex)}"
            status_message.color = "red"
        finally:
            page.update()
    
    def on_file_saved(e: FilePickerResultEvent):
        if e.path and hasattr(page, 'user_data') and 'license_content' in page.user_data:
            try:
                with open(e.path, "wb") as f:
                    f.write(page.user_data["license_content"])
                
                status_message.value = f"许可证已保存到: {e.path}"
                status_message.color = "green"
            except Exception as ex:
                status_message.value = f"保存失败: {str(ex)}"
                status_message.color = "red"
            page.update()
    
    save_file_dialog.on_result = on_file_saved
    
    generate_button = ElevatedButton(
        text="生成许可证", 
        on_click=generate_license,
        bgcolor="#4285F4",
        color="white",
        width=200
    )
    
    howto_text = Text(
        value="将证书复制到MobaXterm安装目录并重启应用\nC:\\Program Files (x86)\\Mobatek\\MobaXterm", 
        size=12, 
        color="#666666",
        weight="normal",
        font_family="SimHei"
    )

    about_text = Text(
        value="仅供学习参考，请尊重知识产权", 
        size=12, 
        color="#666666",
        weight="normal",
        font_family="SimHei"
    ) 
       
    page.add(
        Column(
            [username_input, version_input, count_input, generate_button, status_message, howto_text, about_text],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        )
    )

# 运行应用
if __name__ == "__main__":
    ft.app(target=main)