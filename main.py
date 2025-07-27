import tkinter as tk
from tkinter import filedialog, simpledialog, StringVar, Radiobutton, Label, Entry, Button
from PyPDF2 import PdfReader, PdfWriter

def select_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    return root.tk.splitlist(file_paths)

class RepeatDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("輸入重複次數和選擇模式")
        
        Label(self, text="請輸入重複次數 (n):").grid(row=0)
        self.repeat_count = Entry(self)
        self.repeat_count.grid(row=0, column=1)

        Label(self, text="選擇重複模式:").grid(row=1, columnspan=3)
        self.mode = StringVar()
        Radiobutton(self, text="一個一個檔案的重複", variable=self.mode, value="single_file").grid(row=2, column=0)
        Radiobutton(self, text="全部合併後再重複", variable=self.mode, value="merge_then_repeat").grid(row=2, column=1)
        Radiobutton(self, text="每頁重複再合併", variable=self.mode, value="page_repeat_merge").grid(row=2, column=2)

        self.mode.set("single_file")  # 預設選項為第一個

        self.ok_button = Button(self, text="確定", command=self.on_ok)
        self.ok_button.grid(row=3, columnspan=3)

        self.result = None

        self.center_dialog(parent)  # 將對話框置中

    def center_dialog(self, parent):
        # 獲取視窗大小
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()

        # 獲取螢幕大小
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # 設置視窗位置
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry('+{}+{}'.format(x, y))

    def on_ok(self):
        try:
            repeat_count = int(self.repeat_count.get())
        except ValueError:
            self.result = (None, None)
            self.destroy()
            return
        
        mode = self.mode.get()
        self.result = (repeat_count, mode)
        self.destroy()

def get_repeat_count_and_mode():
    dialog = RepeatDialog(root)
    root.wait_window(dialog)
    return dialog.result

def save_file():
    save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    return save_path

def repeat_and_merge_pdfs_single_file(file_paths, repeat_count):
    output = PdfWriter()
    for file_path in file_paths:
        # Read the file once and store its pages
        reader = PdfReader(file_path)
        pages = list(reader.pages)  # Convert to list to ensure proper copying
        
        # Repeat the entire file's pages
        for _ in range(repeat_count):
            for page in pages:
                output.add_page(page)
    return output

def merge_then_repeat_pdfs(file_paths, repeat_count):
    output = PdfWriter()
    # First, collect all pages from all files
    all_pages = []
    for file_path in file_paths:
        reader = PdfReader(file_path)
        pages = list(reader.pages)  # Convert to list to ensure proper copying
        all_pages.extend(pages)
    
    # Then repeat the entire merged collection
    for _ in range(repeat_count):
        for page in all_pages:
            output.add_page(page)
    return output

def repeat_and_merge_pdfs_by_page(file_paths, repeat_count):
    output = PdfWriter()
    for file_path in file_paths:
        reader = PdfReader(file_path)
        pages = list(reader.pages)  # Convert to list to ensure proper copying
        for page in pages:
            for _ in range(repeat_count):
                output.add_page(page)
    return output

def main():
    global root
    root = tk.Tk()
    root.withdraw()  # 隱藏主視窗
    
    file_paths = select_files()
    if not file_paths:
        print("未選取任何檔案，程式結束。")
        return
    
    repeat_count, mode = get_repeat_count_and_mode()
    if repeat_count is None:
        print("未輸入有效的重複次數或選擇模式，程式結束。")
        return
    
    output_pdf = None
    if mode == "single_file":
        output_pdf = repeat_and_merge_pdfs_single_file(file_paths, repeat_count)
    elif mode == "merge_then_repeat":
        output_pdf = merge_then_repeat_pdfs(file_paths, repeat_count)
    elif mode == "page_repeat_merge":
        output_pdf = repeat_and_merge_pdfs_by_page(file_paths, repeat_count)
    else:
        print("未選擇有效的重複模式，程式結束。")
        return
    
    save_path = save_file()
    if not save_path:
        print("未選取儲存路徑，程式結束。")
        return
    
    with open(save_path, "wb") as f:
        output_pdf.write(f)
    
    print(f"合併的PDF已儲存至: {save_path}")

    # 顯示主視窗並進入主迴圈
    # root.mainloop()
    return

if __name__ == "__main__":
    main()

# 主程式結束後，關閉Tk實例
root.quit()
root.destroy()
