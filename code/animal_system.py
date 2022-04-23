from email import header


class Rule(object):
    """
    description: 存储规则的数据结构
    """

    def __init__(self, rule) -> None:
        self.condition = set(rule[0: -1])
        self.conclusion = rule[-1]

    
    def toString(self):
        return str(self.condition) + '  ->  ' + str(self.conclusion) + '\n'



class AnimalSystem(object):
    """
    description: 动物识别系统类
    """
    
    def __init__(self) -> None:
        self.rulebase = list()
        self.conclusion = list()
        self.path = "./data/rulebase.txt"


    def initialize_rulebase(self):
        """
        description: 从本地txt文件中读入规则
        param: None
        Returns: None
        """

        with open(file=self.path, mode='r', encoding='utf_8') as file:
            rules = file.read().split("\n")
            for rule in rules:
                if len(rule) != 0:
                    self.rulebase.append(Rule(rule.split(" ")))
    

    def add_rule(self, rule):
        """
        description: 添加新规则
        param: rule 新的规则字符串类型
        Returns: None
        """
        with open(file=self.path, mode='a', encoding='utf_8') as file:
            file.writelines(rule + "\n")
        self.rulebase.append(Rule(rule.split(" ")))

    
    def deduce(self, keywords):
        """
        description: 进行推理
        param: keywords 关键词集合
        Returns: None
        """
        
        # 用于存放推理各步结论
        self.conclusion = list()
        while len(keywords) != 0:
            flag = 0
            for rule in self.rulebase:
                flag += 1
                # 判断集合R中是否有元素是输入事实的子集
                if rule.condition.issubset(keywords):
                    # 减去该子集
                    keywords = keywords - rule.condition
                    # 添加子集的结论
                    self.conclusion.append(rule)
                    if len(keywords) != 0:
                        keywords.add(rule.conclusion)
                        flag = 0
                        continue
                    else:
                        break
            if flag == len(self.rulebase) and len(keywords) != 0:
                self.conclusion = list()
                break


    def output(self):
        """
        description: 输出结果列表中的结果
        param: None
        Returns: None
        """

        if len(self.conclusion) != 0:
            for con in self.conclusion:
                print(con.condition, con.conclusion, sep=' -> ')
        else:
            print("该知识超出了认识范畴")