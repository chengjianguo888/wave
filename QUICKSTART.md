# 快速开始指南 (纯Python版本)

## 🚀 3步快速启动

### 第一步: 安装Python依赖

```bash
pip install -r requirements.txt
```

如果安装速度慢，可以使用国内镜像源：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 第二步: 运行应用

**方式1: 使用启动脚本 (推荐)**
```bash
python run.py
```

**方式2: 直接运行Streamlit**
```bash
streamlit run app.py
```

**方式3: 在PyCharm中运行**
1. 用PyCharm打开项目
2. 打开 `run.py` 文件
3. 点击右上角的绿色运行按钮 ▶️
4. 或按快捷键 `Shift+F10`

### 第三步: 访问应用

浏览器会自动打开: **http://localhost:8501**

---

## 💡 首次使用

### 1. 注册账户
- 点击"注册 (Register)"标签
- 填写用户名、邮箱和密码
- 点击"注册 (Register)"按钮

### 2. 登录系统
- 切换到"登录 (Login)"标签
- 输入用户名和密码
- 点击"登录 (Login)"按钮

### 3. 开始检测波浪
- 点击"Browse files"上传图像（支持JPG, PNG）
- 在左侧边栏选择检测算法:
  - 边缘检测 (Edge Detection)
  - 频率分析 (Frequency Analysis)
  - 光流法 (Optical Flow)
  - AI检测 (AI Detection)
- 调整灵敏度参数（0.0-1.0）
- 点击"开始检测 (Start Detection)"按钮

### 4. 查看结果
检测完成后会显示：
- 波浪数量
- 平均振幅
- 平均频率
- 置信度评分
- 波浪详情表格
- 特征图表

---

## 📋 核心功能

- ✅ **纯Python实现** - 无需Node.js或Docker
- ✅ **PyCharm直接运行** - 一键启动
- ✅ **用户认证系统** - 安全的注册登录
- ✅ **4种检测算法** - 适应不同场景
- ✅ **实时波浪检测** - 上传即分析
- ✅ **可视化展示** - 图表和数据表格
- ✅ **历史记录管理** - 完整的检测历史
- ✅ **数据导出** - CSV/JSON格式

---

## ⚙️ 系统要求

- **Python版本**: 3.8 或更高
- **操作系统**: Windows, macOS, Linux
- **内存**: 最低2GB RAM (推荐4GB)
- **IDE**: PyCharm (推荐), VS Code, 或任何Python IDE

---

## 🔧 常见问题

### 问题1: 依赖安装失败

```bash
# 升级pip
pip install --upgrade pip

# 重新安装
pip install -r requirements.txt
```

### 问题2: 端口8501被占用

修改 `run.py` 文件中的端口号:
```python
'--server.port', '8502',  # 改为其他可用端口
```

或在命令行指定:
```bash
streamlit run app.py --server.port 8502
```

### 问题3: OpenCV导入错误

```bash
pip uninstall opencv-python
pip install opencv-python==4.9.0.80
```

### 问题4: 数据库错误

删除并重新创建数据库:
```bash
rm wave_detection.db
python run.py  # 会自动创建新数据库
```

---

## 📚 更多信息

- **完整Python指南**: [PYTHON_GUIDE.md](PYTHON_GUIDE.md)
- **详细README**: [README.md](README.md)
- **系统架构**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **功能列表**: [FEATURES.md](FEATURES.md)

---

## 🎯 与旧版本对比

| 特性 | 旧版本 | 新版本 (纯Python) |
|------|--------|------------------|
| 前端 | React + JavaScript | Streamlit (Python) |
| 后端 | Flask REST API | 集成在Streamlit |
| 启动 | Docker/多步骤 | 单个命令 |
| 依赖 | Python + Node.js | 仅Python |
| PyCharm | ❌ 复杂配置 | ✅ 一键运行 |

---

**享受纯Python开发的便利！🌊**
