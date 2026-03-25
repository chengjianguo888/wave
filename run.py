#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单启动脚本 - 可在PyCharm中直接运行
Simple run script - can be run directly in PyCharm
"""

import subprocess
import sys
import os

def main():
    """启动Streamlit应用"""
    print("🌊 启动波浪检测系统...")
    print("🌊 Starting Wave Detection System...")
    print()
    print("提示: 应用将在浏览器中自动打开")
    print("Tip: The application will open automatically in your browser")
    print()
    print("按 Ctrl+C 停止应用")
    print("Press Ctrl+C to stop the application")
    print()

    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(script_dir, 'app.py')

    # Run Streamlit
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', app_path,
            '--server.port', '8501',
            '--server.address', 'localhost'
        ])
    except KeyboardInterrupt:
        print("\n\n应用已停止 (Application stopped)")
        sys.exit(0)


if __name__ == '__main__':
    main()
