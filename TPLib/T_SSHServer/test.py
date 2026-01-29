import os
import csv
import fnmatch

# 要统计的文件扩展名
exts = ('.py', '.c', '.cpp', '.pyw')

# 要排除的目录模式（完整列表，不省略）
exclude_dirs = (
    '.*',  # 所有隐藏目录
    'build',  # 精确匹配build目录
    'TESTWORK',  # 精确匹配TESTWORK目录
    '*.dist',  # 所有以.dist结尾的目录
    '*.build',  # 所有以.build结尾的目录
    'build*',  # 所有以build开头的目录
    '.*build',  # 所有以build结尾的隐藏目录
    'tool*-*'
)


def count_lines_and_chars(filepath):
    """统计单个文件的行数和字符数"""
    lines = 0
    chars = 0
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                lines += 1
                chars += len(line)
    except UnicodeDecodeError:
        try:
            with open(filepath, 'r', encoding='gbk') as f:
                for line in f:
                    lines += 1
                    chars += len(line)
        except:
            return 0, 0
    except:
        return 0, 0
    return lines, chars


def analyze_files(target_dir='.'):
    """递归分析目录下所有指定后缀名的文件（包括隐藏目录），严格排除指定目录"""
    results = []
    total_lines = 0
    total_chars = 0
    file_count = 0

    for root, dirs, files in os.walk(target_dir):
        # 严格排除所有指定目录模式
        dirs[:] = [
            d for d in dirs
            if not any(
                fnmatch.fnmatch(d, pattern)
                for pattern in exclude_dirs
            )
        ]

        for filename in files:
            if filename.endswith(exts):
                filepath = os.path.join(root, filename)
                lines, chars = count_lines_and_chars(filepath)
                rel_path = os.path.relpath(filepath, target_dir)
                results.append((rel_path, lines, chars))
                total_lines += lines
                total_chars += chars
                file_count += 1

    # 按文件路径排序结果
    results.sort()

    return results, total_lines, total_chars, file_count


def save_to_csv(results, csv_file='file_stats.csv'):
    """将结果保存到CSV文件"""
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['文件路径', '行数', '字符数'])
        writer.writerows(results)
    print(f"\n结果已保存到: {os.path.abspath(csv_file)}")


def print_summary(total_lines, total_chars, file_count):
    """打印统计摘要"""
    print("\n统计摘要:")
    print(f"{'总文件数:':<11}{file_count:>10,}")
    print(f"{'总行数:':<12}{total_lines:>10,}")
    print(f"{'总字符数:':<11}{total_chars:>10,}")


if __name__ == '__main__':
    import sys

    # 获取要统计的目录（默认为当前目录）
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'

    print(f"正在递归统计 {directory} 下的所有指定类型的文件...")

    results, total_lines, total_chars, file_count = analyze_files(directory)

    if file_count == 0:
        print("没有找到任何指定类型的文件")
    else:
        # 打印简要统计信息
        print_summary(total_lines, total_chars, file_count)

        # 保存到CSV
        csv_file = 'file_stats.csv'
        save_to_csv(results, csv_file)

        # 打印前10个文件作为示例
        print("\n示例文件（前10个）:")
        print(f"{'文件路径':<46}{'行数':>6}{'字符数':>12}")
        print('-' * 72)
        for item in results[:10]:
            print(f"{item[0][:48]:<50}{item[1]:>10,}{item[2]:>12,}")
        if len(results) > 10:
            print(f"...还有 {len(results) - 10} 个文件未显示（详见CSV文件）")
        print('-' * 72)

    os.system('pause')
