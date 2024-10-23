import tkinter as tk

def calculate(operation):
    a = float(entry_a.get())
    b = float(entry_b.get())
    
    if operation == 'add':
        result = a + b
    elif operation == 'subtract':
        result = a - b
    elif operation == 'multiply':
        result = a * b
    elif operation == 'divide':
        result = a / b if b != 0 else "Error"
    
    label_result.config(text=f"Kết quả: {result}")


root = tk.Tk()
root.title("Máy tính đơn giản")

# Nhập số liệu
tk.Label(root, text="Nhập a:").grid(row=0, column=0)
entry_a = tk.Entry(root)
entry_a.grid(row=0, column=1)

tk.Label(root, text="Nhập b:").grid(row=1, column=0)
entry_b = tk.Entry(root)
entry_b.grid(row=1, column=1)

# Nút bấm
tk.Button(root, text="Cộng", command=lambda: calculate('add')).grid(row=2, column=0)
tk.Button(root, text="Trừ", command=lambda: calculate('subtract')).grid(row=2, column=1)
tk.Button(root, text="Nhân", command=lambda: calculate('multiply')).grid(row=3, column=0)
tk.Button(root, text="Chia", command=lambda: calculate('divide')).grid(row=3, column=1)

# Hiển thị kết quả
label_result = tk.Label(root, text="Kết quả: ")
label_result.grid(row=4, columnspan=2)

# Chạy ứng dụng
root.mainloop()