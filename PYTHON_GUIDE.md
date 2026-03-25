# 纯Python版本 - PyCharm运行指南

## 系统简介

这是一个**纯Python实现**的波浪检测系统，使用Streamlit框架构建Web界面。
无需Node.js、npm或Docker，可以直接在PyCharm中运行！

## 技术栈

- **Streamlit**: Python Web应用框架
- **OpenCV**: 图像处理和波浪检测
- **NumPy/SciPy**: 科学计算和信号处理
- **SQLite**: 数据库
- **Pandas**: 数据处理和导出
- **Pillow**: 图像处理

## 快速开始

### 方法1: 在PyCharm中运行 (推荐)

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

**选项C: 在PyCharm中直接运行**
1. 在PyCharm中打开 `run.py` 文件
2. 点击右上角的绿色"运行"按钮 ▶️
3. 或者按快捷键 `Shift+F10`

#### 步骤3: 访问应用

应用启动后，浏览器会自动打开：
- 地址: http://localhost:8501

### 方法2: 命令行运行

```bash
# 确保在项目根目录
cd /path/to/wave

# 安装依赖
pip install -r requirements.txt

# 运行应用
python run.py
```

## PyCharm配置

### 创建运行配置

1. 打开 **Run → Edit Configurations...**
2. 点击 **+** → **Python**
3. 配置如下:
   - **Name**: Wave Detection System
   - **Script path**: `/path/to/wave/run.py`
   - **Python interpreter**: 选择项目的Python解释器
   - **Working directory**: `/path/to/wave`
4. 点击 **OK** 保存

现在你可以直接点击运行按钮启动应用！

## 使用指南

### 1. 用户注册/登录

首次使用需要注册账户：
1. 启动应用后，进入"注册 (Register)"标签
2. 填写用户名、邮箱和密码
3. 点击"注册"按钮
4. 返回"登录 (Login)"标签
5. 输入用户名和密码登录

### 2. 波浪检测

登录后进入检测页面：
1. 点击"Browse files"上传图像文件（支持JPG, PNG格式）
2. 在左侧边栏选择检测算法:
   - **边缘检测**: 适合清晰边界的波浪
   - **频率分析**: 适合周期性波浪模式
   - **光流法**: 适合运动波浪检测
   - **AI检测**: 智能识别复杂波浪模式
3. 调整灵敏度参数（0.0-1.0）
4. 点击"开始检测 (Start Detection)"按钮
5. 查看右侧的检测结果

### 3. 查看结果

检测完成后，右侧会显示：
- **波浪数量**: 检测到的波浪总数
- **平均振幅**: 波浪的平均高度
- **平均频率**: 波浪的平均频率
- **置信度**: 检测结果的可信度
- **波浪详情表格**: 每个波浪的详细信息
- **波浪特征图表**: 可视化波浪特征

### 4. 历史记录

切换到"检测历史"页面：
1. 查看所有历史检测记录
2. 查看统计摘要（总检测次数、总波浪数等）
3. 导出数据为CSV或JSON格式

### 5. 算法说明

在"算法说明"页面查看四种检测算法的详细介绍。

## 项目结构

```
wave/
├── app.py                  # Streamlit主应用程序（纯Python）
├── run.py                  # 启动脚本
├── requirements.txt        # Python依赖
├── backend/                # 后端模块
│   ├── wave_detector.py   # 波浪检测引擎
│   ├── database.py        # 数据库层
│   └── config.py          # 配置文件
└── PYTHON_GUIDE.md        # 本文档
```

## 功能特性

### 核心功能
- ✅ **纯Python实现**: 无需JavaScript、Node.js或npm
- ✅ **PyCharm直接运行**: 一键启动，无需额外配置
- ✅ **多算法支持**: 4种不同的检测算法
- ✅ **用户认证**: 安全的登录注册系统
- ✅ **实时检测**: 上传图像即时分析
- ✅ **可视化展示**: 交互式图表和数据表格
- ✅ **历史记录**: 完整的检测历史管理
- ✅ **数据导出**: CSV/JSON格式导出

### 与之前版本的对比

| 特性 | 旧版本 (Flask+React) | 新版本 (Streamlit) |
|------|---------------------|-------------------|
| 前端 | React (JavaScript) | Streamlit (Python) |
| 后端 | Flask REST API | 集成在Streamlit中 |
| 启动方式 | Docker Compose | 单个Python脚本 |
| 依赖 | Python + Node.js | 仅Python |
| PyCharm运行 | ❌ 需要多步骤 | ✅ 一键运行 |

## 常见问题

### Q: 如何在PyCharm中调试？

A: 在PyCharm中:
1. 在代码中设置断点
2. 右键点击 `run.py` → **Debug 'run'**
3. 应用会在调试模式下启动

### Q: 如何修改端口号？

A: 编辑 `run.py` 文件，修改 `--server.port` 参数：
```python
'--server.port', '8501',  # 改为你想要的端口
```

### Q: 数据库文件在哪里？

A: SQLite数据库文件 `wave_detection.db` 会在项目根目录自动创建。

### Q: 如何重置数据库？

A: 删除 `wave_detection.db` 文件，下次运行时会自动重新创建：
```bash
rm wave_detection.db
```

### Q: 能否在没有浏览器的环境中运行？

A: Streamlit需要浏览器访问。如果你需要纯命令行版本，可以使用后端的测试脚本：
```bash
cd backend
python test_api.py  # 这会启动Flask API服务器
```

## 开发指南

### 添加新功能

所有功能都在 `app.py` 中实现，使用Streamlit的组件：

```python
def my_new_page():
    st.title("我的新功能")
    st.write("这是新功能的内容")

# 在main()函数中添加导航项
```

### 修改检测算法

检测算法在 `backend/wave_detector.py` 中实现。参考现有算法添加新算法：

```python
def _my_algorithm(self, image: np.ndarray, sensitivity: float = 0.5, **kwargs) -> Dict:
    # 你的算法实现
    return {
        'wave_count': wave_count,
        'avg_amplitude': avg_amplitude,
        'avg_frequency': avg_frequency,
        'confidence_score': confidence,
        'waves': waves
    }

# 在__init__中注册
self.algorithms['my_algorithm'] = self._my_algorithm
```

## 性能优化建议

1. **大图像处理**: 对于大型图像，考虑在检测前先缩放
2. **批量检测**: 使用Streamlit的缓存功能 `@st.cache_data`
3. **数据库优化**: 对于大量历史记录，添加索引

## 故障排除

### 安装依赖失败

```bash
# 升级pip
pip install --upgrade pip

# 使用国内镜像源（如果在中国）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### OpenCV导入错误

```bash
# 卸载并重新安装
pip uninstall opencv-python
pip install opencv-python==4.9.0.80
```

### Streamlit端口被占用

修改 `run.py` 中的端口号，或使用命令行参数：
```bash
streamlit run app.py --server.port 8502
```

## 系统要求

- **Python版本**: 3.8 或更高
- **操作系统**: Windows, macOS, Linux
- **内存**: 最低2GB RAM
- **IDE**: PyCharm, VS Code, 或任何Python IDE

## 许可证

MIT License

## 技术支持

如有问题，请查看:
1. Streamlit官方文档: https://docs.streamlit.io
2. OpenCV文档: https://docs.opencv.org
3. 项目Issues页面

---

**享受纯Python开发的便利！🎉**
