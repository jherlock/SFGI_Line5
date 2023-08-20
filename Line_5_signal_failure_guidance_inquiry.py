import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os


class FaultGuideV3Updated:
    def __init__(self, root):
        self.root = root
        self.root.title("五号线信号故障指引查询")

        self.descriptions = [
            "紧急制动", "RM框", "ATP红色", "OBCU红点", "车库图标", "无线打叉"
        ]

        self.choices = {}
        for desc in self.descriptions:
            self.choices[desc] = tk.StringVar(value="否")

        for i, desc in enumerate(self.descriptions):
            label = ttk.Label(self.root, text=desc)
            label.grid(row=i, column=0, sticky=tk.W, padx=10, pady=5)

            yes_btn = ttk.Radiobutton(self.root, text="是", variable=self.choices[desc], value="是")
            yes_btn.grid(row=i, column=1, padx=5, pady=5)

            no_btn = ttk.Radiobutton(self.root, text="否", variable=self.choices[desc], value="否")
            no_btn.grid(row=i, column=2, padx=5, pady=5)

        # Load settings from file
        if os.path.exists('fault_data.json'):
            with open('fault_data.json', 'r', encoding="utf-8") as file:
                self.fault_combinations = json.load(file)
        else:
            self.fault_combinations = {}

        ttk.Button(self.root, text="提交", command=self.check_fault).grid(row=len(self.descriptions), column=0,
                                                                          columnspan=3, pady=20)

    def check_fault(self):
        selected_descriptions = [desc for desc, choice in self.choices.items() if choice.get() == "是"]
        selected_set = set(selected_descriptions)

        result = []
        for combination, explanation in self.fault_combinations.items():
            if set(combination.split("|")).issubset(selected_set):  # Split the string key back into a list
                result.append(explanation)

        if result:
            messagebox.showinfo("故障原因及处理方法", "\n".join(result))
        else:
            messagebox.showinfo("提示", "当前的选择组合没有匹配的故障原因，请进行设置或其他选择。")


class FaultSetupUpdated:
    def __init__(self, parent, fault_combinations):
        self.parent = parent
        self.fault_combinations = fault_combinations

        self.window = tk.Toplevel(self.parent)
        self.window.title("设置故障原因及处理方法")

        self.descriptions = [
            "紧急制动", "RM框", "ATP红色", "OBCU红点", "车库图标", "无线打叉"
        ]

        self.choices = {}
        for desc in self.descriptions:
            self.choices[desc] = tk.BooleanVar(value=False)

        for i, desc in enumerate(self.descriptions):
            chkbox = ttk.Checkbutton(self.window, text=desc, variable=self.choices[desc])
            chkbox.grid(row=i, column=0, sticky=tk.W, padx=10, pady=5)

        ttk.Label(self.window, text="可能的故障原因：").grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        self.fault_entry = ttk.Entry(self.window, width=50)
        self.fault_entry.grid(row=0, column=2, padx=10, pady=5)

        ttk.Label(self.window, text="处理方法：").grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        self.solution_entry = ttk.Entry(self.window, width=50)
        self.solution_entry.grid(row=1, column=2, padx=10, pady=5)

        btn_submit = ttk.Button(self.window, text="保存设置", command=self.save_setup)
        btn_submit.grid(row=2, column=1, columnspan=2, padx=10, pady=20)

    def save_setup(self):
        selected_descriptions = [desc for desc, choice in self.choices.items() if choice.get()]
        fault = self.fault_entry.get().strip()
        solution = self.solution_entry.get().strip()

        if not selected_descriptions or not fault or not solution:
            messagebox.showerror("错误", "请确保所有字段都已填写。")
            return

        key = "|".join(selected_descriptions)  # Convert list to a string key
        self.fault_combinations[key] = f"{fault}。处理方法：{solution}。"

        # Save to a file
        with open('fault_data.json', 'w', encoding="utf-8") as file:
            json.dump(self.fault_combinations, file, ensure_ascii=False, indent=4)

        messagebox.showinfo("成功", "设置已保存！")
        self.window.destroy()


class FaultGuideV5Updated(FaultGuideV3Updated):
    def __init__(self, root):
        super().__init__(root)
        # Add a button to open the fault setup window
        btn_setup = ttk.Button(self.root, text="设置故障原因及处理方法", command=self.open_setup)
        btn_setup.grid(row=len(self.descriptions) + 1, column=0, columnspan=3, pady=20)

    def open_setup(self):
        # Open the fault setup window
        FaultSetupUpdated(self.root, self.fault_combinations)


# 创建主窗口并运行应用程序
root = tk.Tk()
app = FaultGuideV5Updated(root)
root.mainloop()
