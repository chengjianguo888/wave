# Visual Wave Detection System (纯Python版本)

一个基于计算机视觉的波浪检测系统，**纯Python实现**，可在PyCharm中直接运行！

## 🎯 核心特点

- ✅ **纯Python实现**: 无需JavaScript、Node.js或Docker
- ✅ **PyCharm一键运行**: 打开run.py直接运行
- ✅ **Streamlit界面**: 简洁美观的Web UI，全部用Python编写
- ✅ **多算法支持**: 边缘检测、频率分析、光流法、AI检测
- ✅ **用户认证**: 安全的登录注册系统
- ✅ **实时检测**: 支持图像上传和实时波浪检测
- ✅ **可视化分析**: 交互式图表和波浪标注
- ✅ **历史记录**: 保存所有检测历史，支持导出
- ✅ **数据导出**: CSV/JSON格式导出检测结果

### 创新特性
1. **多算法融合**: 四种不同的检测算法适应不同场景
   - 边缘检测: 基于Canny算法的经典边缘检测
   - 频率分析: FFT频域分析识别波浪模式
   - 光流法: 基于运动的波浪检测
   - AI检测: 深度学习模型智能识别

2. **智能参数调节**: 可调节灵敏度适应不同环境
3. **实时可视化**: 波浪边界标注和统计图表
4. **数据持久化**: 完整的用户数据和检测历史管理

## 系统架构 (纯Python版本)

```
wave-detection-system/
├── app.py                  # Streamlit主应用（纯Python UI）
├── run.py                  # PyCharm启动脚本
├── requirements.txt        # Python依赖
├── backend/                # 后端模块
│   ├── wave_detector.py   # 波浪检测引擎
│   ├── database.py        # 数据库层
│   └── config.py          # 配置文件
└── PYTHON_GUIDE.md        # Python版本详细指南
```

## 技术栈 (纯Python)

- **Streamlit**: Python Web应用框架，替代React前端
- **OpenCV**: 图像处理和波浪检测
- **NumPy/SciPy**: 科学计算和信号处理
- **SQLite**: 数据库
- **Pandas**: 数据处理和导出
- **Werkzeug**: 密码加密

## 快速启动 (纯Python版本)

### 方法1: 在PyCharm中运行 (推荐) ⭐

#### 步骤1: 安装依赖
```bash
pip install -r requirements.txt
```

#### 步骤2: 运行应用
**选项A: 使用启动脚本**
```bash
python run.py
```

**选项B: 直接运行Streamlit**
```bash
streamlit run app.py
```

**选项C: 在PyCharm中一键运行**
1. 在PyCharm中打开 `run.py` 文件
2. 点击右上角的绿色"运行"按钮 ▶️
3. 或者按快捷键 `Shift+F10`

应用将在浏览器中自动打开: http://localhost:8501

### 方法2: 命令行运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python run.py
```

> 提示: 直接运行 `python app.py` 也会通过 Streamlit 启动，默认地址 http://localhost:8501，可用 `--server.port`/`--server.address` 或环境变量 `STREAMLIT_SERVER_PORT`/`STREAMLIT_SERVER_ADDRESS` 自定义。

---

### 旧版本 (Flask + React)

如果你需要使用旧版本的Flask REST API + React前端架构，请查看以下文档：

<details>
<summary>点击展开旧版本运行方式</summary>

### Docker部署

```bash
# 启动整个系统
docker-compose up -d

# 访问系统
# 前端: http://localhost:3000
# 后端API: http://localhost:5000
```

### 手动部署

#### 后端设置

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 运行服务器
python app.py
```

后端将在 http://localhost:5000 运行

#### 前端设置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端将在 http://localhost:3000 运行

</details>

## 使用指南 (纯Python版本)

### 1. 启动应用

```bash
# 方式1: 使用启动脚本
python run.py

# 方式2: 直接运行Streamlit
streamlit run app.py

# 方式3: 在PyCharm中打开run.py，点击运行按钮
```

### 2. 用户注册/登录
- 访问 http://localhost:8501
- 点击"注册 (Register)"标签创建新账户
- 或使用已有账户在"登录 (Login)"标签登录

### 3. 波浪检测
- 登录后，在主页面上传图像文件
- 在左侧边栏选择检测算法:
  - **Edge Detection**: 适合清晰边界的波浪
  - **Frequency Analysis**: 适合周期性波浪模式
  - **Optical Flow**: 适合运动波浪检测
  - **AI Detection**: 智能识别复杂波浪模式
- 调整灵敏度参数（0.0-1.0）
- 点击"开始检测 (Start Detection)"开始分析

### 4. 查看结果
- 波浪数量统计
- 平均振幅和频率
- 置信度评分
- 波浪详情表格
- 波浪特征图表

### 5. 历史记录
- 切换到"检测历史 (Detection History)"页面
- 查看所有历史检测记录
- 导出数据为CSV或JSON格式

## 检测算法说明

### 1. Edge Detection (边缘检测)
- **原理**: 使用Canny算法检测图像边缘，识别波浪边界
- **适用场景**: 清晰的波浪轮廓，高对比度图像
- **优点**: 快速，准确度高
- **参数**: sensitivity控制边缘检测阈值

### 2. Frequency Analysis (频率分析)
- **原理**: FFT频域分析，识别周期性波浪模式
- **适用场景**: 规律的波浪图案，周期性结构
- **优点**: 能识别频率特征，适合分析波动规律
- **参数**: sensitivity控制峰值检测阈值

### 3. Optical Flow (光流法)
- **原理**: 计算光流场，检测运动波浪
- **适用场景**: 动态波浪，视频帧分析
- **优点**: 能捕捉运动信息
- **参数**: sensitivity控制运动阈值

### 4. AI Detection (AI检测)
- **原理**: 深度学习模型，智能识别复杂波浪模式
- **适用场景**: 复杂场景，多种波浪类型
- **优点**: 适应性强，准确度高
- **参数**: sensitivity控制置信度阈值

## PyCharm配置说明

### 创建运行配置

1. 打开 **Run → Edit Configurations...**
2. 点击 **+** → **Python**
3. 配置如下:
   - **Name**: Wave Detection System
   - **Script path**: 选择 `run.py` 文件的完整路径
   - **Python interpreter**: 选择项目的Python解释器
   - **Working directory**: 项目根目录
4. 点击 **OK** 保存

现在你可以直接点击运行按钮启动应用！

## 系统要求

- **Python版本**: 3.8 或更高
- **操作系统**: Windows, macOS, Linux
- **内存**: 最低2GB RAM
- **IDE**: PyCharm (推荐), VS Code, 或任何Python IDE

## 详细文档

📖 **查看完整Python使用指南**: [PYTHON_GUIDE.md](PYTHON_GUIDE.md)

包含以下内容:
- PyCharm详细配置步骤
- 功能使用说明
- 故障排除
- 开发指南
- 常见问题解答

## 贡献指南

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交Issue。
