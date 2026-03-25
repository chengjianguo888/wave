# 如何在PyCharm中运行 (中文指南)

## 📖 简介

这是一个**纯Python实现**的波浪检测系统。现在你可以直接在PyCharm中运行，无需安装Node.js、npm或Docker！

## 🎯 快速开始（3步）

### 步骤1: 安装依赖

打开PyCharm的Terminal（终端），运行：

```bash
pip install -r requirements.txt
```

**提示**: 如果安装速度慢，使用清华大学镜像源：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 步骤2: 运行应用

在PyCharm中有3种方式运行：

#### 方式A: 使用运行按钮（最简单）
1. 在项目浏览器中找到 `run.py` 文件
2. 右键点击文件
3. 选择 "Run 'run'" 或直接点击右上角的绿色运行按钮 ▶️
4. 或按快捷键 `Shift+F10`

#### 方式B: 使用Terminal
在PyCharm的Terminal中运行：
```bash
python run.py
```

#### 方式C: 直接运行Streamlit
```bash
streamlit run app.py
```

### 步骤3: 访问应用

应用启动后，浏览器会自动打开：
- 地址: **http://localhost:8501**

## 🎨 主要功能

### 1. 用户注册和登录
- 首次使用需要注册账户
- 填写用户名、邮箱和密码
- 注册后可以登录使用

### 2. 波浪检测
- 上传图像文件（JPG, PNG格式）
- 选择4种检测算法之一：
  1. **边缘检测** - 快速、准确，适合清晰边界
  2. **频率分析** - 适合周期性波浪
  3. **光流法** - 适合运动波浪
  4. **AI检测** - 智能识别复杂模式
- 调整灵敏度参数（0.0-1.0）
- 查看检测结果

### 3. 查看结果
检测完成后显示：
- 📊 波浪数量
- 📏 平均振幅
- 📈 平均频率
- 🎯 置信度评分
- 📋 详细数据表格
- 📉 特征图表

### 4. 历史记录
- 查看所有检测历史
- 查看统计摘要
- 导出数据为CSV或JSON格式

## 🔧 PyCharm配置（可选）

如果你想创建专门的运行配置：

### 创建自定义运行配置

1. 点击 **Run → Edit Configurations...**
2. 点击左上角的 **+** 按钮
3. 选择 **Python**
4. 填写配置：
   - **Name**: 波浪检测系统
   - **Script path**: 点击文件夹图标，选择项目中的 `run.py`
   - **Python interpreter**: 确保选择了正确的Python解释器
   - **Working directory**: 应该自动设置为项目根目录
5. 点击 **OK** 保存

现在你可以在运行配置下拉菜单中选择"波浪检测系统"并运行！

## 📂 项目结构

```
wave/
├── app.py                  # Streamlit主应用（纯Python UI）
├── run.py                  # 启动脚本
├── requirements.txt        # Python依赖
├── backend/                # 后端模块
│   ├── wave_detector.py   # 波浪检测引擎
│   ├── database.py        # 数据库层
│   ├── config.py          # 配置文件
│   └── tests/             # 测试文件
├── PYTHON_GUIDE.md        # 详细Python指南
├── QUICKSTART.md          # 快速开始指南
└── README.md              # 完整说明文档
```

## 💡 使用技巧

### 调试应用
在PyCharm中调试：
1. 在代码中设置断点（点击行号旁边）
2. 右键点击 `run.py`
3. 选择 "Debug 'run'"
4. 应用会在调试模式下启动

### 修改端口
如果8501端口被占用，编辑 `run.py`：
```python
'--server.port', '8502',  # 改为你需要的端口
```

### 查看日志
Streamlit会在Terminal中显示所有日志信息。

## ⚠️ 常见问题

### Q1: 安装依赖时出错
```bash
# 升级pip
pip install --upgrade pip

# 重新安装
pip install -r requirements.txt
```

### Q2: OpenCV安装失败
```bash
# 卸载重装
pip uninstall opencv-python
pip install opencv-python==4.9.0.80
```

### Q3: 应用启动后浏览器没有自动打开
手动在浏览器中访问: http://localhost:8501

### Q4: 数据库错误
删除数据库文件重新创建：
```bash
rm wave_detection.db
python run.py
```

### Q5: 导入模块错误
确保在项目根目录运行：
```bash
cd /path/to/wave
python run.py
```

## 🎓 技术说明

### 为什么选择Streamlit？
- ✅ 纯Python实现，无需JavaScript
- ✅ 快速开发Web界面
- ✅ 内置组件丰富（文件上传、图表、表格等）
- ✅ 自动刷新和状态管理
- ✅ 易于调试和维护

### 主要技术栈
- **Streamlit 1.31.0** - Web应用框架
- **OpenCV 4.9.0** - 图像处理
- **NumPy 1.26.3** - 数值计算
- **SciPy 1.12.0** - 科学计算
- **Pandas 2.2.0** - 数据处理
- **Pillow 10.2.0** - 图像库

## 📖 更多文档

- **完整指南**: [PYTHON_GUIDE.md](PYTHON_GUIDE.md)
- **快速开始**: [QUICKSTART.md](QUICKSTART.md)
- **系统架构**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **功能说明**: [FEATURES.md](FEATURES.md)

## 🆘 获取帮助

如果遇到问题：
1. 查看本文档的常见问题部分
2. 查看 [PYTHON_GUIDE.md](PYTHON_GUIDE.md) 的故障排除章节
3. 提交Issue到GitHub

---

**祝你使用愉快！如有问题随时联系！🌊**
