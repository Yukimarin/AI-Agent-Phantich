import os
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

class OutputValidator:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")

    def validate_json(self, file_path):
        """Kiểm tra xem file JSON có hợp lệ không."""
        if not os.path.exists(file_path):
            return False, f"File {file_path} không tồn tại."
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
            return True, ""
        except json.JSONDecodeError as e:
            return False, f"Lỗi cú pháp JSON: {str(e)}"
        except Exception as e:
            return False, f"Lỗi đọc file JSON: {str(e)}"

    def validate_chartjs(self, file_path):
        """Kiểm tra cú pháp Chart.js cơ bản trong HTML (lỗi thiếu ngoặc nhọn, ngoặc vuông)."""
        if not os.path.exists(file_path):
            return False, f"File {file_path} không tồn tại."
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Đếm số lượng ngoặc nhọn { } trong các thẻ script
            script_blocks = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
            for block in script_blocks:
                open_braces = block.count('{')
                close_braces = block.count('}')
                if open_braces != close_braces:
                    return False, f"Cú pháp JavaScript có thể bị lỗi: Số lượng ngoặc nhọn mở ({open_braces}) và đóng ({close_braces}) không khớp."
                    
            return True, ""
        except Exception as e:
            return False, f"Lỗi đọc file HTML: {str(e)}"

    def fix_with_llm(self, file_path, error_msg):
        """Gửi file lỗi lên LLM để sửa tự động."""
        print(f"Validator: Thử dùng LLM để sửa lỗi tại {file_path}...")
        
        if not self.api_key:
            print("Validator: Cảnh báo - Không tìm thấy GEMINI_API_KEY trong môi trường. Không thể dùng LLM tự động sửa.")
            return False
            
        try:
            # Ở đây chúng ta sẽ import thư viện gọi API.
            # Lưu ý: Cần google-genai. 
            from google import genai
            client = genai.Client(api_key=self.api_key)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            prompt = f"File sau bị lỗi cú pháp: {error_msg}\n\nHãy sửa lại toàn bộ nội dung file này. Chỉ trả về nội dung đã sửa, không thêm markdown hay giải thích gì khác.\n\nNội dung file:\n{content}"
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            
            fixed_content = response.text
            
            # Làm sạch nếu model cố tình trả về code block markdown
            if fixed_content.startswith("```"):
                lines = fixed_content.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines[-1].startswith("```"):
                    lines = lines[:-1]
                fixed_content = "\n".join(lines)
                
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
                
            print(f"Validator: LLM đã sửa và ghi đè file {file_path}.")
            return True
            
        except ImportError:
            print("Validator: Cảnh báo - Chưa cài đặt thư viện 'google-genai'. Vui lòng chạy 'uv pip install google-genai'.")
            return False
        except Exception as e:
            print(f"Validator: LLM sửa lỗi thất bại - {str(e)}")
            return False

def check_agent_output(file_path, file_type="json"):
    validator = OutputValidator()
    
    max_retries = 2
    for attempt in range(max_retries + 1):
        if file_type == "json":
            is_valid, err = validator.validate_json(file_path)
        elif file_type == "html":
            is_valid, err = validator.validate_chartjs(file_path)
        else:
            return True # Không biết check gì thì cho qua
            
        if is_valid:
            if attempt > 0:
                print(f"Validator: File {file_path} đã hợp lệ sau {attempt} lần sửa.")
            return True
            
        print(f"Validator: Phát hiện lỗi tại {file_path} (Lần thử {attempt+1}/{max_retries+1}) - Lỗi: {err}")
        
        if attempt < max_retries:
            success = validator.fix_with_llm(file_path, err)
            if not success:
                print("Validator: Không thể sửa bằng LLM. Từ bỏ vòng lặp.")
                break
        else:
            print("Validator: Đã hết số lần retry. Fallback kích hoạt.")
            
    return False

if __name__ == "__main__":
    if len(sys.argv) > 2:
        file_to_check = sys.argv[1]
        file_type = sys.argv[2]
        is_valid = check_agent_output(file_to_check, file_type)
        if not is_valid:
            sys.exit(1)
        else:
            sys.exit(0)
    else:
        print("Sử dụng: python validator.py <đường_dẫn_file> <json|html>")
