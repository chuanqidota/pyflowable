
  # pyflowable

  **基于 Flowable 6.8.0 的 Python 企业流程审批与自动化工作流系统** —— 用 Django 封装 Flowable BPM 引擎，让业务开发者以"写 Python 类"的方式定义和驱动审批流程。

  ![Python](https://img.shields.io/badge/Python-3.x-blue) ![Django](https://img.shields.io/badge/Django-6.0-green) ![Flowable](https://img.shields.io/badge/Flowable-6.8.0-orange)
  ![License](https://img.shields.io/badge/License-Apache--2.0-lightgrey)

  ---

  ## 一、为什么做这个项目

  Flowable 是一个成熟的开源 BPM 引擎，但直接在业务系统中使用它有三个痛点：

  1. **调用繁琐**：原生 REST API 粒度细、参数多，错误处理散落在各处，业务代码很快会被一堆 `requests.post(...)` 淹没；
  2. **引擎是黑盒**：Flowable 只懂"流程"，不懂"业务"。引擎库里的数据无法直接表达「工单池 / 我的待办 / 我的工单」这类带业务语义的查询；
  3. **流程与代码割裂**：谁在哪个节点推进流程、驳回回到哪个节点、哪个节点该自动执行——这些逻辑如果没有统一承载，会逐渐腐化为面条代码。

  pyflowable 的答案一句话概括：**把 BPMN 流程模型"翻译"成 Python 代码结构，用命名约定 + 装饰器 + 返回值路由来驱动流程往前走**。业务开发者不需要关心 REST 调用和状态同步，只需要回答一个问题——"这个节点要做什么"。

  ---

  ## 二、核心设计思想

  整个项目的设计源自两条约定：

  > **Flowable 流程的英文名称和类名称做映射，任务名称和类方法名称做映射；代码驱动 Flowable 的流程往前走。**

  具体展开为三个约定：

  | BPMN 世界 | Python 世界 | 说明 |
  |---|---|---|
  | 流程定义 key | `apps/flowable/process/` 下的**类名** | 一个流程 = 一个类，如 `AppApplyProcess` |
  | 任务节点（`xxx_task`） | 类上的**同名方法** | 节点名必须以 `_task` 结尾，如 `submit_task` |
  | 流程走向（网关分支） | **方法返回值** | 返回约定的 dict，声明"同意 / 驳回 / 自动执行 / 候选人" |

  这意味着：**流程图即代码，代码即流程图**。在 Flowable UI 里画好的 BPMN，与 Python 类的方法签名天然一一对应，通过反射机制自动衔接，无需任何手工绑定。

  ---

  ## 三、整体架构思路

  系统采用**双引擎、双数据库**架构：Flowable 负责它擅长的（流程拓扑流转、网关计算、多实例或签），业务系统负责自己擅长的（表单、权限、查询、审计）。

  ```mermaid
  graph TB
      subgraph 业务侧 ["pyflowable（Django + DRF）"]
          A["REST 封装层<br/>FlowableHandler<br/>统一 REST 调用与错误处理"]
          B["状态镜像层<br/>Django 模型双写流程状态<br/>工单池 / 我的待办 可查询"]
          C["代码驱动层<br/>装饰器生命周期 + 返回值路由<br/>业务开发者只写节点逻辑"]
      end

      subgraph 引擎侧 ["Docker 运行的 Flowable 6.8.0"]
          D["flowable-rest :8081<br/>流程引擎 API"]
          E["flowable-ui :8082<br/>BPMN 建模界面"]
      end

      F[("业务数据库<br/>工单/任务/操作记录")]
      G[("Flowable 引擎库<br/>流程实例/执行树")]

      C --> A --> D
      D --> G
      B --> F
      C --> B
      E -.->|流程定义部署| D
  ```

  三层各自的设计意图：

  ### 1. REST 封装层——消灭重复样板

  `FlowableHandler` 封装 flowable-rest 的全部交互（流程定义、流程实例、任务、用户组、流程图等），统一返回 `(bool, msg)` 元组，统一错误处理与认证。业务代码从此不再出现裸的 HTTP 调用。

  ### 2. 状态镜像层——让流程数据变成业务数据

  Flowable 对业务系统是黑盒，"谁有哪些待办"这种高频查询不应该穿透到引擎库。因此在业务库中用 Django 模型**镜像**流程状态：

  - `Process` / `ProcessGroup` / `ProcessAttr`——流程定义、分组、表单属性的本地登记；
  - `Instance`——工单实例：引擎实例 ID、状态、流程图快照（base64）、操作记录（JSON 审计日志）；
  - `InstanceTask`——流程启动时为**每个节点预建一行**，记录 key、分配人、状态、参数。

  镜像层的价值：**「流程池 / 我的待办 / 我的工单 / 已办」全部变成普通 SQL 查询**，可以随意 join 业务表、分页、过滤，这是引擎库做不到的。

  ### 3. 代码驱动层——声明式 DSL（本项目最核心的设计）

  每个节点方法用装饰器声明生命周期，用返回值声明流程走向：

  - `@finish_task`——用于**除最后一个之外**的所有节点：执行前抓取流程图快照存档、流转任务状态、执行业务逻辑、完成后推进引擎，并按需自动执行下一节点；
  - `@complete_task`——只用于**最后一个节点**，随流程结束收尾。

  任务状态机：

  ```mermaid
  stateDiagram-v2
      [*] --> init: 流程启动时预建节点
      init --> ing: 认领 / 开始办理
      ing --> finish: 业务逻辑执行成功，推进引擎
      ing --> error: 执行异常
      finish --> [*]
  ```

  ---

  ## 四、API 设计风格：返回值即路由

  节点方法不需要调用任何引擎 API，**返回值就是流程走向的声明**。四个路由函数覆盖了审批流的全部语义：

  | 路由函数 | 语义 | 关键参数 |
  |---|---|---|
  | `next_approval` | 进入下一个**人工审批**节点 | 候选人列表（配合 BPMN 多实例或签 `assigneeList`） |
  | `next_gateway_agree` | 网关**同意**分支 | `auto_next_task=True` 时自动连续执行后续节点 |
  | `next_gateway_reject` | 网关**驳回**分支 | `target` 驳回目标节点、`clean` 需重置状态的节点 |
  | `next_auto_task` | 下一节点**自动执行**（无需人工介入） | — |

  值得注意的是**驳回语义由 Python 侧实现**：BPMN 里网关只认变量，而"驳回到哪个节点、哪些节点状态要清零重走"这种业务规则，通过 `next_gateway_reject(target=..., clean=[...])` 显式声明，清晰且可单测。

  ---

  ## 五、写一个流程是什么体验

  以「应用申请」流程为例（提交 → 领导或签审批 → 网关判断 → 运维处理 → DBA 处理收尾），BPMN 在 flowable-ui 中绘制，Python 侧对应的全部代码：

  ```python
  from flowable.utils.decorator import finish_task, complete_task
  from flowable.utils.next_task import (
      next_approval, next_gateway_agree, next_gateway_reject, next_auto_task
  )

  class AppApplyProcess:
      """类名 = 流程定义 key"""

      @finish_task
      def submit_task(self, *args, **kwargs):
          return next_approval(["xiaoa"])                # 指定下一审批节点的候选人

      @finish_task
      def leader_task(self, *args, **kwargs):
          if kwargs.get("allow") == 1:
              return next_gateway_agree(auto_next_task=True)   # 同意，后续节点自动执行
          return next_gateway_reject(                          # 驳回：回到提交节点，
              target="submit_task", clean=["leader_task"]       # 并重置领导审批节点状态
          )

      @finish_task
      def sor_task(self, *args, **kwargs):
          return next_auto_task()                       # 运维处理完，自动进入下一节点

      @complete_task
      def dba_task(self, *args, **kwargs):              # 最后一个节点，流程结束
          ...
  ```

  流程推进时，框架通过 `importlib` + `methodcaller` 反射定位到类与方法——**新增一个流程，只需在 `process/` 目录下新增一个类，再在 Flowable UI 里画好并部署同 key 的 BPMN，无需改动框架任何代码**。

  一次完整的生命周期：

  ```mermaid
  sequenceDiagram
      participant U as 用户
      participant API as DRF 接口
      participant Celery as Celery Worker
      participant P as 节点方法(装饰器包裹)
      participant F as Flowable 引擎

      U->>API: 提交工单 submit
      API->>F: 启动流程实例(拉取节点清单，预建 InstanceTask)
      U->>API: 办理节点 handle
      API->>Celery: 异步投递任务
      Celery->>P: 反射调用节点方法
      P->>P: 抓取流程图快照 / 状态流转 init→ing→finish
      P->>F: complete 任务(携带路由变量)
      F-->>P: 返回下一任务
      P->>P: 若声明 auto_next_task，继续自动执行
  ```

  ---

  ## 六、业务能力

  围绕工单全生命周期的动作均封装为服务层接口：**提交（submit）、撤回（repeal）、认领（claim）、转办（delegate）、协调后处理（resolve）、办理（handle）**。办理走 Celery 异步执行，避免长事务阻塞；REST API 基于
  JWT 认证，并由 drf-spectacular 自动生成交互式 Swagger 文档。

  ---

  ## 七、快速开始

  ```bash
  # 1. 启动 Flowable 引擎（rest:8081 / ui:8082）
  docker compose up -d

  # 2. 安装依赖
  pip install -r requirement.txt

  # 3. 初始化并启动 Django
  python manage.py migrate && python manage.py runserver
  ```

  引擎连接信息通过 `config/config.yaml` 配置（`FLOWABLE_HOST / USERNAME / PASSWORD / BUSINESS_KEY`）。**详细的本地部署与端到端测试步骤（提交 → 审批 → 认领 → 办理的完整 15 步）、以及新流程接入指南，见
  [`docs/说明文档.md`](docs/说明文档.md)。**

  ---

  ## License

  [Apache License 2.0](LICENSE)
