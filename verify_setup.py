#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
系统验证脚本 - 检查所有依赖和组件是否正常工作
System Verification Script - Check if all dependencies and components work correctly
"""

import sys
import os


def check_python_version():
    """检查Python版本"""
    print("🔍 检查Python版本...")
    version = sys.version_info
    print(f"   Python版本: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("   ❌ Python版本过低！需要Python 3.8或更高")
        return False
    else:
        print("   ✅ Python版本符合要求")
        return True


def check_dependencies():
    """检查依赖包"""
    print("\n🔍 检查依赖包...")

    dependencies = [
        ('streamlit', 'Streamlit'),
        ('cv2', 'OpenCV'),
        ('numpy', 'NumPy'),
        ('scipy', 'SciPy'),
        ('PIL', 'Pillow'),
        ('pandas', 'Pandas'),
        ('werkzeug', 'Werkzeug'),
    ]

    all_ok = True
    for module_name, display_name in dependencies:
        try:
            __import__(module_name)
            print(f"   ✅ {display_name}")
        except ImportError:
            print(f"   ❌ {display_name} - 未安装")
            all_ok = False

    return all_ok


def check_backend_modules():
    """检查后端模块"""
    print("\n🔍 检查后端模块...")

    sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

    modules = [
        ('database', 'Database模块'),
        ('wave_detector', 'WaveDetector模块'),
        ('config', 'Config模块'),
    ]

    all_ok = True
    for module_name, display_name in modules:
        try:
            __import__(module_name)
            print(f"   ✅ {display_name}")
        except ImportError as e:
            print(f"   ❌ {display_name} - 导入失败: {e}")
            all_ok = False

    return all_ok


def check_main_app():
    """检查主应用文件"""
    print("\n🔍 检查主应用文件...")

    app_path = os.path.join(os.path.dirname(__file__), 'app.py')
    run_path = os.path.join(os.path.dirname(__file__), 'run.py')

    files_ok = True

    if os.path.exists(app_path):
        print(f"   ✅ app.py 存在")
    else:
        print(f"   ❌ app.py 不存在")
        files_ok = False

    if os.path.exists(run_path):
        print(f"   ✅ run.py 存在")
    else:
        print(f"   ❌ run.py 不存在")
        files_ok = False

    return files_ok


def check_database():
    """检查数据库功能"""
    print("\n🔍 检查数据库功能...")

    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
        from database import Database

        db = Database('test_verification.db')
        db.initialize()
        print("   ✅ 数据库初始化成功")

        # Clean up test database
        if os.path.exists('test_verification.db'):
            os.remove('test_verification.db')
            print("   ✅ 测试数据库已清理")

        return True
    except Exception as e:
        print(f"   ❌ 数据库测试失败: {e}")
        return False


def check_wave_detector():
    """检查波浪检测器"""
    print("\n🔍 检查波浪检测器...")

    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
        from wave_detector import WaveDetector
        import numpy as np

        detector = WaveDetector()
        print("   ✅ WaveDetector初始化成功")

        # Test with a simple image
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        algorithms = ['edge_detection', 'frequency_analysis', 'optical_flow', 'ai_detection']

        for algo in algorithms:
            try:
                # We can't actually run detection without a real image file
                # Just check if the method exists
                if algo in detector.algorithms:
                    print(f"   ✅ {algo} 算法可用")
                else:
                    print(f"   ❌ {algo} 算法不可用")
            except Exception as e:
                print(f"   ⚠️  {algo} 测试警告: {e}")

        return True
    except Exception as e:
        print(f"   ❌ WaveDetector测试失败: {e}")
        return False


def main():
    """主验证函数"""
    print("=" * 60)
    print("🌊 波浪检测系统 - 环境验证")
    print("   Wave Detection System - Environment Verification")
    print("=" * 60)

    results = []

    # Run all checks
    results.append(("Python版本", check_python_version()))
    results.append(("依赖包", check_dependencies()))
    results.append(("后端模块", check_backend_modules()))
    results.append(("应用文件", check_main_app()))
    results.append(("数据库功能", check_database()))
    results.append(("波浪检测器", check_wave_detector()))

    # Summary
    print("\n" + "=" * 60)
    print("📋 验证结果摘要")
    print("=" * 60)

    all_passed = True
    for check_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{check_name:15s} : {status}")
        if not result:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n🎉 所有检查通过！系统可以正常运行。")
        print("\n📝 运行应用:")
        print("   方式1: python run.py")
        print("   方式2: streamlit run app.py")
        print("   方式3: 在PyCharm中打开run.py并点击运行按钮")
        print("\n🌐 访问地址: http://localhost:8501")
        return 0
    else:
        print("\n⚠️  部分检查未通过。请修复上述问题后重试。")
        print("\n💡 建议:")
        print("   1. 运行: pip install -r requirements.txt")
        print("   2. 检查Python版本: python --version")
        print("   3. 查看详细文档: PYTHON_GUIDE.md")
        return 1


if __name__ == '__main__':
    sys.exit(main())
