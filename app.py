# -*- coding: utf-8 -*-
"""
Visual Wave Detection System - Streamlit Application
纯Python实现，可直接在PyCharm中运行
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import sys
import os
import subprocess
from datetime import datetime
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.database import Database
from backend.wave_detector import WaveDetector

DEFAULT_STREAMLIT_PORT = "8501"
DEFAULT_STREAMLIT_ADDRESS = "localhost"

def _running_in_streamlit() -> bool:
    """Check whether the script is executing inside a Streamlit runtime."""
    try:
        from streamlit.runtime import exists
    except (ImportError, ModuleNotFoundError):
        return False

    return exists()


def _get_cli_override(args, option_name: str) -> Optional[str]:
    """Extract a value for a Streamlit CLI option (supports = or space separated)."""
    for idx, arg in enumerate(args):
        if arg.startswith(f"{option_name}="):
            return arg.split("=", 1)[1]
        if arg == option_name and idx + 1 < len(args):
            return args[idx + 1]
    return None


def _filter_server_args(args):
    """Remove server address/port args so we can re-apply normalized values once."""
    filtered = []
    skip_next = False
    for arg in args:
        if skip_next:
            skip_next = False
            continue
        if arg in ("--server.port", "--server.address"):
            skip_next = True
            continue
        if arg.startswith("--server.port=") or arg.startswith("--server.address="):
            continue
        filtered.append(arg)
    return filtered


def _bootstrap_streamlit():
    """If executed directly, re-launch the app via `streamlit run`."""
    script_path = os.path.abspath(__file__)
    # Allow overriding defaults via environment for headless deployments
    fallback_port = os.environ.get("STREAMLIT_SERVER_PORT", DEFAULT_STREAMLIT_PORT)
    fallback_address = os.environ.get("STREAMLIT_SERVER_ADDRESS", DEFAULT_STREAMLIT_ADDRESS)
    user_args = sys.argv[1:]

    port_override = _get_cli_override(user_args, "--server.port")
    address_override = _get_cli_override(user_args, "--server.address")

    effective_port = port_override or fallback_port
    effective_address = address_override or fallback_address
    filtered_args = _filter_server_args(user_args)
    cleaned_args = [arg for arg in filtered_args if arg.strip()]

    print("⚡ 检测到直接运行 app.py，正在通过 Streamlit 启动应用...")
    print("⚡ Detected direct execution of app.py, launching via Streamlit...")
    print(f"🌐 配置的访问地址 / Configured URL: http://{effective_address}:{effective_port}")
    if effective_address not in ("localhost", "127.0.0.1"):
        print(f"💡 提示: 本机可使用 http://localhost:{effective_port} 访问")

    cmd = [
        sys.executable, "-m", "streamlit", "run", script_path,
        "--server.port", effective_port,
        "--server.address", effective_address
    ]
    cmd.extend(cleaned_args)

    try:
        result = subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        print("\n⏹️ Streamlit 已停止")
        sys.exit(0)
    except FileNotFoundError:
        print("❌ 无法启动 Streamlit: 未找到可执行文件，请确认已安装依赖 (pip install -r requirements.txt)")
        sys.exit(1)
    except PermissionError as exc:
        print(f"❌ 无法启动 Streamlit，权限不足: {exc}")
        sys.exit(1)
    except Exception as exc:
        print(f"❌ 无法启动 Streamlit: {exc}")
        sys.exit(1)

    if result.returncode != 0:
        print(f"❌ Streamlit 启动失败，返回码: {result.returncode}")
        sys.exit(result.returncode)


def initialize_app():
    """Configure page and session state."""
    st.set_page_config(
        page_title="波浪检测系统",
        page_icon="🌊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'db' not in st.session_state:
        st.session_state.db = Database()
        st.session_state.db.initialize()
    if 'detector' not in st.session_state:
        st.session_state.detector = WaveDetector()


def login_page():
    """登录页面"""
    st.title("🌊 Visual Wave Detection System")
    st.markdown("---")

    tab1, tab2 = st.tabs(["登录 (Login)", "注册 (Register)"])

    with tab1:
        st.subheader("用户登录")
        with st.form("login_form"):
            username = st.text_input("用户名 (Username)")
            password = st.text_input("密码 (Password)", type="password")
            submit = st.form_submit_button("登录 (Login)")

            if submit:
                if not username or not password:
                    st.error("请填写所有字段")
                else:
                    user = st.session_state.db.get_user_by_username(username)
                    if user and check_password_hash(user['password_hash'], password):
                        st.session_state.authenticated = True
                        st.session_state.user_id = user['id']
                        st.session_state.username = user['username']
                        st.success("登录成功！")
                        st.rerun()
                    else:
                        st.error("用户名或密码错误")

    with tab2:
        st.subheader("用户注册")
        with st.form("register_form"):
            reg_username = st.text_input("用户名 (Username)", key="reg_username")
            reg_email = st.text_input("邮箱 (Email)", key="reg_email")
            reg_password = st.text_input("密码 (Password)", type="password", key="reg_password")
            reg_password2 = st.text_input("确认密码 (Confirm Password)", type="password")
            register = st.form_submit_button("注册 (Register)")

            if register:
                if not reg_username or not reg_email or not reg_password:
                    st.error("请填写所有字段")
                elif reg_password != reg_password2:
                    st.error("两次密码不匹配")
                else:
                    existing_user = st.session_state.db.get_user_by_username(reg_username)
                    if existing_user:
                        st.error("用户名已存在")
                    else:
                        password_hash = generate_password_hash(reg_password)
                        user_id = st.session_state.db.create_user(
                            reg_username, password_hash, reg_email
                        )
                        if user_id:
                            st.success("注册成功！请登录")
                        else:
                            st.error("注册失败，请重试")


def detection_page():
    """波浪检测页面"""
    st.title("🌊 波浪检测 (Wave Detection)")

    # Sidebar for algorithm selection
    st.sidebar.title("检测设置 (Detection Settings)")

    algorithm = st.sidebar.selectbox(
        "选择算法 (Algorithm)",
        ["edge_detection", "frequency_analysis", "optical_flow", "ai_detection"],
        format_func=lambda x: {
            "edge_detection": "边缘检测 (Edge Detection)",
            "frequency_analysis": "频率分析 (Frequency Analysis)",
            "optical_flow": "光流法 (Optical Flow)",
            "ai_detection": "AI检测 (AI Detection)"
        }[x]
    )

    sensitivity = st.sidebar.slider(
        "灵敏度 (Sensitivity)",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.1
    )

    # Algorithm description
    algorithm_descriptions = {
        "edge_detection": "🔍 **边缘检测**: 使用Canny算法检测图像边缘，识别波浪边界。适合清晰的波浪轮廓。",
        "frequency_analysis": "📊 **频率分析**: FFT频域分析，识别周期性波浪模式。适合规律的波浪图案。",
        "optical_flow": "🎬 **光流法**: 计算光流场，检测运动波浪。适合动态波浪分析。",
        "ai_detection": "🤖 **AI检测**: 深度学习模型，智能识别复杂波浪模式。适应性强，准确度高。"
    }

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 算法说明")
    st.sidebar.info(algorithm_descriptions[algorithm])

    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("上传图像 (Upload Image)")
        uploaded_file = st.file_uploader(
            "选择图像文件 (JPG, PNG)",
            type=['jpg', 'jpeg', 'png'],
            help="上传需要检测波浪的图像文件"
        )

        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="上传的图像", use_container_width=True)

            # Detect button
            if st.button("🚀 开始检测 (Start Detection)", type="primary", use_container_width=True):
                with st.spinner("正在检测波浪..."):
                    # Convert PIL to OpenCV format
                    image_np = np.array(image)
                    if len(image_np.shape) == 2:  # Grayscale
                        image_cv = cv2.cvtColor(image_np, cv2.COLOR_GRAY2BGR)
                    else:  # RGB
                        image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

                    # Save temporary file for detection
                    temp_path = f"temp_{st.session_state.user_id}_{uploaded_file.name}"
                    cv2.imwrite(temp_path, image_cv)

                    try:
                        # Perform detection
                        result = st.session_state.detector.detect(
                            temp_path,
                            algorithm=algorithm,
                            sensitivity=sensitivity
                        )

                        # Save to database
                        detection_id = st.session_state.db.save_detection(
                            user_id=st.session_state.user_id,
                            filename=uploaded_file.name,
                            algorithm=algorithm,
                            result_data=result
                        )

                        # Store result in session state
                        st.session_state.last_result = result
                        st.session_state.last_detection_id = detection_id

                        st.success(f"检测完成！检测ID: {detection_id}")

                    finally:
                        # Clean up temp file
                        if os.path.exists(temp_path):
                            os.remove(temp_path)

    with col2:
        st.subheader("检测结果 (Detection Results)")

        if 'last_result' in st.session_state:
            result = st.session_state.last_result

            # Display metrics
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

            with metric_col1:
                st.metric("波浪数量 (Waves)", result['wave_count'])

            with metric_col2:
                st.metric("平均振幅 (Avg Amplitude)", f"{result['avg_amplitude']:.2f}")

            with metric_col3:
                st.metric("平均频率 (Avg Frequency)", f"{result['avg_frequency']:.4f}")

            with metric_col4:
                st.metric("置信度 (Confidence)", f"{result['confidence_score']:.2%}")

            # Display wave details
            st.markdown("---")
            st.markdown("### 波浪详情 (Wave Details)")

            if result['waves']:
                waves_df = pd.DataFrame(result['waves'])
                st.dataframe(waves_df, use_container_width=True)

                # Create visualization chart
                st.markdown("### 波浪特征图表 (Wave Characteristics)")
                if 'amplitude' in waves_df.columns:
                    st.bar_chart(waves_df['amplitude'][:20])
            else:
                st.info("未检测到波浪")
        else:
            st.info("上传图像并点击'开始检测'以查看结果")


def history_page():
    """历史记录页面"""
    st.title("📜 检测历史 (Detection History)")

    # Get user's detection history
    detections = st.session_state.db.get_user_detections(
        st.session_state.user_id,
        page=1,
        per_page=100
    )

    if not detections:
        st.info("暂无检测历史")
        return

    # Convert to DataFrame
    df = pd.DataFrame(detections)

    # Display summary statistics
    st.subheader("统计摘要 (Statistics)")
    col1, col2, col3, col4 = st.columns(4)

    stats = st.session_state.db.get_user_stats(st.session_state.user_id)

    with col1:
        st.metric("总检测次数", stats['total_detections'])
    with col2:
        st.metric("总波浪数", stats['total_waves'] or 0)
    with col3:
        st.metric("平均置信度", f"{(stats['avg_confidence'] or 0):.2%}")
    with col4:
        st.metric("最后检测时间", stats['last_detection'] or "无")

    st.markdown("---")

    # Display history table
    st.subheader("历史记录列表")

    # Format the dataframe
    display_df = df[['id', 'filename', 'algorithm', 'wave_count', 'avg_amplitude',
                     'avg_frequency', 'confidence_score', 'created_at']].copy()

    display_df.columns = ['ID', '文件名', '算法', '波浪数', '平均振幅',
                          '平均频率', '置信度', '检测时间']

    st.dataframe(display_df, use_container_width=True)

    # Export option
    st.markdown("---")
    st.subheader("导出数据 (Export Data)")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("导出为 CSV (Export as CSV)"):
            csv = display_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="下载 CSV 文件",
                data=csv,
                file_name=f"wave_detection_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

    with col2:
        if st.button("导出为 JSON (Export as JSON)"):
            json_str = df.to_json(orient='records', force_ascii=False, indent=2)
            st.download_button(
                label="下载 JSON 文件",
                data=json_str,
                file_name=f"wave_detection_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )


def algorithms_page():
    """算法介绍页面"""
    st.title("🔬 检测算法说明 (Detection Algorithms)")

    st.markdown("""
    本系统提供四种不同的波浪检测算法，每种算法适用于不同的场景：
    """)

    # Edge Detection
    st.markdown("---")
    st.markdown("### 1. 边缘检测 (Edge Detection)")
    st.markdown("""
    - **原理**: 使用Canny算法检测图像边缘，识别波浪边界
    - **适用场景**: 清晰的波浪轮廓，高对比度图像
    - **优点**: 快速，准确度高
    - **参数**: sensitivity控制边缘检测阈值
    """)

    # Frequency Analysis
    st.markdown("---")
    st.markdown("### 2. 频率分析 (Frequency Analysis)")
    st.markdown("""
    - **原理**: FFT频域分析，识别周期性波浪模式
    - **适用场景**: 规律的波浪图案，周期性结构
    - **优点**: 能识别频率特征，适合分析波动规律
    - **参数**: sensitivity控制峰值检测阈值
    """)

    # Optical Flow
    st.markdown("---")
    st.markdown("### 3. 光流法 (Optical Flow)")
    st.markdown("""
    - **原理**: 计算光流场，检测运动波浪
    - **适用场景**: 动态波浪，视频帧分析
    - **优点**: 能捕捉运动信息
    - **参数**: sensitivity控制运动阈值
    """)

    # AI Detection
    st.markdown("---")
    st.markdown("### 4. AI检测 (AI Detection)")
    st.markdown("""
    - **原理**: 深度学习模型，智能识别复杂波浪模式
    - **适用场景**: 复杂场景，多种波浪类型
    - **优点**: 适应性强，准确度高
    - **参数**: sensitivity控制置信度阈值
    """)


def profile_page():
    """用户信息页面"""
    st.title("👤 个人信息 (User Profile)")

    user = st.session_state.db.get_user_by_id(st.session_state.user_id)

    if user:
        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**用户ID:**")
            st.text(user['id'])

            st.markdown("**用户名:**")
            st.text(user['username'])

        with col2:
            st.markdown("**邮箱:**")
            st.text(user['email'])

            st.markdown("**注册时间:**")
            st.text(user['created_at'])

        # User statistics
        st.markdown("---")
        st.subheader("使用统计 (Usage Statistics)")

        stats = st.session_state.db.get_user_stats(st.session_state.user_id)

        metric_col1, metric_col2, metric_col3 = st.columns(3)

        with metric_col1:
            st.metric("总检测次数", stats['total_detections'])

        with metric_col2:
            st.metric("总波浪数", stats['total_waves'] or 0)

        with metric_col3:
            st.metric("平均置信度", f"{(stats['avg_confidence'] or 0):.2%}")


def main():
    """主应用程序"""
    initialize_app()

    # Check authentication
    if not st.session_state.authenticated:
        login_page()
        return

    # Sidebar navigation
    st.sidebar.title(f"👋 欢迎, {st.session_state.username}!")

    page = st.sidebar.radio(
        "导航 (Navigation)",
        ["🌊 波浪检测", "📜 检测历史", "🔬 算法说明", "👤 个人信息"],
        label_visibility="visible"
    )

    # Logout button
    if st.sidebar.button("退出登录 (Logout)", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 系统信息")
    st.sidebar.info("版本: 1.0.0\n\n纯Python实现\n可直接在PyCharm运行")

    # Route to appropriate page
    if page == "🌊 波浪检测":
        detection_page()
    elif page == "📜 检测历史":
        history_page()
    elif page == "🔬 算法说明":
        algorithms_page()
    elif page == "👤 个人信息":
        profile_page()


if __name__ == '__main__':
    if _running_in_streamlit():
        main()
    else:
        _bootstrap_streamlit()
