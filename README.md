# Visual Wave Detection System

一个基于计算机视觉的波浪检测系统，提供多种检测算法和实时分析功能。

## 系统特性

### 核心功能
- **多算法支持**: 边缘检测、频率分析、光流法、AI检测
- **用户认证**: 安全的登录注册系统，JWT token认证
- **实时检测**: 支持图像上传和实时波浪检测
- **可视化分析**: 交互式图表和波浪标注
- **历史记录**: 保存所有检测历史，支持导出
- **数据导出**: CSV/JSON格式导出检测结果

### 创新特性
1. **多算法融合**: 四种不同的检测算法适应不同场景
   - 边缘检测: 基于Canny算法的经典边缘检测
   - 频率分析: FFT频域分析识别波浪模式
   - 光流法: 基于运动的波浪检测
   - AI检测: 深度学习模型智能识别

2. **智能参数调节**: 可调节灵敏度适应不同环境
3. **实时可视化**: 波浪边界标注和统计图表
4. **数据持久化**: 完整的用户数据和检测历史管理

## 系统架构

```
wave-detection-system/
├── backend/                # Python Flask后端
│   ├── app.py             # 主应用程序
│   ├── database.py        # 数据库层
│   ├── wave_detector.py   # 波浪检测引擎
│   ├── config.py          # 配置文件
│   └── requirements.txt   # Python依赖
├── frontend/              # React前端
│   ├── src/
│   │   ├── components/    # React组件
│   │   │   ├── Login.jsx          # 登录界面
│   │   │   ├── Dashboard.jsx      # 主仪表板
│   │   │   ├── WaveVisualizer.jsx # 波浪可视化
│   │   │   └── DetectionHistory.jsx # 历史记录
│   │   ├── App.jsx        # 主应用
│   │   └── main.jsx       # 入口文件
│   ├── package.json       # Node.js依赖
│   └── vite.config.js     # Vite配置
└── docker-compose.yml     # Docker部署配置
```

## 技术栈

### 后端
- **Flask**: Web框架
- **OpenCV**: 图像处理和波浪检测
- **NumPy/SciPy**: 科学计算和信号处理
- **SQLite**: 数据库
- **JWT**: 用户认证

### 前端
- **React**: UI框架
- **Chart.js**: 数据可视化
- **Axios**: HTTP客户端
- **Vite**: 构建工具

## 快速启动

### 方法1: Docker部署 (推荐)

```bash
# 启动整个系统
docker-compose up -d

# 访问系统
# 前端: http://localhost:3000
# 后端API: http://localhost:5000
```

### 方法2: 手动部署

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

## 使用指南

### 1. 用户注册/登录
- 访问系统首页
- 点击"Register"创建新账户
- 或使用已有账户登录

### 2. 波浪检测
- 在Dashboard中点击上传区域或拖拽图像文件
- 选择检测算法:
  - **Edge Detection**: 适合清晰边界的波浪
  - **Frequency Analysis**: 适合周期性波浪模式
  - **Optical Flow**: 适合运动波浪检测
  - **AI Detection**: 智能识别复杂波浪模式
- 调整灵敏度参数（0-100%）
- 点击"Start Detection"开始分析

### 3. 查看结果
- 波浪数量统计
- 平均振幅和频率
- 置信度评分
- 可视化标注图像
- 波浪特征图表

### 4. 历史记录
- 切换到"Detection History"标签
- 查看所有历史检测记录
- 导出数据为CSV格式

## API文档

### 认证接口

#### POST /api/auth/register
注册新用户
```json
{
  "username": "user123",
  "password": "password",
  "email": "user@example.com"
}
```

#### POST /api/auth/login
用户登录
```json
{
  "username": "user123",
  "password": "password"
}
```

返回:
```json
{
  "access_token": "jwt_token",
  "user": {
    "id": 1,
    "username": "user123",
    "email": "user@example.com"
  }
}
```

### 检测接口

#### POST /api/detect/upload
上传图像进行检测 (需要认证)

参数:
- `file`: 图像文件
- `algorithm`: 算法类型 (edge_detection, frequency_analysis, optical_flow, ai_detection)
- `sensitivity`: 灵敏度 (0.0-1.0)

#### GET /api/detections/history
获取检测历史 (需要认证)

查询参数:
- `page`: 页码
- `per_page`: 每页数量

#### GET /api/algorithms
获取可用算法列表 (需要认证)

#### GET /api/stats/summary
获取用户统计信息 (需要认证)

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

## 环境变量配置

创建 `.env` 文件配置系统参数:

```env
# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key

# Database
DATABASE_PATH=wave_detection.db

# Upload
UPLOAD_FOLDER=uploads

# AI Model
AI_MODEL_PATH=models/wave_detection_model.pth
```

## 开发指南

### 添加新的检测算法

1. 在 `backend/wave_detector.py` 中添加新方法:
```python
def _new_algorithm(self, image: np.ndarray, **kwargs) -> Dict:
    # Your algorithm implementation
    return {
        'wave_count': wave_count,
        'avg_amplitude': avg_amplitude,
        'avg_frequency': avg_frequency,
        'confidence_score': confidence,
        'waves': waves
    }
```

2. 在 `algorithms` 字典中注册:
```python
self.algorithms['new_algorithm'] = self._new_algorithm
```

3. 在API中添加算法描述 (app.py)

### 扩展前端功能

前端组件位于 `frontend/src/components/`:
- 修改 `Dashboard.jsx` 添加新功能面板
- 修改 `WaveVisualizer.jsx` 添加新的可视化方式
- 添加新组件到 `components/` 目录

## 安全性

- 密码使用bcrypt哈希存储
- JWT token认证保护API
- 文件上传大小限制(50MB)
- SQL注入防护
- XSS防护

## 性能优化

- 图像处理使用OpenCV优化
- 数据库索引优化查询
- 前端懒加载和代码分割
- 分页减少数据传输

## 测试

```bash
# 后端测试
cd backend
pytest tests/

# 前端测试
cd frontend
npm test
```

## 贡献指南

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交Issue。
