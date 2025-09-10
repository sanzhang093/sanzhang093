# 🧲 AI竞争对手智能分析代理团队

一个基于多AI模型融合的智能竞争对手分析平台，通过自动化数据收集、深度分析和可视化展示，为企业提供全面的竞争情报分析服务。

## ✨ 项目特色

- **🤖 多模型支持**: 集成OpenAI GPT-4和阿里云通义千问，提供灵活的AI分析能力
- **🔍 智能搜索引擎**: 支持Perplexity AI和Exa AI，精准发现竞争对手
- **🕷️ 专业数据爬取**: 使用Firecrawl提取高质量结构化数据
- **📊 可视化分析**: 生成交互式对比表格和详细分析报告
- **🛡️ 容错机制**: 完善的错误处理和备用分析方案

## 🚀 核心功能

### 1. 智能竞争对手发现
- 通过URL或公司描述自动识别竞争对手
- 支持多种搜索引擎策略
- 智能去重和结果优化

### 2. 深度数据提取
- 自动提取公司基本信息
- 分析定价策略和产品功能
- 识别技术栈和营销重点
- 收集客户反馈和评价

### 3. 多维度分析报告
- **市场定位分析**: 分析各竞争对手的市场定位和差异化策略
- **产品功能对比**: 对比核心功能和特性
- **定价策略分析**: 分析定价模式和策略
- **技术栈对比**: 分析使用的技术和工具
- **营销策略分析**: 分析目标受众和营销重点
- **竞争优势识别**: 识别独特优势
- **市场机会发现**: 发现市场空白和机会
- **战略建议**: 提供具体的竞争策略建议

### 4. 可视化展示
- 交互式对比表格
- 详细数据展示
- 原始JSON数据查看
- 响应式设计

## 🛠️ 技术栈

### 前端框架
- **Streamlit**: 快速构建交互式Web应用
- **Pandas**: 数据处理和分析
- **自定义CSS**: 美观的界面设计

### AI模型集成
- **OpenAI GPT-4**: 通过Agno框架集成
- **阿里云通义千问**: 支持多种模型选择
- **智能提示工程**: 优化的分析提示词

### 数据获取
- **Firecrawl**: 专业网站爬取和数据提取
- **Perplexity AI**: 智能搜索引擎
- **Exa AI**: 神经网络搜索
- **Pydantic**: 数据验证和结构化

### 数据处理
- **JSON**: 结构化数据存储
- **Requests**: HTTP请求处理
- **错误处理**: 完善的异常处理机制

## 📦 安装指南

### 1. 环境要求
- Python 3.8+
- 稳定的网络连接
- 有效的API密钥

### 2. 安装依赖

```bash
# 基础依赖
pip install streamlit pandas requests pydantic

# OpenAI 支持（可选）
pip install agno

# Qwen 支持（可选）
pip install -U "qwen-agent[gui,rag,code_interpreter,mcp]"

# 网站爬取支持
pip install firecrawl-py

# 搜索引擎支持（可选）
pip install exa-py
```

### 3. 获取API密钥

#### 必需API
- **Firecrawl API**: [获取密钥](https://www.firecrawl.dev/app/api-keys)

#### 可选API
- **OpenAI API**: [获取密钥](https://platform.openai.com/api-keys)
- **DashScope API**: [获取密钥](https://dashscope.console.aliyun.com/)
- **Perplexity API**: [获取密钥](https://www.perplexity.ai/settings/api)
- **Exa API**: [获取密钥](https://dashboard.exa.ai/api-keys)

### 4. API密钥安全管理

**⚠️ 重要安全提示：**

- **请勿将API密钥硬编码在代码中**
- **不要将包含API密钥的文件提交到版本控制系统**
- **建议使用环境变量或配置文件管理API密钥**
- **定期轮换API密钥以确保安全**

#### 推荐的安全做法：

1. **使用配置文件**：
   ```bash
   # 复制示例配置文件
   cp config.example.py config.py
   # 编辑 config.py 并填入您的API密钥
   ```

2. **使用环境变量**：
   ```bash
   export OPENAI_API_KEY="your-api-key"
   export DASHSCOPE_API_KEY="your-api-key"
   export FIRECRAWL_API_KEY="your-api-key"
   ```

3. **使用 .env 文件**：
   ```bash
   # 创建 .env 文件
   echo "OPENAI_API_KEY=your-api-key" > .env
   echo "DASHSCOPE_API_KEY=your-api-key" >> .env
   echo "FIRECRAWL_API_KEY=your-api-key" >> .env
   ```

## 🎯 使用方法

### 1. 启动应用
```bash
streamlit run competitor_agent_team_combined.py
```

### 2. 配置API密钥
在侧边栏中配置所需的API密钥：
- 选择AI模型提供商（OpenAI或Qwen）
- 选择搜索引擎（Perplexity或Exa）
- 输入Firecrawl API密钥

### 3. 输入分析目标
- **方式一**: 输入公司URL
- **方式二**: 输入公司描述

### 4. 开始分析
点击"🚀 开始分析竞争对手"按钮，系统将：
1. 搜索竞争对手URL
2. 提取竞争对手信息
3. 生成对比表格
4. 生成智能分析报告

## 📊 功能演示

### 输入示例
```
URL: https://example.com
描述: AI驱动的数据分析平台
```

### 输出内容
- **竞争对手列表**: 自动发现的10个竞争对手
- **对比表格**: 包含定价、功能、技术栈等维度
- **详细分析**: 8个维度的深度分析报告
- **战略建议**: 具体的竞争策略建议

## 🔧 配置说明

### AI模型配置
- **OpenAI GPT-4**: 需要OpenAI API密钥
- **Qwen模型**: 支持qwen-max、qwen-plus、qwen-turbo、qwen-long

### 搜索引擎配置
- **Perplexity AI**: 使用Sonar Pro模型
- **Exa AI**: 支持神经网络搜索

### 数据提取配置
- **Firecrawl**: 专业网站爬取
- **结构化提取**: 基于Pydantic模式

## 🎨 界面特色

- **响应式设计**: 适配不同屏幕尺寸
- **美观界面**: 自定义CSS样式
- **交互体验**: 流畅的用户操作
- **实时反馈**: 进度显示和状态提示

## 🛡️ 错误处理

### 容错机制
- **API失败处理**: 自动切换到备用方案
- **数据提取失败**: 提供基础分析报告
- **网络异常**: 智能重试和错误提示

### 备用方案
- **基础分析**: 不依赖AI的分析报告
- **数据展示**: 即使分析失败也能查看原始数据
- **用户提示**: 清晰的错误信息和解决建议

## 📈 应用场景

### 企业应用
- **市场研究**: 快速了解竞争对手情况
- **产品规划**: 制定差异化产品策略
- **定价策略**: 分析市场定价模式
- **营销决策**: 制定有效的营销策略

### 行业适用
- **SaaS服务**: 分析软件服务竞争对手
- **电商平台**: 了解电商竞争格局
- **金融科技**: 分析FinTech竞争对手
- **教育培训**: 研究教育行业竞争

## 🔮 未来规划

### 功能扩展
- [ ] 支持更多AI模型（Claude、Gemini等）
- [ ] 增加实时监控功能
- [ ] 添加数据导出功能
- [ ] 支持批量分析

### 技术优化
- [ ] 提升数据提取准确性
- [ ] 优化分析报告质量
- [ ] 增强用户界面体验
- [ ] 支持多语言分析

### 部署方案
- [ ] Docker容器化部署
- [ ] 云端SaaS服务
- [ ] 企业私有化部署
- [ ] API服务接口

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目：

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

## 📄 许可证

本项目基于MIT许可证开源。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 提交GitHub Issue
- 发送邮件至项目维护者

## 🙏 致谢

感谢以下开源项目和服务：
- [Streamlit](https://streamlit.io/) - Web应用框架
- [OpenAI](https://openai.com/) - AI模型服务
- [阿里云通义千问](https://tongyi.aliyun.com/) - AI模型服务
- [Firecrawl](https://www.firecrawl.dev/) - 网站爬取服务
- [Perplexity AI](https://www.perplexity.ai/) - 搜索引擎服务
- [Exa](https://exa.ai/) - 神经网络搜索服务

---

**⭐ 如果这个项目对你有帮助，请给个Star支持一下！**