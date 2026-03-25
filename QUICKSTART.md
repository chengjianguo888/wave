# Visual Wave Detection System - Quick Start Guide

## 系统概述
视觉波浪检测系统是一个基于计算机视觉技术的Web应用，能够自动检测和分析图像中的波浪模式。

## 快速安装

### 使用Docker (推荐)
```bash
# 克隆仓库
git clone <repository-url>
cd wave

# 启动系统
docker-compose up -d

# 访问应用
# 前端: http://localhost:3000
# 后端: http://localhost:5000
```

### 手动安装

#### 1. 安装后端
```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量 (可选)
cp .env.example .env
# 编辑 .env 文件设置密钥

# 启动服务器
python app.py
```

#### 2. 安装前端
```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

#### 3. 使用启动脚本（Linux/Mac）
```bash
chmod +x start.sh
./start.sh
```

## 首次使用

1. **访问系统**: 打开浏览器访问 http://localhost:3000

2. **注册账户**:
   - 点击"Register"
   - 输入用户名、邮箱和密码
   - 点击注册按钮

3. **登录系统**:
   - 使用刚注册的账户登录
   - 进入主Dashboard

4. **开始检测**:
   - 点击上传区域或拖拽图像文件
   - 选择检测算法
   - 调整灵敏度
   - 点击"Start Detection"

5. **查看结果**:
   - 查看检测统计
   - 浏览可视化结果
   - 查看历史记录

## 示例数据

生成示例波浪图像用于测试:
```bash
cd backend
python generate_samples.py
```

这将在 `backend/samples/` 目录生成三种类型的示例图像:
- sine_wave.png: 正弦波图像
- ocean_wave.png: 海浪图像
- ripple_wave.png: 涟漪图像

## 测试系统

### 后端测试
```bash
cd backend
pip install -r tests/requirements.txt
pytest tests/
```

### API测试
```bash
cd backend
# 确保服务器正在运行
python test_api.py
```

## 常见问题解决

### 端口已被占用
如果5000或3000端口被占用:
- 修改 docker-compose.yml 中的端口映射
- 或在本地运行时指定不同端口

### 依赖安装失败
**后端**:
```bash
# 升级pip
pip install --upgrade pip

# 如果OpenCV安装失败
pip install opencv-python-headless
```

**前端**:
```bash
# 清除缓存
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### 数据库初始化
数据库会在首次启动时自动创建。如需重置:
```bash
rm backend/wave_detection.db
# 重启后端服务器
```

## 下一步

- 查看完整文档: `docs/USER_GUIDE.md`
- 了解技术细节: `docs/TECHNICAL_DOCS.md`
- 查看API文档: README.md中的API部分

## 获取帮助

- 查看文档目录
- 提交Issue
- 查看示例代码

祝使用愉快！
