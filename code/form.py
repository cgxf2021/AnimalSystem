import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from animal_system import AnimalSystem
from animal_system import Rule


class Form(object):
    def __init__(self) -> None:

        self.win = tk.Tk()
        self.animal = AnimalSystem()
        self.rulebase = str()
        self.conclusions = tk.StringVar()

        def initialize_rulebase():
            # 初始化规则库
            with open(file="./data/rulebase.txt", mode='r', encoding='utf_8') as file:
                rule = file.read()
            self.rulebase = rule
            self.rulebase_text.insert(tk.INSERT, self.rulebase)

        self.rulebase_label = ttk.Label(self.win, text="规则库", compound="center")
        self.input_label = ttk.Label(self.win, text="输入事实", compound="center")
        self.rulebase_text = scrolledtext.ScrolledText(self.win, width=40, height=25, wrap=tk.WORD)
        self.input_text = scrolledtext.ScrolledText(self.win, width=50, height=10, wrap=tk.WORD)
        self.deduce_button = ttk.Button(self.win, text="强行推理", width=8)
        self.deduce_process_label = ttk.Label(self.win, text="推理过程", compound="center")
        self.deduce_process_text = scrolledtext.ScrolledText(self.win, width=50, height=10, wrap=tk.WORD)
        self.add_new_rule_text = ttk.Entry(self.win, width=40)
        self.animal_label = ttk.Label(self.win, text="是啥动物？")
        self.add_new_rule_button = ttk.Button(self.win, text="添加新规则", width=10)
        self.animal_text = ttk.Entry(self.win, width=40)
        initialize_rulebase()
        self.animal.initialize_rulebase()
        

    def create_form(self):
        """
        description: 创建界面
        param: None
        Returns: None
        """

        # 设置主窗口
        self.win.title("Animal System")

        # 设置各部件位置
        self.rulebase_label.grid(column=0, row=0, padx=10, pady=5)
        self.input_label.grid(column=1, row=0, padx=10, pady=5)
        self.rulebase_text.grid(column=0, row=1, rowspan=4, padx=10)
        self.rulebase_text.configure(state='disabled')
        self.input_text.grid(column=1, row=1, padx=10)
        self.deduce_button.grid(column=1, row=2, padx=20, pady=5, sticky=tk.E)
        self.deduce_process_label.grid(column=1, row=3, padx=10, sticky=tk.W)
        self.deduce_process_text.grid(column=1, row=4, padx=10)
        self.add_new_rule_text.grid(column=0, padx=10, pady=8, sticky=tk.W)
        self.animal_label.grid(column=1, row=5, padx=10, pady=5, sticky=tk.W)
        self.add_new_rule_button.grid(column=0, row=6, padx=10, pady=10)
        self.animal_text.grid(column=1, row=6, padx=10, sticky=tk.W)
        self.animal_text.configure(state='disabled')
        

        def click_deduce_button():
            """
            description: 设置按钮回调函数
            """

            # 记录最终推理结果的字符串
            conclusions = str()
            # 从输入事实文本框读入字符串
            feature_str = self.input_text.get('1.0', 'end-1c')
            # 处理字符串
            if len(feature_str) != 0:
                feature = feature_str.split('\n')
                for item in feature[0: -1]:
                    keywords = set(item.split(' '))
                    # 调用animalsystem类中deduce方法进行推理
                    self.animal.deduce(keywords=keywords)
                    if len(self.animal.conclusion) != 0:
                        for con in self.animal.conclusion:
                            self.deduce_process_text.insert(tk.INSERT, con.toString())
                        self.deduce_process_text.insert(tk.INSERT, '\n')
                        conclusions += str(self.animal.conclusion[-1].conclusion) + ";"
                    else:
                        self.deduce_process_text.insert(tk.INSERT, "该知识超出了认识范畴\n\n")
                        conclusions += '?;'
                self.conclusions.set(conclusions)
                self.animal_text.configure(textvariable=self.conclusions)
            else:
                # 读入字符串为空
                self.conclusions.set('???')
                self.deduce_process_text.insert(tk.INSERT, "输入事实为空\n\n")
                self.animal_text.configure(textvariable=self.conclusions)


        def click_add_new_rule_button():
            """
            description: 添加新规则回调函数
            """

            rule_str = self.add_new_rule_text.get()
            rule = rule_str.split(' ')
            if len(rule) >= 2:
                rule = Rule(rule=rule)
                self.animal.add_rule(rule=rule_str)
                self.rulebase += rule_str + '\n'
                self.rulebase_text.configure(state='normal')
                self.rulebase_text.insert(tk.INSERT, rule_str + '\n')
                self.rulebase_text.configure(state='disabled')
            self.add_new_rule_text.configure(textvariable=tk.StringVar(value=""))
            self.animal.initialize_rulebase()


        # 设置推理按钮回调函数
        self.deduce_button.configure(command=click_deduce_button)

        # 设置添加规则按钮回调函数
        self.add_new_rule_button.configure(command=click_add_new_rule_button)

        self.win.mainloop()


if __name__ == "__main__":
    form = Form()
    form.create_form()