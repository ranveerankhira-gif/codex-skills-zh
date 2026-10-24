# 长期沉淀协议

每次商品调研结束都执行本协议，无论结果是成功、失败还是受阻。记录保存在 Skill 自身的 `state/` 目录；脚本拒绝写到 Skill 目录之外。`context` 是只读操作，不创建目录或写锁。

## 数据层

- `raw-research.jsonl`：所有可解析调研记录的追加式原始层。门控失败仍保留，不代表可信。
- `preference-events.jsonl`：用户偏好事件。区分 `explicit`、`repeated_inference`、`single_context`，不覆盖旧事件。
- `category-findings.jsonl`：所有品类发现；每条带 `raw` 或 `trusted` 层级。
- `receipts.jsonl`：每次写入的校验结果、晋升数量、去重和未晋升原因。
- `pending-categories.jsonl`：未覆盖品类的待完善记录。

价格、库存、配送和店铺状态始终是易变事实，历史记录只能做检索线索。品类质量模式必须保留证据日期和来源；旧结论不能替代当前核验。

## 调研记录最小结构

输入为 UTF-8 JSON 对象：

```json
{
  "schema_version": 3,
  "session_id": "唯一会话标识",
  "researched_at": "ISO 8601 时间",
  "category": "apparel_textiles",
  "branded_or_modelled": true,
  "request": {"summary": "用户需求摘要"},
  "queries": [
    {"role": "transaction", "platform": "平台名", "query": "查询词", "status": "success", "url": "https://...", "failure_reason": ""}
  ],
  "gates": {
    "requirement": {"status": "PASS", "reason": "..."},
    "web_coverage": {"status": "PASS", "reason": "..."},
    "identity": {"status": "PASS", "reason": "..."},
    "review_completeness": {"status": "PASS", "reason": "..."},
    "manipulation": {"status": "PASS", "reason": "..."},
    "complaint_severity": {"status": "PASS", "reason": "..."},
    "seller": {"status": "PASS", "reason": "..."},
    "price_value": {"status": "PASS", "reason": "..."},
    "publication": {"status": "PASS", "reason": "由程序复核"}
  },
  "candidates": [],
  "preference_events": [],
  "category_findings": [],
  "pending_category": null
}
```

最终候选的 `candidates` 至少包含 `id`、`name`、`finalist`、`identity`、`review_coverage`、`complaint_coverage`、`authenticity`、`seller_risk` 和 `complaints`。评论覆盖使用 `access_mode`、`access_result`、`access_attempts`、`reported_negative_count`、`accessible_negative_count`、`read_negative_count`、`limitations`、`source_urls`；版本 3 另要求 `negative_reviews`、`reader_evidence`、`filter_verified`、`pages_read`、`exhausted`、`adapter_version` 和 `error_code`，详细规则见 [评论访问与差评读取](review-access.md)、[淘宝与天猫官方客户端查验](taobao-tmall-official-client.md) 与 [OpenCLI 京东评论读取器](opencli-review-reader.md)。`access_mode` 允许 `official_client`；该模式与 `authorized_session` 一样需要本任务授权记录。至少需要两个独立域名的评论或体验证据。商品投诉和 `seller_risk.complaint_coverage` 分别使用 `reported_count`、`accessible_count`、`read_count`、`limitations`，且已读数必须与逐条投诉记录数一致。身份使用 `matched`、`unique`、`conflict` 或 `unknown`。真实性使用 `credible`、`mixed`、`manipulated` 或 `unknown`。商铺风险使用 `acceptable`、`mixed`、`high` 或 `unknown`，并附来源 URL。

每条投诉包含 `source_url`、`date`、`variant`、`summary`、`evidence`、`seller_response`、`resolved`、`severity`、`scope`；`scope` 区分 `product` 与 `seller`。未知字段写 `unknown`，不得编造。

## 自动晋升规则

原始调研总是先写入。结构校验失败的记录不能晋升。只有以下门全部为 `PASS` 时，品类发现才可能进入 `trusted`：`web_coverage`、`identity`、`review_completeness`、`manipulation`、`complaint_severity`。发现本身还必须至少有两个不同平台、两个来源 URL、有效证据日期，并声明 `high` 置信度。否则保留为 `raw` 并在回执说明原因。

偏好全部自动追加，但优先级为 `explicit` > `repeated_inference` > `single_context`。冲突事件并存，后续调研不得让推断覆盖明确表达。脚本拒绝保存完整地址、账号、订单号、电话、身份证、支付信息和收礼人姓名等字段。

当前价格、库存、配送和店铺状态通过 `dynamic_facts` 记录 `price`、`inventory`、`shipping`、`store_status`。每条绑定 `candidate_id`，附 `source_url`、`verified_at` 和 `value`；一个商品的证据不能替另一个商品通过。强推荐要求每个最终候选四类证据均有效且在72小时内。价格另需正数 `amount`、`currency`、`price_type`（`listed`、`checkout`、`member`、`coupon`）和 `current_offer: true`。金额所对应的商品变体和优惠资格必须明确。

`status` 支持 `verified`、`n_a`、`unknown`、`historical`、`restricted`。后三类是有效记录但不会通过实时核验；历史价使用实际证据日期，另可记 `observed_at` 表示本次看到页面的时间。`n_a` 只用于确实不适用并附 `reason`，不能把读不到价格写成不适用。读取商品页内嵌数据也不能绕过账号或风控限制。

条件推荐要求库存、配送、店铺状态当前可核对；价格可受限，但须说明结算前提。每个选中候选须有 `conditional_basis` 和 `purchase_checks`（具体规则见 evidence-and-evaluation.md），例：

```json
{
  "conditional_basis": "已核实具体变体、适配与退换；负面评论正文受限，质量置信度有限",
  "purchase_checks": {
    "variant": {"status": "PASS", "reason": "商品页确认目标规格SKU", "source_urls": ["https://shop.example/item"]},
    "seller_and_returns": {"status": "PASS", "reason": "明确卖家主体和退换条件", "source_urls": ["https://shop.example/item"]},
    "hard_constraints": {"status": "PASS", "reason": "逐项核对实际适配、预算与到货期限", "source_urls": ["https://shop.example/spec"]},
    "safety": {"status": "N/A", "reason": "普通非安全关键商品，无额外安全功效要求"}
  }
}
```

示例值不能原样充当证据。硬条件不满足或证据不够就写 `FAIL`/`BLOCKED`；额外实质检查（如 `fit`、`delivery`）同样不能被忽略。`recommendation` 包含 `mode`、存在且唯一的 `candidate_ids` 和条件推荐的非空 `conditions`。用户坚持完整评论审计时，在 `request.require_full_review_before_recommendation` 标为 `true`。程序输出的 `publication` 是高置信度发布门；`conditional_eligible` 与 `conditional_reasons` 单独表示条件推荐资格。`schema_version: 1` 和 `2` 的旧记录仍可校验和追加保存，但缺少版本 3 的筛选、分页和逐条评论证据时不会自动取得更高置信度；新调研使用版本 3。

开始新调研时读取长期上下文：

```powershell
python scripts/shopping_memory.py context --category <category>
```

该命令按偏好证据优先级解析当前画像，并只返回同品类 `trusted` 经验；同优先级的不同明确偏好会标为 `conflict`，不能擅自选一个。历史动态事实仍必须重新核验。

## 写入命令

先校验：

```powershell
python scripts/shopping_memory.py validate --input <record.json>
```

再写入：

```powershell
python scripts/shopping_memory.py commit --input <record.json>
```

也可把 JSON 通过标准输入传给 `--stdin`。命令会输出 JSON 回执。若返回码非零或回执含错误，向用户说明原始记录是否已写入、哪些项目没有晋升；不得静默跳过。

同一 `session_id` 使用内容哈希去重：相同内容重复提交不再写原始层；内容改变则追加 `_revision`、`_record_hash` 和新校验结果，保留旧版。不必为每次补证据换会话编号。只有 `raw_written: true` 才能说本次原始记录已新增，`raw_duplicate: true` 必须说明是重复。写入权限失败时保留工作区JSON并准确报告；若任务授权允许，走正式权限申请，不反复调用同一失败命令。

流程经验写入 Skill 引用文档，商品质量发现才放 `category_findings`。一次礼物的收礼人体型不是用户永久偏好；价格、SKU、当天配送和风控码只作带日期的案例，不推广成长期推荐规则。
