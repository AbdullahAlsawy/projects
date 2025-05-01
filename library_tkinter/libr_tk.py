import tkinter as tk

# إنشاء نافذة رئيسية
root = tk.Tk()
root.title("آلة حاسبة")

# متغير لعرض الأرقام والنتائج
entry_var = tk.StringVar()

# دالة لتنفيذ العمليات الحسابية
def button_click(value):
    current = entry_var.get()
    entry_var.set(current + str(value))

def clear():
    entry_var.set("")

def calculate():
    try:
        result = eval(entry_var.get())  # حساب المعادلة باستخدام eval
        entry_var.set(result)
    except Exception as e:
        entry_var.set("خطأ")

# إنشاء واجهة المستخدم
entry = tk.Entry(root, textvariable=entry_var, font=("Arial", 20), bd=10, relief="sunken", width=14, justify="right")
entry.grid(row=0, column=0, columnspan=4)

# أزرار الآلة الحاسبة
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('C', 4, 1), ('=', 4, 2), ('+', 4, 3),
]

# إضافة الأزرار إلى الواجهة
for (text, row, col) in buttons:
    if text == 'C':
        button = tk.Button(root, text=text, font=("Arial", 20), width=5, command=clear)
    elif text == '=':
        button = tk.Button(root, text=text, font=("Arial", 20), width=5, command=calculate)
    else:
        button = tk.Button(root, text=text, font=("Arial", 20), width=5, command=lambda value=text: button_click(value))
    button.grid(row=row, column=col)

# بدء التطبيق
root.mainloop()
