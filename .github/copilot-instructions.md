<!-- Copilot / AI agent 说明（适用于 "Ants-remake with pygame" 项目） -->
# 项目概览

- 主要入口：`main.py` — 初始化 Pygame 循环、UI/菜单、事件处理，并绘制/更新所有精灵组。
- 核心游戏逻辑与数据模型：`object.py` — 定义 `GameState`、精灵类（`Ants`、`Harvester`、`Thrower`、`Bees`、`Lawn`、`Food`、`Bullet`）以及模块级精灵组（`Harvesters`、`Throwers`、`Bees_group`、`food_group`、`bullet_group`、`lawn_sprites`）。
- 资源目录：`assets/` 包含图片、字体和音乐；代码中以相对于项目根目录的路径直接加载（例如 `assets/ants/Thrower.gif`）。

# 架构要点（从多文件视角）

- `main.py` 负责主循环：读取输入 -> 修改模型（`GameState` 与精灵）-> 渲染。若修改游戏规则或行为，优先在 `object.py` 中实现。
- `object.py` 使用大量模块级全局（精灵组与 `GameState`），这些全局在 `main.py` 中被直接引用。新增行为或精灵应在 `object.py` 中定义并导出，再由 `main.py` 使用。
- 时间与调度采用 `pygame.time.get_ticks()` 记录时间戳（例：`plant_time`, `born_time`），通过时间差触发动作。新增基于时间的行为请沿用相同模式。

# 约定与常用模式（务必遵守）

- 精灵组为模块级对象，统一放在 `object.py`：例如 `Harvesters`、`Throwers`、`Bees_group`、`food_group`、`bullet_group`、`lawn_sprites`。
- 行/列区分：使用 `get_row(position)` 与 `row_y_dic` 将点击位置映射为行名（`'row1'..'row4'`）。
- 资源（食物）流：全局状态使用 `GameState.food`。每种蚂蚁在类级别声明 `food_cost`（例如 `Thrower.food_cost = 3`）；收集行为由 `Harvester.update(current_time)` 定期增加 `GameState.food` 并生成 `Food` 精灵。
- 碰撞检测：项目中提供 `bullet_collide_bees(bullet, Bees_group)` 助手函数；子弹碰到蜜蜂时会减少 `Bee.health` 并自毁。
- 资源加载：所有图片/字体以 `pygame.image.load(...)` 直接加载相对路径。请不要更改路径解析方式（运行和测试依赖项目根目录）。

# 运行与开发工作流

- 安装运行时依赖：`pygame`（仓库未包含 requirements）：
  - Windows PowerShell：
    ```powershell
    python -m pip install pygame
    ```
- 从项目根运行游戏：
  ```powershell
  python main.py
  ```
- 仓库内没有自动化测试。建议通过运行并在 Pygame 窗口中交互验证行为。

# 编辑代码时的建议（具体到本项目）

- 添加或修改行为时优先在 `object.py` 中实现类或辅助函数，保持 `main.py` 主要负责事件/UI 层。
- 保持渲染尺寸与坐标一致：屏幕分辨率固定为 `(1920, 1080)`；草坪为 9×4 网格，瓦片尺寸约 `170×170`（参见 `main.py` 的 lawn 创建循环）。
- 时间驱动的 `update` 方法签名须保持兼容：蚂蚁类使用 `update(self, current_time)`（`main.py` 会以 `Harvesters.update(current_time)` 形式调用），其他精灵通常使用无参 `update()`；请保留现有签名以兼容 `Group.update()`。

# 示例（方便快速上手）

- 新增蚂蚁：在 `object.py` 中创建 `Ants` 的子类，声明 `food_cost`、加载 `self.image`、设置 `self.rect.center = position`、设置 `self.row = get_row(position)`，并在模块级声明对应的 `pygame.sprite.Group()`（例如 `NewAnts = pygame.sprite.Group()`）。在 `main.py` 的点击处理里创建并加入该组，同时在主循环中绘制与更新。
- 生成蜜蜂示例：`Bees_group.add(Bees(n))`，其中 `n` 为 `'row1'..'row4'`（参见 `main.py` 的波次逻辑）。

# 集成要点与常见陷阱

- 代码依赖模块级可变状态（`GameState` 与精灵组），修改时要注意副作用，避免在局部文件重复声明相同全局名。
- 缺失资源文件会在 `pygame.image.load()` 抛出异常。若更改或添加资源，请同步更新 `assets/` 目录并在 README 记录新增资源路径。
- 主循环使用 `pygame.mouse.get_pressed()[0]` 直接检测左键；如引入自定义 UI，务必避免与现有点击逻辑冲突。

# 给 AI 代理的工作准则

- 修改范围要小且集中：修改游戏规则或精灵行为优先改 `object.py`，`main.py` 仅处理 UI/事件层变更。
- 保留现有公共名字（`GameState`、精灵组名、`get_row`、`row_y_dic`），以避免破坏主循环对它们的直接引用。
- 新增文件时请同时更新 `README.md`（记录运行/依赖/资源）以便开发者快速启动。

---
如果你希望我把这份说明同步到 `README.md`、或把它整理为英文/中英文双语版本，请告诉我你优先的目标，我会继续迭代。
---
If any section is unclear or you'd like conventions translated into Chinese, tell me which parts to expand or revise.