import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import ctypes

def set_high_dpi():
    """Windows 환경 고해상도 설정"""
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except:
            pass

class FileRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("파일 이름 일괄 변경기")
        self.root.geometry("720x480")
        self.root.minsize(480, 400) # 최소 크기 제한
        
        self.selected_files = []

        # 창 크기 조절 시 내부 요소가 늘어나도록 설정
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(4, weight=1) # 하단 여백 조절

        self.setup_ui()

    def setup_ui(self):
        # 파일 선택 버튼 (상단 전체 너비)
        self.btn_select = tk.Button(self.root, text="파일 선택하기", command=self.select_files, height=2)
        self.btn_select.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="ew")
        
        self.lbl_status = tk.Label(self.root, text="선택된 파일이 없습니다.", fg="gray")
        self.lbl_status.grid(row=1, column=0, padx=20, pady=5, sticky="w")

        # 입력 및 옵션 영역을 감싸는 프레임
        input_frame = tk.Frame(self.root)
        input_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        input_frame.columnconfigure(1, weight=1) # 입력칸이 늘어나게 설정

        forbidden_text = '사용 금지 문자: \\ / : * ? " < > |'
        lbl_forbidden = tk.Label(input_frame, text=forbidden_text, fg="#d32f2f", font=("맑은 고딕", 9))
        lbl_forbidden.grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 5))

        # 이름 입력
        tk.Label(input_frame, text="새 파일 이름 : ", width=12, anchor="w").grid(row=0, column=0, pady=5)
        self.entry_name = tk.Entry(input_frame)
        self.entry_name.grid(row=0, column=1, pady=5, sticky="ew")

        # 정렬 옵션 (4가지 메뉴)
        tk.Label(input_frame, text="정렬 기준 : ", width=12, anchor="w").grid(row=1, column=0, pady=5)
        
        self.sort_options = [
            "기존 이름 (오름차순)", 
            "기존 이름 (내림차순)", 
            "수정시간 (과거순)", 
            "수정시간 (최신순)"
        ]
        self.selected_option = tk.StringVar()
        self.selected_option.set(self.sort_options[0])
        
        self.menu_option = ttk.Combobox(input_frame, textvariable=self.selected_option, values=self.sort_options, state="readonly")
        self.menu_option.grid(row=1, column=1, pady=5, sticky="ew")

        # 실행 버튼
        self.btn_run = tk.Button(self.root, text="이름 변경 시작", command=self.run_rename, 
                                 bg="#4CAF50", fg="white", font=("맑은 고딕", 10, "bold"), height=2)
        self.btn_run.grid(row=3, column=0, padx=20, pady=20, sticky="ew")

    def select_files(self):
        files = filedialog.askopenfilenames(
            title="이름을 바꿀 파일들을 선택하세요",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.webp *.bmp *.gif"), ("All files", "*.*")]
        )
        if files:
            self.selected_files = list(files)
            self.lbl_status.config(text=f"선택된 파일: {len(self.selected_files)}개", fg="black")

    def run_rename(self):
        if not self.selected_files:
            messagebox.showwarning("알림", "먼저 변경할 파일을 선택해 주세요.")
            return
            
        new_base_name = self.entry_name.get().strip()
        if not new_base_name:
            messagebox.showwarning("알림", "새로운 파일 이름을 입력해 주세요.")
            return

        # --- 정렬 로직 적용 ---
        current_sort = self.selected_option.get()
        
        if current_sort == "기존 이름 (오름차순)":
            self.selected_files.sort()
        elif current_sort == "기존 이름 (내림차순)":
            self.selected_files.sort(reverse=True)
        elif current_sort == "수정시간 (오름차순)":
            self.selected_files.sort(key=lambda x: os.path.getmtime(x))
        elif current_sort == "수정시간 (내림차순)":
            self.selected_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

        # 이름 변경 진행
        count = 0
        for index, old_path in enumerate(self.selected_files, start=1):
            folder_path = os.path.dirname(old_path)
            extension = os.path.splitext(old_path)[1]
            new_filename = f"{new_base_name}_{index}{extension}"
            new_path = os.path.join(folder_path, new_filename)

            try:
                os.rename(old_path, new_path)
                count += 1
            except Exception as e:
                print(f"오류 발생: {e}")

        messagebox.showinfo("완료", f"총 {count}개의 파일 이름을 성공적으로 변경했습니다!")
        self.selected_files = []
        self.lbl_status.config(text="선택된 파일이 없습니다.", fg="gray")
        self.entry_name.delete(0, tk.END)

if __name__ == "__main__":
    set_high_dpi()
    window = tk.Tk()
    app = FileRenamerApp(window)
    window.mainloop()
