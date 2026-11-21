# client-order-reply-skill

![Version](https://img.shields.io/badge/version-2.1.0-2f6f9f)
![License](https://img.shields.io/badge/license-MIT-4c9a2a)
![Compatible](https://img.shields.io/badge/agents-Codex%20%7C%20Claude%20Code%20%7C%20Cursor%20%7C%20Antigravity-333333)

给 Codex、Claude Code、Cursor、Antigravity、OpenCode 等 AI 编程助手用的**接单回复与谈单 Skill**。

接金融实证、量化估值、工程仿真、数据分析、AI 算法、软件开发或科研配套单时，把客户的消息、截图、任务书、数据或工程文件直接丢给它。它会先把整单精读几遍，遇到拿不准的专业细节先全网搜索查证，再结合对应行业的真实卡点和谈单策略，写一段**像真人在微信或闲鱼上打字、没有 AI 腔、可直接复制发送**的回复。

## 解决什么问题

普通 AI 写接单回复有四个通病：扫一眼就瞎编、满嘴客服和翻译腔、动不动主动报白菜价、不看领域盲目套固定模板。这个 Skill 从流程上卡死了这四个问题：

| 核心能力 | 具体做法 |
| --- | --- |
| **先三遍精读，再动笔** | 强制过完完整聊天上下文、截图逐行文字和附件源码/工程文件，拆清客户画像、明面要求、隐含工作量与当前谈单阶段，不扫一眼就瞎回 |
| **不懂就全网搜索核实** | 遇到陌生模型、前沿审稿方法、数据库口径、国标/行标、软件报错或细分行情，主动联网检索查证后再回复；查不到或未联网时如实提示，严禁编造参数与标准 |
| **深度去除 AI 味** | 禁用顿号/分号/冒号/括号/引号/感叹号/列表，过滤客服套话、书面连接词与工整排比；按谈单阶段弹性控制字数（30 字破冰到 280 字多项确认），不搞每条都一样的“五件套模板” |
| **默认绝对不报价** | 除非你明确要求报价，否则回复正文里一个价格数字、价位词都不出，先把技术难度、工作量和交付讲透，再自然要资料或让客户先出预算 |
| **报价必须对得起工作量** | 仅在你明确让报价时启用五维核价（有效工时 + 技术稀缺度 + 数据/算力硬成本 + 加急系数 + 返工与讲解风险），绝不乱报低价、绝不照抄范例数字、信息不全绝不硬报死价 |
| **亲切尊重，礼貌询问** | 先接住客户的处境再谈事，多用咱们和我帮你，讲难点不挑客户的错，有疑问礼貌问，尊重客户的决定，不催不逼，让客户觉得找对了人 |
| **金融 + 全领域专业知识库** | 按订单领域按需加载对应参考手册，说出只有真干过才知道的实操坑，一眼立住内行形象 |

## 效果对比：AI 味 vs 真人感

以客户咨询“多期 DID + 中介效应，觉得挺简单”为例：

| 普通 AI 回复 | 使用本 Skill 回复 |
| --- | --- |
| 您好！明白您的需求。关于您提到的多期 DID 和中介效应分析，其实并没有看起来那么简单。首先，多期 DID 存在异质性处理效应问题；其次，现在审稿对传统中介不太认可；最后，数据整理也很耗时。我可以为您提供一站式代码、结果表和说明服务，大概 500 到 800 元。请问您什么时候需要？ | 这个题做细了工作量其实不小，多期DID现在只跑普通双向固定效应很容易被导师或者审稿人挑刺，平行趋势动态图，安慰剂，还有csdid或者Bacon分解都得补上才站得住。中介这块好些学校也不认老的三步法了，得按江艇两步法配机制变量来写。CSMAR原始表里合并报表和母公司报表混在一起，ST和金融股剔除，跨表对齐和1%缩尾也都得细核。数据，do文件，三线表和结果解读都能给你配齐，方便的话先发下变量定义和年份，我看按什么深度给你排比较合适。 |

差异一眼可见：不瞎报价、不用客服腔、不用“首先其次最后”，直接点中 `csdid`、江艇两步法、母公司报表混杂等真痛点。

## 执行工作流

```text
收到客户消息 / 截图 / 任务书 / 数据 / 工程文件
        │
        ▼
[1] 三遍精读：扫全貌与附件 → 挖隐含工作量与雷区 → 判当前谈单阶段
        │
        ▼
[2] 联网检索：陌生方法 / 数据库口径 / 国标规范 / 软件报错 / 市场行情
        │
        ▼
[3] 路由领域手册：金融量化 / 电气CAE仿真 / AI数据开发 / 社科商业
        │
        ▼
[4] 报价开关判定：
    ├── 默认未让报价 ──► 正文零价格数字，拆技术难点 + 交付 + 推进下一步
    └── 明确要求报价 ──► 五维工作量核价 + 给用户3行核价备忘 + 合理带锚点报价
        │
        ▼
[5] 去 AI 味成文 + 7 项发前硬检 ──► 输出可直接复制发给客户的回复
```

## 覆盖的专业领域

所有领域知识按需懒加载，不拖慢日常触发：

| 领域模块 | 覆盖细分方向与内行切入点 |
| --- | --- |
| **金融、经济、会计与量化**（重点） | 公司金融实证（Stata `reghdfe` / 交错 DID `csdid` / Bacon 分解 / 江艇两步法 / PSM-DID / IV-2SLS / 空间计量 / 门槛回归）、CSMAR/Wind/CNRDS/WRDS 口径清洗坑、资产定价与时间序列（FF 因子 / DY 溢出 / TVP-SV-VAR / DCC-GARCH / Copula）、衍生品与风控（BSM / 蒙特卡洛 / 雪球 Greeks / VaR-ES / WOE-IV 评分卡 / KMV）、量化回测（未来函数公告日对齐 / 复权陷阱 / A股涨跌停与滑点）、动态三表联动与 DCF 估值（FCFF vs FCFE / WACC / 配平检查）、银行 ALM 与链上金融 |
| **电气、电力、控制与 CAE/CAD** | 电力电子与电机控制（PSIM / Simulink / PLECS / LLC 扫频 / PI 抗饱和 / FOC / MPC / VSG）、电力系统并网与高低穿（PowerFactory / PSCAD / PSS/E / 国标核对 / 微电网鲁棒优化）、机械流体热电磁 CAE（ANSYS / ABAQUS 接触非线性与 UMAT / COMSOL 多物理场 / 网格无关性）、硬件 PCB（AD / KiCad）、系统动力学与离散仿真（Vensim / Arena / FlexSim）、化工 Aspen 与土木岩土 |
| **数据、AI 算法、生信与开发** | 深度学习与 CV/NLP/大模型（YOLO 改进与消融 / 时序预测 / SHAP / LoRA / RAG / 算力与复现成本）、医学统计与药经（Cox / Nomogram / PSM / MR / Meta / 决策树与 Markov / PSA 龙卷风图）、生信单细胞（TCGA / GEO / Seurat）、数学建模、Web 全栈/小程序/爬虫反爬/自动化开发与范围边界 |
| **社科问卷与商业分析** | 问卷信效度与结构方程（SPSS / AMOS / Mplus / SmartPLS / PROCESS / 共同方法偏差 / LPA / fsQCA）、行研与运营分析（市场规模测算 / RFM / A/B 实验 / BI 看板）、科研规范绘图与 CiteSpace 文献计量；其余冷门跨学科任务自动触发联网查证 |

## 安装

### 方式一：使用 `npx skills` 一键安装

```bash
npx skills add 1837620622/client-order-reply-skill
```

### 方式二：手动克隆安装

**Codex / 通用 Agent（`~/.agents/skills`）**

```bash
git clone https://github.com/1837620622/client-order-reply-skill.git
mkdir -p ~/.agents/skills
cp -r client-order-reply-skill/skills/client-order-reply ~/.agents/skills/
```

**Claude Code（`~/.claude/skills`）**

```bash
git clone https://github.com/1837620622/client-order-reply-skill.git
mkdir -p ~/.claude/skills
cp -r client-order-reply-skill/skills/client-order-reply ~/.claude/skills/
```

**Cursor（`~/.cursor/skills`，也会读 `~/.agents/skills` 和 `~/.claude/skills`）**

```bash
mkdir -p ~/.cursor/skills
cp -r client-order-reply-skill/skills/client-order-reply ~/.cursor/skills/
```

**Antigravity（全局 `~/.gemini/config/skills`，项目内 `.agents/skills`）**

```bash
mkdir -p ~/.gemini/config/skills
cp -r client-order-reply-skill/skills/client-order-reply ~/.gemini/config/skills/
```

**其他客户端**

OpenCode，Gemini CLI 等支持 Agent Skills 的客户端一般会读项目内的 `.agents/skills/`，把 `skills/client-order-reply` 复制进去即可。Windows 用户把 `~` 换成 `%USERPROFILE%`。装完重启客户端生效。

## 怎么用

直接把客户原话、聊天截图、任务书、数据文件或工程文件发给助手就行：

- **日常回复（默认绝不报价）**
  - `客户说："帮我看看这个多期DID和机制检验能不能做，周五要"，怎么回`
  - `帮我回复客户，他把任务书和PSIM工程发过来了，先压一下现成模型的预期`
  - `客户问："这个DCF估值套个模板填一下数应该挺快的吧"，帮我回他`
- **明确要求报价（触发工作量五维核价）**
  - `这次帮我报个价，先算下大概工作量，别报低了，顺便写一段回复`
  - `这单我打算报 2800 到 3500，帮我把活和交付讲透再把价带出来`
- **处理砍价、加急、多条微信模式**
  - `客户嫌贵说别家只要300，帮我回，不白降价，给他减范围方案`
  - `帮我拆成 2 到 3 条短微信消息，语气再随口一点`

## 目录结构

```text
client-order-reply-skill/
├── README.md
├── LICENSE
└── skills/
    └── client-order-reply/
        ├── SKILL.md                                 # 技能主入口：六条铁律、五步工作流、路由表与自检清单
        └── references/
            ├── research-protocol.md                 # 三遍精读需求 + 强制全网检索核实 SOP
            ├── anti-ai-style.md                     # 去 AI 味手册 + 10 组改写对照 + 亲切尊重的待客语气
            ├── pricing-and-negotiation.md           # 默认不报价铁律 + 五维工作量核价模型 + 砍价拆招
            ├── domain-finance-econ.md               # 金融实证、量化回测、衍生品风控、估值与财会知识库
            ├── domain-engineering-sim.md            # 电气电力、控制仿真、机械 CAE/CAD、PCB 与化工土木知识库
            ├── domain-data-ai-dev.md                # AI 算法、数据分析、医学统计/药经、生信与开发爬虫知识库
            ├── domain-academic-business.md          # 社科问卷 SEM、商业分析与通用科研配套知识库
            └── examples.md                          # 14 段多领域实战标杆回复范例
```

## 协议

[MIT](LICENSE)
