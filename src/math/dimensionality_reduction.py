class DimensionalityReduction:
    def __init__(self, max_length=1000):
        # 设置默认最大长度为1000，可以在初始化时传入其他值
        self.max_length = max_length

    def dr_from_text(self, text):
        # 检查单个文本的长度
        if len(text) > self.max_length:
            raise ValueError(f"Text length exceeds the maximum length of {self.max_length}.")
        # 处理文本
        pass

    def dr_from_texts(self, texts):
        # 检查多个文本的长度
        for text in texts:
            if len(text) > self.max_length:
                raise ValueError(f"Text length exceeds the maximum length of {self.max_length}.")
        # 处理文本列表
        pass