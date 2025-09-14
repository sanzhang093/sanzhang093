# -*- coding: utf-8 -*-
"""
AI 竞争对手智能分析代理团队 - 综合版本
功能：结合 OpenAI 和 Qwen 模型，提供多种分析选项
"""

import streamlit as st
import requests
import pandas as pd
import json
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import time

# 尝试导入各种依赖
try:
    from agno.agent import Agent
    from agno.tools.firecrawl import FirecrawlTools
    from agno.models.openai import OpenAIChat
    from agno.tools.duckduckgo import DuckDuckGoTools
    AGNO_AVAILABLE = True
except ImportError:
    AGNO_AVAILABLE = False

try:
    from qwen_agent.agents import Assistant
    from qwen_agent.llm import get_chat_model
    QWEN_AVAILABLE = True
except ImportError:
    QWEN_AVAILABLE = False

try:
    from firecrawl import FirecrawlApp
    FIRECRAWL_AVAILABLE = True
except ImportError:
    FIRECRAWL_AVAILABLE = False

try:
    from exa_py import Exa
    EXA_AVAILABLE = True
except ImportError:
    EXA_AVAILABLE = False

# 配置 Streamlit 页面
st.set_page_config(page_title="AI 竞争对手智能分析代理团队 - 综合版本", layout="wide")

# 添加自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2e8b57;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #2e8b57;
        padding-bottom: 0.5rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .competitor-card {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 主界面标题
st.markdown('<h1 class="main-header">🧲 AI 竞争对手智能分析代理团队</h1>', unsafe_allow_html=True)
st.markdown('<h2 style="text-align: center; color: #666; margin-bottom: 2rem;">综合版本 - 支持多种AI模型</h2>', unsafe_allow_html=True)

# 侧边栏 - 模型和API配置
st.sidebar.title("🔧 配置选项")

# 安全提示
st.sidebar.markdown("""
<div class="warning-box">
    <h4>🔒 安全提示</h4>
    <p><strong>重要：</strong>请勿将API密钥提交到版本控制系统！</p>
    <p>建议使用环境变量或配置文件来管理API密钥。</p>
</div>
""", unsafe_allow_html=True)

# 模型选择
model_provider = st.sidebar.selectbox(
    "选择AI模型提供商",
    options=["OpenAI GPT-4", "Qwen (通义千问)"],
    help="选择用于分析的AI模型"
)

# 根据选择的模型显示相应的配置
if model_provider == "OpenAI GPT-4":
    st.sidebar.subheader("OpenAI 配置")
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password", help="OpenAI API 密钥")
    
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.session_state.model_provider = "openai"
        st.sidebar.success("✅ OpenAI API 已配置")
    else:
        st.sidebar.warning("⚠️ 请输入 OpenAI API Key")
        
else:  # Qwen
    st.sidebar.subheader("Qwen 配置")
    # DashScope API Key
    dashscope_api_key = st.sidebar.text_input("DashScope API Key", type="password", help="阿里云 DashScope API 密钥")
    qwen_model = st.sidebar.selectbox(
        "选择 Qwen 模型",
        options=["qwen-max", "qwen-plus", "qwen-turbo", "qwen-long"],
        help="选择要使用的 Qwen 模型"
    )
    
    if dashscope_api_key:
        st.session_state.dashscope_api_key = dashscope_api_key
        st.session_state.qwen_model = qwen_model
        st.session_state.model_provider = "qwen"
        st.sidebar.success("✅ Qwen API 已配置")
    else:
        st.sidebar.warning("⚠️ 请输入 DashScope API Key")

# 搜索引擎选择
st.sidebar.subheader("🔍 搜索引擎配置")
search_engine = st.sidebar.selectbox(
    "选择搜索引擎",
    options=["Perplexity AI - Sonar Pro", "Exa AI"],
    help="选择用于查找竞争对手的搜索引擎"
)

# 根据选择的搜索引擎显示相应的API密钥输入框
if search_engine == "Perplexity AI - Sonar Pro":
    perplexity_api_key = st.sidebar.text_input("Perplexity API Key", type="password", help="Perplexity API 密钥")
    if perplexity_api_key:
        st.session_state.perplexity_api_key = perplexity_api_key
        st.session_state.search_engine = "perplexity"
        st.sidebar.success("✅ Perplexity API 已配置")
    else:
        st.sidebar.warning("⚠️ 请输入 Perplexity API Key")
else:  # Exa AI
    # Exa API Key
    exa_api_key = st.sidebar.text_input("Exa API Key", type="password", help="Exa API 密钥")
    if exa_api_key:
        st.session_state.exa_api_key = exa_api_key
        st.session_state.search_engine = "exa"
        st.sidebar.success("✅ Exa API 已配置")
    else:
        st.sidebar.warning("⚠️ 请输入 Exa API Key")

# Firecrawl 配置
st.sidebar.subheader("🕷️ 网站爬取配置")
# Firecrawl API Key
firecrawl_api_key = st.sidebar.text_input("Firecrawl API Key", type="password", help="Firecrawl API 密钥")
if firecrawl_api_key:
    st.session_state.firecrawl_api_key = firecrawl_api_key
    st.sidebar.success("✅ Firecrawl API 已配置")
else:
    st.sidebar.warning("⚠️ 请输入 Firecrawl API Key")

# 功能说明
st.markdown("""
<div class="info-box">
    <h4>🚀 功能特点</h4>
    <ul>
        <li><strong>多模型支持</strong>: 支持 OpenAI GPT-4 和 Qwen (通义千问)</li>
        <li><strong>智能搜索引擎</strong>: 支持 Perplexity AI 和 Exa AI</li>
        <li><strong>专业爬取</strong>: 使用 Firecrawl 提取高质量网站数据</li>
        <li><strong>深度分析</strong>: 生成详细的分析报告和对比表格</li>
        <li><strong>错误处理</strong>: 智能错误处理和备用方案</li>
    </ul>
    <p><strong>使用方法：</strong> 配置API密钥后，提供您公司的 <strong>URL</strong> 或 <strong>描述</strong>，系统将自动分析竞争对手。</p>
</div>
""", unsafe_allow_html=True)

# 用户输入区域
st.subheader("📝 输入信息")
col1, col2 = st.columns(2)
with col1:
    url = st.text_input("输入您的公司 URL：", placeholder="https://example.com")
with col2:
    description = st.text_area("输入您公司的描述（如果 URL 不可用）：", placeholder="例如：AI驱动的数据分析平台")

# 竞争对手数据模式定义
class CompetitorDataSchema(BaseModel):
    """竞争对手数据模式"""
    company_name: str = Field(description="公司名称")
    pricing: str = Field(description="定价详情、层级和计划")
    key_features: List[str] = Field(description="产品/服务的主要功能和能力")
    tech_stack: List[str] = Field(description="使用的技术、框架和工具")
    marketing_focus: str = Field(description="主要营销角度和目标受众")
    customer_feedback: str = Field(description="客户推荐、评论和反馈")

# OpenAI 分析器
class OpenAIAnalyzer:
    """使用 OpenAI 的竞争对手分析器"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        if AGNO_AVAILABLE:
            self.analysis_agent = Agent(
                model=OpenAIChat(id="gpt-4o", api_key=api_key),
                show_tool_calls=True,
                markdown=True
            )
        else:
            self.analysis_agent = None
    
    def analyze_competitors(self, competitor_data: List[Dict]) -> str:
        """分析竞争对手数据"""
        if not self.analysis_agent:
            return "OpenAI Agent 未正确初始化，请检查 agno 库是否正确安装"
        
        # 格式化数据
        formatted_data = json.dumps(competitor_data, indent=2, ensure_ascii=False)
        
        # 构建分析提示
        analysis_prompt = f"""
        请分析以下竞争对手数据，并提供详细的竞争分析报告：

        {formatted_data}

        请从以下角度进行分析：
        1. 市场定位分析 - 分析各竞争对手的市场定位和差异化策略
        2. 产品功能对比 - 对比各竞争对手的核心功能和特性
        3. 定价策略分析 - 分析定价模式和策略
        4. 技术栈对比 - 分析各竞争对手使用的技术
        5. 营销策略分析 - 分析目标受众和营销重点
        6. 竞争优势识别 - 识别各竞争对手的独特优势
        7. 市场机会发现 - 发现市场空白和机会
        8. 战略建议 - 提供具体的竞争策略建议

        请提供具体、可操作的分析结果，重点关注如何获得竞争优势。
        请确保报告内容完整且不重复。
        """
        
        try:
            report = self.analysis_agent.run(analysis_prompt)
            content = report.content
            
            # 如果响应内容为空或过短，返回备用分析
            if len(content.strip()) < 100:
                return self._generate_fallback_analysis(competitor_data)
            
            return content
        except Exception as e:
            return f"分析过程中出现错误: {str(e)}"
    
    def _generate_fallback_analysis(self, competitor_data: List[Dict]) -> str:
        """生成备用分析报告"""
        if not competitor_data:
            return "没有竞争对手数据可供分析"
        
        analysis = f"""
# 竞争对手分析报告（OpenAI 备用版本）

## 分析概览
成功分析了 {len(competitor_data)} 个竞争对手的数据。

## 竞争对手列表
"""
        
        for i, competitor in enumerate(competitor_data, 1):
            analysis += f"""
### {i}. {competitor.get('company_name', f'竞争对手 {i}')}
- **网站**: {competitor.get('competitor_url', 'N/A')}
- **定价策略**: {competitor.get('pricing', 'N/A')[:200]}...
- **关键功能**: {', '.join(competitor.get('key_features', [])[:3]) if competitor.get('key_features') else 'N/A'}
- **技术栈**: {', '.join(competitor.get('tech_stack', [])[:3]) if competitor.get('tech_stack') else 'N/A'}
- **营销重点**: {competitor.get('marketing_focus', 'N/A')[:200]}...

"""
        
        analysis += """
## 基础分析建议

### 1. 市场定位分析
- 分析各竞争对手的市场定位和差异化策略
- 识别市场空白和机会

### 2. 产品功能对比
- 对比各竞争对手的核心功能和特性
- 发现功能优势和不足

### 3. 定价策略分析
- 分析定价模式和策略
- 制定有竞争力的定价方案

### 4. 技术栈对比
- 分析各竞争对手使用的技术
- 评估技术优势和劣势

### 5. 营销策略分析
- 分析目标受众和营销重点
- 制定差异化营销策略

## 建议
1. 深入分析竞争对手的优劣势
2. 制定差异化竞争策略
3. 关注市场趋势和客户需求
4. 持续监控竞争对手动态

---
*注：此为备用分析报告，建议检查OpenAI API配置以获得更深入的分析。*
"""
        
        return analysis

# Qwen 分析器
class QwenAnalyzer:
    """使用 Qwen 的竞争对手分析器"""
    
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.llm_cfg = {
            'model': model,
            'model_type': 'qwen_dashscope',
            'api_key': api_key,
            'generate_cfg': {
                'top_p': 0.8,
                'temperature': 0.7
            }
        }
        
        # 初始化 Qwen Agent
        if QWEN_AVAILABLE:
            self.assistant = Assistant(
                llm=self.llm_cfg,
                system_message="你是一个专业的竞争对手分析专家。请根据提供的信息进行深入分析，提供具体、可操作的建议。",
                function_list=[]
            )
        else:
            self.assistant = None
    
    def analyze_competitors(self, competitor_data: List[Dict]) -> str:
        """分析竞争对手数据"""
        if not self.assistant:
            return "Qwen Agent 未正确初始化，请检查 qwen-agent 库是否正确安装"
        
        # 格式化数据
        formatted_data = json.dumps(competitor_data, indent=2, ensure_ascii=False)
        
        # 构建分析提示
        analysis_prompt = f"""
        请分析以下竞争对手数据，并提供详细的竞争分析报告：

        {formatted_data}

        请从以下角度进行分析：
        1. 市场定位分析 - 分析各竞争对手的市场定位和差异化策略
        2. 产品功能对比 - 对比各竞争对手的核心功能和特性
        3. 定价策略分析 - 分析定价模式和策略
        4. 技术栈对比 - 分析各竞争对手使用的技术
        5. 营销策略分析 - 分析目标受众和营销重点
        6. 竞争优势识别 - 识别各竞争对手的独特优势
        7. 市场机会发现 - 发现市场空白和机会
        8. 战略建议 - 提供具体的竞争策略建议

        请提供具体、可操作的分析结果，重点关注如何获得竞争优势。
        请确保报告内容完整且不重复。
        """
        
        try:
            messages = [{'role': 'user', 'content': analysis_prompt}]
            response_content = ""
            seen_content = set()  # 用于去重
            last_content_length = 0  # 记录上次内容长度
            
            # 处理Qwen Agent的流式响应
            for response in self.assistant.run(messages=messages):
                # 检查响应类型并提取内容
                if isinstance(response, list):
                    for item in response:
                        if isinstance(item, dict):
                            if 'content' in item:
                                content = item['content']
                                # 检查内容是否真正新增（避免重复的标题和开头）
                                if content and len(content) > last_content_length:
                                    new_content = content[last_content_length:]
                                    if new_content not in seen_content and len(new_content.strip()) > 0:
                                        response_content += new_content
                                        seen_content.add(new_content)
                                        last_content_length = len(content)
                            elif 'extra' in item and 'model_service_info' in item['extra']:
                                model_info = item['extra']['model_service_info']
                                if 'output' in model_info and 'choices' in model_info['output']:
                                    choices = model_info['output']['choices']
                                    if choices and len(choices) > 0:
                                        choice = choices[0]
                                        if 'message' in choice and 'content' in choice['message']:
                                            content = choice['message']['content']
                                            if content and len(content) > last_content_length:
                                                new_content = content[last_content_length:]
                                                if new_content not in seen_content and len(new_content.strip()) > 0:
                                                    response_content += new_content
                                                    seen_content.add(new_content)
                                                    last_content_length = len(content)
                elif isinstance(response, dict):
                    if 'content' in response:
                        content = response['content']
                        if content and len(content) > last_content_length:
                            new_content = content[last_content_length:]
                            if new_content not in seen_content and len(new_content.strip()) > 0:
                                response_content += new_content
                                seen_content.add(new_content)
                                last_content_length = len(content)
                    elif 'extra' in response and 'model_service_info' in response['extra']:
                        model_info = response['extra']['model_service_info']
                        if 'output' in model_info and 'choices' in model_info['output']:
                            choices = model_info['output']['choices']
                            if choices and len(choices) > 0:
                                choice = choices[0]
                                if 'message' in choice and 'content' in choice['message']:
                                    content = choice['message']['content']
                                    if content and len(content) > last_content_length:
                                        new_content = content[last_content_length:]
                                        if new_content not in seen_content and len(new_content.strip()) > 0:
                                            response_content += new_content
                                            seen_content.add(new_content)
                                            last_content_length = len(content)
                elif hasattr(response, 'content'):
                    content = response.content
                    if content and len(content) > last_content_length:
                        new_content = content[last_content_length:]
                        if new_content not in seen_content and len(new_content.strip()) > 0:
                            response_content += new_content
                            seen_content.add(new_content)
                            last_content_length = len(content)
                else:
                    content = str(response)
                    if content and len(content) > last_content_length:
                        new_content = content[last_content_length:]
                        if new_content not in seen_content and len(new_content.strip()) > 0:
                            response_content += new_content
                            seen_content.add(new_content)
                            last_content_length = len(content)
            
            # 如果响应内容为空或过短，返回备用分析
            if len(response_content.strip()) < 100:
                return self._generate_fallback_analysis(competitor_data)
            
            # 后处理：清理可能的重复内容
            cleaned_content = self._clean_duplicate_content(response_content)
            
            return cleaned_content
        except Exception as e:
            return f"分析过程中出现错误: {str(e)}"
    
    def _clean_duplicate_content(self, content: str) -> str:
        """清理重复的内容，特别是重复的标题和开头"""
        import re
        
        # 按行分割内容
        lines = content.split('\n')
        cleaned_lines = []
        seen_lines = set()
        
        # 定义需要去重的模式
        duplicate_patterns = [
            r'^#+\s*竞争对手分析报告\s*$',
            r'^#+\s*分析报告\s*$',
            r'^#+\s*市场定位分析\s*$',
            r'^#+\s*产品功能对比\s*$',
            r'^#+\s*定价策略分析\s*$',
            r'^#+\s*技术栈对比\s*$',
            r'^#+\s*营销策略分析\s*$',
            r'^#+\s*竞争优势识别\s*$',
            r'^#+\s*市场机会发现\s*$',
            r'^#+\s*战略建议\s*$',
        ]
        
        for line in lines:
            line_stripped = line.strip()
            
            # 跳过空行
            if not line_stripped:
                cleaned_lines.append(line)
                continue
            
            # 检查是否是重复的标题
            is_duplicate_title = False
            for pattern in duplicate_patterns:
                if re.match(pattern, line_stripped, re.IGNORECASE):
                    if line_stripped in seen_lines:
                        is_duplicate_title = True
                        break
                    seen_lines.add(line_stripped)
                    break
            
            # 如果不是重复标题，或者虽然是标题但第一次出现，则保留
            if not is_duplicate_title:
                cleaned_lines.append(line)
        
        # 重新组合内容
        cleaned_content = '\n'.join(cleaned_lines)
        
        # 进一步清理：移除连续的重复段落
        # 按段落分割（以双换行符为分隔符）
        paragraphs = cleaned_content.split('\n\n')
        unique_paragraphs = []
        seen_paragraphs = set()
        
        for paragraph in paragraphs:
            paragraph_stripped = paragraph.strip()
            if paragraph_stripped and paragraph_stripped not in seen_paragraphs:
                # 检查段落是否包含重复的标题模式
                has_duplicate_title = False
                for pattern in duplicate_patterns:
                    if re.search(pattern, paragraph_stripped, re.IGNORECASE):
                        # 如果段落包含重复标题，只保留第一次出现的
                        if any(pattern in seen for seen in seen_paragraphs):
                            has_duplicate_title = True
                            break
                
                if not has_duplicate_title:
                    unique_paragraphs.append(paragraph)
                    seen_paragraphs.add(paragraph_stripped)
        
        return '\n\n'.join(unique_paragraphs)
    
    def _generate_fallback_analysis(self, competitor_data: List[Dict]) -> str:
        """生成备用分析报告"""
        if not competitor_data:
            return "没有竞争对手数据可供分析"
        
        analysis = f"""
# 竞争对手分析报告（Qwen 备用版本）

## 分析概览
成功分析了 {len(competitor_data)} 个竞争对手的数据。

## 竞争对手列表
"""
        
        for i, competitor in enumerate(competitor_data, 1):
            analysis += f"""
### {i}. {competitor.get('company_name', f'竞争对手 {i}')}
- **网站**: {competitor.get('competitor_url', 'N/A')}
- **定价策略**: {competitor.get('pricing', 'N/A')[:200]}...
- **关键功能**: {', '.join(competitor.get('key_features', [])[:3]) if competitor.get('key_features') else 'N/A'}
- **技术栈**: {', '.join(competitor.get('tech_stack', [])[:3]) if competitor.get('tech_stack') else 'N/A'}
- **营销重点**: {competitor.get('marketing_focus', 'N/A')[:200]}...

"""
        
        analysis += """
## 基础分析建议

### 1. 市场定位分析
- 分析各竞争对手的市场定位和差异化策略
- 识别市场空白和机会

### 2. 产品功能对比
- 对比各竞争对手的核心功能和特性
- 发现功能优势和不足

### 3. 定价策略分析
- 分析定价模式和策略
- 制定有竞争力的定价方案

### 4. 技术栈对比
- 分析各竞争对手使用的技术
- 评估技术优势和劣势

### 5. 营销策略分析
- 分析目标受众和营销重点
- 制定差异化营销策略

## 建议
1. 深入分析竞争对手的优劣势
2. 制定差异化竞争策略
3. 关注市场趋势和客户需求
4. 持续监控竞争对手动态

---
*注：此为备用分析报告，建议检查Qwen API配置以获得更深入的分析。*
"""
        
        return analysis

# 获取竞争对手 URL 的函数
def get_competitor_urls(url: str = None, description: str = None) -> List[str]:
    """获取竞争对手 URL 列表"""
    if not url and not description:
        raise ValueError("请提供 URL 或描述")

    if search_engine == "Perplexity AI - Sonar Pro":
        perplexity_url = "https://api.perplexity.ai/chat/completions"
        
        content = "找到 10 个与公司相似的竞争对手公司 URL，"
        if url and description:
            content += f"URL: {url} 和描述: {description}"
        elif url:
            content += f"URL: {url}"
        else:
            content += f"描述: {description}"
        content += "。只返回 URL，不要其他文本。"

        payload = {
            "model": "sonar-pro",
            "messages": [
                {
                    "role": "system",
                    "content": "精确并只返回  10个公司 URL。"
                },
                {
                    "role": "user",
                    "content": content
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.8,
        }
        
        headers = {
            "Authorization": f"Bearer {st.session_state.perplexity_api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(perplexity_url, json=payload, headers=headers)
            response.raise_for_status()
            urls = response.json()['choices'][0]['message']['content'].strip().split('\n')
            return [url.strip() for url in urls if url.strip()]
        except Exception as e:
            st.error(f"从 Perplexity 获取竞争对手 URL 时出错: {str(e)}")
            return []

    else:  # Exa AI
        try:
            if EXA_AVAILABLE:
                exa = Exa(api_key=st.session_state.exa_api_key)
                
                if url:
                    # 使用 find_similar 查找相似网站
                    result = exa.find_similar(
                        url=url,
                        num_results=10,
                        exclude_source_domain=True,
                        category="company"
                    )
                else:
                    # 使用 search 根据描述搜索
                    result = exa.search(
                        description,
                        type="neural",
                        category="company",
                        use_autoprompt=True,
                        num_results=10
                    )
                
                # 确保返回10个URL，如果不足则尝试补充
                urls = [item.url for item in result.results]
                
                # 如果结果不足10个，尝试使用不同的搜索策略
                if len(urls) < 10 and description:
                    try:
                        # 尝试使用不同的搜索词
                        additional_result = exa.search(
                            f"{description} competitors",
                            type="neural",
                            num_results=10 - len(urls)
                        )
                        additional_urls = [item.url for item in additional_result.results]
                        urls.extend(additional_urls)
                    except:
                        pass
                
                # 去重并限制为10个
                unique_urls = list(dict.fromkeys(urls))[:10]
                return unique_urls
            else:
                st.error("Exa 库未安装，请运行: pip install exa-py")
                return []
        except Exception as e:
            st.error(f"从 Exa 获取竞争对手 URL 时出错: {str(e)}")
            return []

# 使用 Firecrawl 提取竞争对手信息
def extract_competitor_info(competitor_url: str) -> Optional[Dict]:
    """使用 Firecrawl 提取竞争对手信息"""
    try:
        if not FIRECRAWL_AVAILABLE:
            st.error("Firecrawl 库未安装，请运行: pip install firecrawl-py")
            return None
            
        # 初始化 FirecrawlApp
        app = FirecrawlApp(api_key=st.session_state.firecrawl_api_key)
        
        # 添加通配符以爬取子页面
        url_pattern = f"{competitor_url}/*"
        
        # 定义数据提取提示
        extraction_prompt = """
        提取有关公司产品的详细信息，包括：
        - 公司名称和基本信息
        - 定价详情、计划和层级
        - 关键功能和主要能力
        - 技术栈和技术详情
        - 营销重点和目标受众
        - 客户反馈和推荐
        
        分析整个网站内容，为每个字段提供全面信息。
        """
        
        # 调用 Firecrawl 提取功能
        response = app.extract(
            [url_pattern],
            prompt=extraction_prompt,
            schema=CompetitorDataSchema.model_json_schema()
        )
        
        # 处理 ExtractResponse 对象
        try:
            if hasattr(response, 'success') and response.success:
                if hasattr(response, 'data') and response.data:
                    extracted_info = response.data
                    
                    # 创建 JSON 结构
                    competitor_json = {
                        "competitor_url": competitor_url,
                        "company_name": extracted_info.get('company_name', 'N/A') if isinstance(extracted_info, dict) else getattr(extracted_info, 'company_name', 'N/A'),
                        "pricing": extracted_info.get('pricing', 'N/A') if isinstance(extracted_info, dict) else getattr(extracted_info, 'pricing', 'N/A'),
                        "key_features": extracted_info.get('key_features', [])[:5] if isinstance(extracted_info, dict) and extracted_info.get('key_features') else getattr(extracted_info, 'key_features', [])[:5] if hasattr(extracted_info, 'key_features') else ['N/A'],
                        "tech_stack": extracted_info.get('tech_stack', [])[:5] if isinstance(extracted_info, dict) and extracted_info.get('tech_stack') else getattr(extracted_info, 'tech_stack', [])[:5] if hasattr(extracted_info, 'tech_stack') else ['N/A'],
                        "marketing_focus": extracted_info.get('marketing_focus', 'N/A') if isinstance(extracted_info, dict) else getattr(extracted_info, 'marketing_focus', 'N/A'),
                        "customer_feedback": extracted_info.get('customer_feedback', 'N/A') if isinstance(extracted_info, dict) else getattr(extracted_info, 'customer_feedback', 'N/A')
                    }
                    
                    return competitor_json
                else:
                    return None
            else:
                return None
                
        except Exception as response_error:
            return None
            
    except Exception as e:
        st.error(f"使用 Firecrawl 提取信息失败: {str(e)}")
        return None

# 生成对比表格
def generate_comparison_report(competitor_data: List[Dict]) -> None:
    """生成竞争对手对比报告"""
    if not competitor_data:
        st.error("没有可比较的竞争对手数据")
        return
    
    # 准备表格数据
    table_data = []
    for competitor in competitor_data:
        row = {
            '公司': f"{competitor.get('company_name', 'N/A')}",
            '网站': competitor.get('competitor_url', 'N/A'),
            '定价': competitor.get('pricing', 'N/A')[:100] + '...' if len(competitor.get('pricing', '')) > 100 else competitor.get('pricing', 'N/A'),
            '关键功能': ', '.join(competitor.get('key_features', [])[:3]) if competitor.get('key_features') else 'N/A',
            '技术栈': ', '.join(competitor.get('tech_stack', [])[:3]) if competitor.get('tech_stack') else 'N/A',
            '营销重点': competitor.get('marketing_focus', 'N/A')[:100] + '...' if len(competitor.get('marketing_focus', '')) > 100 else competitor.get('marketing_focus', 'N/A'),
            '客户反馈': competitor.get('customer_feedback', 'N/A')[:100] + '...' if len(competitor.get('customer_feedback', '')) > 100 else competitor.get('customer_feedback', 'N/A')
        }
        table_data.append(row)
    
    # 创建并显示表格
    df = pd.DataFrame(table_data)
    st.subheader("📊 竞争对手对比表")
    st.markdown("---")
    
    # 使用更好的表格显示
    st.dataframe(
        df, 
        use_container_width=True,
        hide_index=True,
        column_config={
            "公司": st.column_config.TextColumn("公司名称", width="medium"),
            "网站": st.column_config.LinkColumn("网站链接", width="medium"),
            "定价": st.column_config.TextColumn("定价策略", width="large"),
            "关键功能": st.column_config.TextColumn("关键功能", width="large"),
            "技术栈": st.column_config.TextColumn("技术栈", width="medium"),
            "营销重点": st.column_config.TextColumn("营销重点", width="large"),
            "客户反馈": st.column_config.TextColumn("客户反馈", width="large")
        }
    )
    
    # 显示详细数据
    st.subheader("📋 详细竞争对手信息")
    for i, competitor in enumerate(competitor_data, 1):
        with st.expander(f"🏢 {competitor.get('company_name', f'竞争对手 {i}')} - 详细信息"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**基本信息**")
                st.write(f"**公司名称**: {competitor.get('company_name', 'N/A')}")
                st.write(f"**网站**: {competitor.get('competitor_url', 'N/A')}")
                
                st.markdown("**定价信息**")
                st.write(competitor.get('pricing', 'N/A'))
                
                st.markdown("**营销重点**")
                st.write(competitor.get('marketing_focus', 'N/A'))
            
            with col2:
                st.markdown("**关键功能**")
                features = competitor.get('key_features', [])
                if features:
                    for feature in features:
                        st.write(f"• {feature}")
                else:
                    st.write("N/A")
                
                st.markdown("**技术栈**")
                tech_stack = competitor.get('tech_stack', [])
                if tech_stack:
                    for tech in tech_stack:
                        st.write(f"• {tech}")
                else:
                    st.write("N/A")
                
                st.markdown("**客户反馈**")
                st.write(competitor.get('customer_feedback', 'N/A'))
    
    # 显示原始数据（可选）
    with st.expander("🔍 查看原始JSON数据"):
        st.json(competitor_data)

# 备用分析函数（不依赖AI）
def generate_fallback_analysis(competitor_data: List[Dict]) -> str:
    """生成备用分析报告（不依赖AI）"""
    if not competitor_data:
        return "没有竞争对手数据可供分析"
    
    analysis = f"""
# 竞争对手分析报告（基础版本）

## 分析概览
成功分析了 {len(competitor_data)} 个竞争对手的数据。

## 竞争对手列表
"""
    
    for i, competitor in enumerate(competitor_data, 1):
        analysis += f"""
### {i}. {competitor.get('company_name', f'竞争对手 {i}')}
- **网站**: {competitor.get('competitor_url', 'N/A')}
- **定价策略**: {competitor.get('pricing', 'N/A')[:200]}...
- **关键功能**: {', '.join(competitor.get('key_features', [])[:3]) if competitor.get('key_features') else 'N/A'}
- **技术栈**: {', '.join(competitor.get('tech_stack', [])[:3]) if competitor.get('tech_stack') else 'N/A'}
- **营销重点**: {competitor.get('marketing_focus', 'N/A')[:200]}...

"""
    
    analysis += """
## 基础分析建议

### 1. 市场定位分析
- 分析各竞争对手的市场定位和差异化策略
- 识别市场空白和机会

### 2. 产品功能对比
- 对比各竞争对手的核心功能和特性
- 发现功能优势和不足

### 3. 定价策略分析
- 分析定价模式和策略
- 制定有竞争力的定价方案

### 4. 技术栈对比
- 分析各竞争对手使用的技术
- 评估技术优势和劣势

### 5. 营销策略分析
- 分析目标受众和营销重点
- 制定差异化营销策略

## 建议
1. 深入分析竞争对手的优劣势
2. 制定差异化竞争策略
3. 关注市场趋势和客户需求
4. 持续监控竞争对手动态

---
*注：此为基础分析报告，建议配置AI模型以获得更深入的分析。*
"""
    
    return analysis

# 主程序逻辑
def main():
    """主程序逻辑"""
    # 检查必要的配置
    required_configs = []
    
    if not st.session_state.get('model_provider'):
        required_configs.append("AI模型提供商")
    if not st.session_state.get('search_engine'):
        required_configs.append("搜索引擎")
    if not st.session_state.get('firecrawl_api_key'):
        required_configs.append("Firecrawl API")
    
    if required_configs:
        st.warning(f"请先配置以下选项：{', '.join(required_configs)}")
        return
    
    # 分析按钮
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 开始分析竞争对手", type="primary", use_container_width=True):
            if url or description:
                # 获取竞争对手 URL
                with st.spinner("正在搜索竞争对手..."):
                    competitor_urls = get_competitor_urls(url=url, description=description)
                    st.write(f"找到 {len(competitor_urls)} 个竞争对手 URL")
                
                if not competitor_urls:
                    st.error("未找到竞争对手 URL！")
                    st.stop()
                
                # 提取竞争对手信息
                competitor_data = []
                successful_extractions = 0
                failed_extractions = 0
                
                for i, comp_url in enumerate(competitor_urls):
                    with st.spinner(f"正在使用 Firecrawl 分析竞争对手 {i+1}/{len(competitor_urls)}: {comp_url}"):
                        competitor_info = extract_competitor_info(comp_url)
                        
                        if competitor_info is not None:
                            competitor_data.append(competitor_info)
                            successful_extractions += 1
                            st.success(f"✓ 成功分析 {comp_url}")
                        else:
                            failed_extractions += 1
                            st.error(f"✗ 分析失败 {comp_url}")
                
                if competitor_data:
                    st.success(f"成功分析了 {successful_extractions}/{len(competitor_urls)} 个竞争对手！")
                    
                    # 生成对比表格
                    with st.spinner("正在生成对比表格..."):
                        generate_comparison_report(competitor_data)
                    
                    # 生成分析报告
                    with st.spinner("正在生成分析报告..."):
                        try:
                            # 根据选择的模型提供商进行分析
                            if st.session_state.model_provider == "openai":
                                if st.session_state.get('openai_api_key'):
                                    analyzer = OpenAIAnalyzer(st.session_state.openai_api_key)
                                    analysis_report = analyzer.analyze_competitors(competitor_data)
                                else:
                                    raise Exception("OpenAI API Key 未配置")
                            else:  # qwen
                                if st.session_state.get('dashscope_api_key'):
                                    analyzer = QwenAnalyzer(
                                        st.session_state.dashscope_api_key,
                                        st.session_state.get('qwen_model', 'qwen-max')
                                    )
                                    analysis_report = analyzer.analyze_competitors(competitor_data)
                                else:
                                    raise Exception("DashScope API Key 未配置")
                            
                            # 显示分析报告
                            st.subheader("🧠 竞争对手智能分析报告")
                            st.markdown("---")
                            
                            # 检查报告内容是否为空或包含错误信息
                            if analysis_report and not analysis_report.startswith("分析过程中出现错误") and not analysis_report.startswith("Agent 未正确初始化"):
                                # 使用容器美化显示
                                with st.container():
                                    st.markdown(analysis_report)
                            else:
                                st.error("AI分析报告生成失败，显示基础分析报告")
                                st.markdown("---")
                                fallback_report = generate_fallback_analysis(competitor_data)
                                st.markdown(fallback_report)
                                
                        except Exception as e:
                            st.error(f"AI分析过程中出现错误: {str(e)}")
                            st.info("显示基础分析报告作为备用方案")
                            st.markdown("---")
                            fallback_report = generate_fallback_analysis(competitor_data)
                            st.markdown(fallback_report)
                    
                    st.success("分析完成！")
                else:
                    st.error("无法提取任何竞争对手数据")
            else:
                st.error("请提供 URL 或描述")

# 运行主程序
if __name__ == "__main__":
    main()

# 使用说明
with st.expander("📖 使用说明"):
    st.markdown("""
    ## 使用说明
    
    ### 1. 安装依赖
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
    
    ### 2. 获取 API 密钥
    - **OpenAI API**: 访问 [OpenAI Platform](https://platform.openai.com/api-keys)
    - **DashScope API**: 访问 [阿里云 DashScope](https://dashscope.console.aliyun.com/)
    - **Firecrawl API**: 访问 [Firecrawl](https://www.firecrawl.dev/app/api-keys)
    - **Perplexity API** (可选): 访问 [Perplexity](https://www.perplexity.ai/settings/api)
    - **Exa API** (可选): 访问 [Exa](https://dashboard.exa.ai/api-keys)
    
    ### 2.1 API 密钥安全管理
    **⚠️ 重要安全提示：**
    - 请勿将API密钥硬编码在代码中
    - 不要将包含API密钥的文件提交到版本控制系统
    - 建议使用环境变量或配置文件管理API密钥
    - 定期轮换API密钥以确保安全
    
    ### 3. 运行应用
    ```bash
    streamlit run competitor_agent_team_combined.py
    ```
    
    ### 4. 功能特点
    - **多模型支持**: 支持 OpenAI GPT-4 和 Qwen (通义千问)
    - **智能搜索引擎**: 支持 Perplexity AI 和 Exa AI
    - **专业爬取**: 使用 Firecrawl 提取高质量网站数据
    - **深度分析**: 生成详细的分析报告和对比表格
    - **错误处理**: 智能错误处理和备用方案
    
    ### 5. 技术优势
    - **Firecrawl**: 专业的网站爬取工具，能提取结构化数据
    - **多AI模型**: 灵活的AI模型选择，适应不同需求
    - **多引擎支持**: 灵活的竞争对手发现机制
    - **容错机制**: 即使AI分析失败，也能提供基础分析
    
    ### 6. 注意事项
    - 确保网络连接正常
    - API 密钥需要有效
    - 某些网站可能无法访问
    - 建议使用 qwen-max 或 gpt-4o 模型获得最佳效果
    - 如果AI分析失败，系统会自动提供基础分析报告
    """)

# 依赖检查
with st.expander("🔧 依赖检查"):
    st.markdown("### 依赖库状态")
    
    dependencies = [
        ("Streamlit", True, "Web界面框架"),
        ("Pandas", True, "数据处理"),
        ("Requests", True, "HTTP请求"),
        ("Pydantic", True, "数据验证"),
        ("Agno (OpenAI)", AGNO_AVAILABLE, "OpenAI模型支持"),
        ("Qwen Agent", QWEN_AVAILABLE, "Qwen模型支持"),
        ("Firecrawl", FIRECRAWL_AVAILABLE, "网站爬取"),
        ("Exa", EXA_AVAILABLE, "Exa搜索引擎支持")
    ]
    
    for dep_name, available, description in dependencies:
        status = "✅ 已安装" if available else "❌ 未安装"
        st.write(f"- **{dep_name}**: {status} - {description}")
    
    if not all([AGNO_AVAILABLE or QWEN_AVAILABLE, FIRECRAWL_AVAILABLE]):
        st.warning("⚠️ 请安装必要的依赖库以获得完整功能")
