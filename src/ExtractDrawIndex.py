import re
import sys

if len(sys.argv) < 3:
    print("请提供输入文件和输出文件的路径作为命令行参数")
    sys.exit(1)

input_file = sys.argv[1]    # 输入文件路径
output_file = sys.argv[2]   # 输出文件路径

total_triangles = 0
total_drawcmd = 0

# 打开输入文件和输出文件
with open(input_file, 'r') as input_f, open(output_file, 'w') as output_f:
    # 逐行读取输入文件内容
    for line in input_f:
        # 使用正则表达式匹配提取 vkCmdDrawIndexed(23754, 1) 这部分内容
        match = re.search(r'vkCmdDrawIndexed\(\d+,\s*\d+\)', line)

        if match:
            extracted_str = match.group()
            # 写入提取后的内容到输出文件
            output_f.write(extracted_str + "\n")

            indices, instances = map(int, extracted_str.split('(')[1].split(')')[0].split(', '))
            triangles = (indices // 3) * instances
            total_triangles += triangles
            total_drawcmd += 1

print(f"total_triangles : {total_triangles}")
print(f"total_drawcmd : {total_drawcmd}")
