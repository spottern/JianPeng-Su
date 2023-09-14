import re
import jieba
from simhash import Simhash
import time
from memory_profiler import profile
# 原始文本错误定义类
class FileError(Exception):
    def __init__(self, file_path, error_message):
        self.file_path = file_path
        self.error_message = error_message

    def __str__(self):
        return f"Error accessing file '{self.file_path}': {self.error_message}"
# 抄袭文本错误定义类
class SimilarityCalculationError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


# 查重函数，接口为初始文本和抄袭文本
@profile
def check_similarity(original, copy):
    # 创建了一个正则表达式模式
    regex = re.compile(r'[\u4e00-\u9fa5]+')

    try:
        # 删除标点
        cl_test1 = re.findall(regex, original)
        cl_test2 = re.findall(regex, copy)

        # 将删除标点后的文本以字符串的形式存储
        original = ''.join(cl_test1)
        copy = ''.join(cl_test2)

        # 对字符串进行分词
        original_words = list(jieba.cut(original))
        copy_words = list(jieba.cut(copy))

        # 生成simhash值
        original_simhash = Simhash(original_words)
        copy_simhash = Simhash(copy_words)

        # 计算海明距离
        distance = original_simhash.distance(copy_simhash)
        # 计算查重率
        final = 1 - distance / 64
        return final

    except ValueError:
        raise SimilarityCalculationError("Error calculating similarity. Please check the input text.")


# 输入文件
original_text = input('输入原文文件路径：')
copy_text = input('输入抄袭版论文文件路径：')
result = input('输入答案文件保存路径：')

# 开始性能和内存监测
start_time = time.time()

try:
    # 读取原始文件
    with open(original_text, 'r', encoding='utf-8') as f1:
        text1 = f1.read()
        if not text1:
            raise FileError(original_text, "Original text file is empty.")

    # 读取抄袭文件
    with open(copy_text, 'r', encoding='utf-8') as f2:
        text2 = f2.read()
        if not text2:
            raise FileError(copy_text, "Copy text file is empty.")

    similarity = check_similarity(text1, text2)

    # 结束性能和内存监测
    end_time = time.time()

    # 输出结果到指定文本中
    with open(result, 'w', encoding='utf-8') as f3:
        # 以百分比形式呈现到文本中
        f3.write('抄袭版论文与原文的重复率为：{:.2f}%'.format(similarity * 100))
        f3.write('\n')
        f3.write('程序执行时间：{:.2f}秒'.format(end_time - start_time))

    print('抄袭版论文与原文的重复率为：{:.2f}%'.format(similarity * 100))
    print('程序执行时间：{:.2f}秒'.format(end_time - start_time))
# 模块异常结果
except FileError as e:
    print(f"错误获取原文文件 '{e.file_path}': {e.error_message}")

except SimilarityCalculationError as e:
    print(f"错误获取抄袭文本文件: {e}")

except Exception as e:
    print(f"输出结果错误: {e}")
