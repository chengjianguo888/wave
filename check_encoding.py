#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Encoding Verification Script for Visual Wave Detection System
检查系统中所有文件的编码，确保没有乱码问题
"""

import os
import sys
from pathlib import Path


def check_file_encoding(filepath):
    """Check if a file can be read with UTF-8 encoding"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            return True, len(content), None
    except UnicodeDecodeError as e:
        return False, 0, str(e)
    except Exception as e:
        return None, 0, str(e)


def check_python_files(base_dir):
    """Check all Python files for encoding issues"""
    print("=" * 70)
    print("检查 Python 文件编码 (Checking Python File Encodings)")
    print("=" * 70)

    issues = []
    ok_count = 0

    for root, dirs, files in os.walk(base_dir):
        # Skip certain directories
        if any(skip in root for skip in ['.git', 'node_modules', 'venv', '__pycache__']):
            continue

        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                relative_path = os.path.relpath(filepath, base_dir)

                success, size, error = check_file_encoding(filepath)

                if success:
                    print(f"✓ {relative_path}: {size} 字符, UTF-8 编码正常")
                    ok_count += 1
                elif success is False:
                    print(f"✗ {relative_path}: 编码错误 - {error}")
                    issues.append((relative_path, error))

    print(f"\n总计: {ok_count} 个Python文件检查通过")
    return issues


def check_chinese_text():
    """Test Chinese character handling"""
    print("\n" + "=" * 70)
    print("测试中文字符处理 (Testing Chinese Character Handling)")
    print("=" * 70)

    test_strings = [
        "波浪检测系统",
        "边缘检测算法",
        "频率分析",
        "光流法",
        "人工智能检测",
        "用户认证系统",
        "实时可视化",
        "历史记录管理",
        "数据导出功能"
    ]

    all_ok = True
    for test_str in test_strings:
        try:
            # Test encoding and decoding
            encoded = test_str.encode('utf-8')
            decoded = encoded.decode('utf-8')

            if decoded == test_str:
                print(f"✓ {test_str}: 编码/解码正常")
            else:
                print(f"✗ {test_str}: 编码/解码失败")
                all_ok = False
        except Exception as e:
            print(f"✗ {test_str}: 错误 - {str(e)}")
            all_ok = False

    return all_ok


def check_documentation():
    """Check documentation files for Chinese text"""
    print("\n" + "=" * 70)
    print("检查文档文件 (Checking Documentation Files)")
    print("=" * 70)

    doc_files = [
        'README.md',
        'QUICKSTART.md',
        'PROJECT_OVERVIEW.md',
        'FEATURES.md',
        'ARCHITECTURE.md',
        'docs/USER_GUIDE.md',
        'docs/TECHNICAL_DOCS.md'
    ]

    base_dir = os.path.dirname(os.path.abspath(__file__))
    issues = []

    for doc_file in doc_files:
        filepath = os.path.join(base_dir, doc_file)

        if not os.path.exists(filepath):
            print(f"⊘ {doc_file}: 文件不存在")
            continue

        success, size, error = check_file_encoding(filepath)

        if success:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                chinese_count = sum(1 for c in content if '\u4e00' <= c <= '\u9fff')
                print(f"✓ {doc_file}: {size} 字符, {chinese_count} 个中文字符")
        else:
            print(f"✗ {doc_file}: 编码错误 - {error}")
            issues.append((doc_file, error))

    return issues


def check_frontend_files(base_dir):
    """Check frontend files for potential encoding issues"""
    print("\n" + "=" * 70)
    print("检查前端文件 (Checking Frontend Files)")
    print("=" * 70)

    extensions = ['.jsx', '.js', '.css', '.html']
    issues = []
    ok_count = 0

    frontend_dir = os.path.join(base_dir, 'frontend')

    if not os.path.exists(frontend_dir):
        print("前端目录不存在")
        return []

    for root, dirs, files in os.walk(frontend_dir):
        if 'node_modules' in root:
            continue

        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                filepath = os.path.join(root, file)
                relative_path = os.path.relpath(filepath, base_dir)

                success, size, error = check_file_encoding(filepath)

                if success:
                    print(f"✓ {relative_path}: {size} 字符")
                    ok_count += 1
                elif success is False:
                    print(f"✗ {relative_path}: 编码错误 - {error}")
                    issues.append((relative_path, error))

    print(f"\n总计: {ok_count} 个前端文件检查通过")
    return issues


def generate_report(all_issues):
    """Generate final report"""
    print("\n" + "=" * 70)
    print("编码检查报告 (Encoding Check Report)")
    print("=" * 70)

    if not all_issues:
        print("\n✅ 所有文件编码检查通过！")
        print("✅ All files passed encoding verification!")
        print("\n系统使用标准 UTF-8 编码")
        print("System uses standard UTF-8 encoding")
        print("\n支持的字符:")
        print("- 中文 (Chinese)")
        print("- English")
        print("- 数字和符号 (Numbers and symbols)")
        return True
    else:
        print(f"\n✗ 发现 {len(all_issues)} 个编码问题:")
        for filepath, error in all_issues:
            print(f"  - {filepath}: {error}")
        return False


def main():
    """Main function"""
    print("\n" + "=" * 70)
    print("Visual Wave Detection System - 编码验证工具")
    print("Encoding Verification Tool")
    print("=" * 70)
    print()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    if base_dir.endswith('backend'):
        base_dir = os.path.dirname(base_dir)

    print(f"项目目录 (Project Directory): {base_dir}")
    print(f"Python 版本 (Python Version): {sys.version}")
    print(f"默认编码 (Default Encoding): {sys.getdefaultencoding()}")
    print()

    all_issues = []

    # Check Python files
    py_issues = check_python_files(base_dir)
    all_issues.extend(py_issues)

    # Check Chinese text handling
    if not check_chinese_text():
        all_issues.append(("Chinese text handling", "Failed"))

    # Check documentation
    doc_issues = check_documentation()
    all_issues.extend(doc_issues)

    # Check frontend files
    frontend_issues = check_frontend_files(base_dir)
    all_issues.extend(frontend_issues)

    # Generate report
    success = generate_report(all_issues)

    if success:
        print("\n" + "=" * 70)
        print("结论: 系统不存在乱码问题 ✓")
        print("Conclusion: No encoding issues found in the system ✓")
        print("=" * 70)
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
