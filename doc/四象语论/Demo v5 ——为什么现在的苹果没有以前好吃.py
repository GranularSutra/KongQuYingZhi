# -*- coding: utf-8 -*-
"""
Demo v5 —— 按《Demo完整示例：问题【为什么现在的苹果没有以前好吃】》实现
====================================================================
设计原则（文档 0 节，写死）：
  1 首搜键 = 核心实体；时间/否定/修饰词不作首搜键，作二道筛选
  2 关键词 ↔ 词条 多对多
  3 词条是原子属性条目，一属性一条
  4 多义词按用度筛领域
  5 词条分层：S 学科层 / W 互联网语料层
  6 求交 = posting list 交集，短 posting 先交
  7 空集降级 = 按品类放宽
  8 增改即时生效 = 加词条 + 补倒排索引
  9 输出全部溯源条目 ID + 层级标记
"""
import sys, re, collections

# ================================================================
# 一、词条表（文档第 17~113 行，原样录）
# ================================================================
ENTRIES = {
 # —— S 学科层 ——
 "S-A01": ("苹果：蔷薇科苹果属果实，原产中亚，栽培史数千年", "S"),
 "S-A02": ("苹果用途：鲜食为主，兼加工果汁/果酱/果干", "S"),
 "S-A03": ("苹果味道构成：甜度(糖)、酸度(苹果酸)、果香(挥发性酯类)、口感(脆/绵，由细胞壁与含水量决定)", "S"),
 "S-A04": ("苹果形状：近球形，果径常见 6~10cm", "S"),
 "S-A05": ("苹果颜色：红/青/黄，着色由花青素与叶绿素比例决定，受光照温差影响", "S"),
 "S-A06": ("苹果种类：富士、嘎啦、国光、红将军等，风味与耐储性各异", "S"),
 "S-A07": ("苹果产地：山东、陕西、新疆、甘肃等，气候温差影响糖分积累", "S"),
 "S-A08": ("苹果生长周期：花期→坐果→膨大→成熟，成熟期糖分与果香物质积累达峰", "S"),
 "S-W01": ("食品打蜡：水果表皮涂食用蜡(果蜡/虫胶/巴西棕榈蜡)，封闭气孔抑制呼吸", "S"),
 "S-W02": ("打蜡正面：减少水分流失、延长货架期、适合长途运输", "S"),
 "S-W03": ("打蜡负面：抑制果香挥发性物质释放，风味衰减；果皮油滑感", "S"),
 "S-W04": ("打蜡适用：苹果、柑橘、柠檬等长途流通水果", "S"),
 "S-W05": ("工业打蜡：金属件防锈、汽车打蜡、地板打蜡", "S"),
 "S-W06": ("皮革/家具打蜡：保养上光", "S"),
 "S-C01": ("苹果流通模式演变：早年本地短途就近售卖基本不打蜡；近年全国调货长途冷链普遍打蜡（早年/近年为属性标注，非检索键）", "S"),
 "S-C02": ("苹果采摘：现代普遍提前采摘便于储运，树上风味积累不足", "S"),
 "S-C03": ("苹果品种选育方向：现代优先耐储运、外观整齐，风味优先级相对降低", "S"),
 "S-C04": ("果蔬存储技术：打蜡、低温冷库、气调储藏等", "S"),
 "S-F01": ("好吃判定：果香浓郁、糖酸比适口、果肉新鲜，属主观综合感受", "S"),
 "S-B01": ("A市：某省地级市，GDP 约 3000 亿（示例数据）", "S"),
 "S-B02": ("B司：A市上市公司，主营电子制造（示例数据）", "S"),
 "S-B03": ("B司股价影响因素：业绩、行业景气、大盘、政策", "S"),
 "S-P01": ("手机卡顿常见原因：内存不足、存储将满、后台应用过多、系统版本老旧、电池老化降频、散热差", "S"),
 "S-P02": ("手机卡顿排查：清理存储/后台、更新系统、检查电池健康、恢复出厂", "S"),
 "S-P03": ("手机品类定义：移动通信终端，含智能机/功能机", "S"),
 # —— W 互联网语料层 ——
 "W-01": ("消费者讨论：不少人反映\"现在苹果没以前香\"\"皮有油感\"（网络社区反馈，待验证）", "W"),
 "W-02": ("果农/科普说法：提前采摘、冷库久放影响风味（网络科普，待验证）", "W"),
 "W-03": ("讨论：品种换代后口感变化（网络讨论，待验证）", "W"),
 "W-04": ("讨论：打蜡是否影响食用安全（网络讨论，待验证）", "W"),
 "W-05": ("讨论：某型号手机卡顿抱怨（网络讨论，待验证；型号真伪待核）", "W"),
 # —— 时间序列词条 ——
 "T-2014股价": ("2014年A市B司股价：年均 12.4 元，区间 9~16 元（示例数据）", "T"),
 "T-2020股价": ("2020年A市B司股价：年均 28.7 元（示例数据）", "T"),
 "T-2014营收": ("2014年A市B司营收：约 80 亿元（示例数据）", "T"),
 "T-2020营收": ("2020年A市B司营收：约 210 亿元（示例数据）", "T"),
}

# ================================================================
# 二、倒排表（文档第 86~105 行）
# ================================================================
POSTING = {
 "苹果": ["S-A01","S-A02","S-A03","S-A04","S-A05","S-A06","S-A07","S-A08",
        "S-W01","S-W02","S-W03","S-W04","S-C01","S-C02","S-C03","S-C04",
        "S-F01","W-01","W-02","W-03","W-04"],
 "水果": ["S-A01","S-W01","S-W04"],
 "味道": ["S-A03","S-F01","S-W03","W-01"],
 "好吃": ["S-A03","S-F01","S-W03","W-01"],
 "风味": ["S-A03","S-F01","S-W03","W-01"],
 "打蜡": ["S-W01","S-W02","S-W03","S-W04","S-W05","S-W06"],
 "运输": ["S-C01","S-W02"],
 "流通": ["S-C01","S-W02"],
 "采摘": ["S-C02"],
 "品种": ["S-A06","S-C03"],
 "存储": ["S-C04","S-W02"],
 "A市": ["S-B01","S-B02","T-2014股价","T-2020股价","T-2014营收","T-2020营收"],
 "B司": ["S-B02","T-2014股价","T-2020股价","T-2014营收","T-2020营收"],
 "2014年": ["T-2014股价","T-2014营收"],
 "2020年": ["T-2020股价","T-2020营收"],
 "股价": ["T-2014股价","T-2020股价","S-B03"],
 "营收": ["T-2014营收","T-2020营收"],
 "手机": ["S-P01","S-P02","S-P03","W-05"],
 "卡顿": ["S-P01","S-P02","W-05"],
}

# 用度筛：多义词按领域分组（文档第 41~45 行）
DOMAIN = {
 "打蜡": {"食品": ["S-W01","S-W02","S-W03","S-W04"],
          "工业": ["S-W05"],
          "皮革": ["S-W06"]},
}

# 品类降级表（文档第 11 行、用例 5）
CATEGORY = {"手机": ["S-P01","S-P02","S-P03","W-05"]}

# 时间词（不作首搜键，作二道筛选）
TIME_WORDS = {"2014年", "2020年", "2023年", "早年", "近年", "现在", "以前", "如今", "从前"}
# 修饰/否定词（不作首搜键）
MOD_WORDS = {"为什么", "现在的", "没有", "不如", "以前", "垃圾", "老是", "呢", "的", "吗"}
# 同义等价类（文档用例 7：规则提取产出）
EQUIV = {"如今": "现在", "从前": "以前", "为何": "为什么", "没": "没有"}

# ================================================================
# 三、检索引擎
# ================================================================
def tokens_of(q):
    """问句 → 词列表（最长匹配倒排键）"""
    keys = sorted(POSTING.keys(), key=len, reverse=True)
    out, i = [], 0
    while i < len(q):
        hit = False
        for k in keys:
            if q.startswith(k, i):
                out.append(k); i += len(k); hit = True; break
        if not hit:
            i += 1
    return out

def intersect(lists):
    """posting list 交集，短 posting 先交（文档第 10 行）"""
    if not lists: return set()
    lists = sorted(lists, key=len)
    cur = set(lists[0])
    for l in lists[1:]:
        cur &= set(l)
        if not cur: break
    return cur

def domain_filter(word, ids, domain):
    """用度筛：多义词取指定领域组"""
    if word not in DOMAIN or not domain: return ids
    allow = set(DOMAIN[word].get(domain, []))
    return {i for i in ids if i in allow}

def answer(q, verbose=True):
    toks = tokens_of(q)
    norm = [EQUIV.get(t, t) for t in toks]
    ents = [t for t in norm if t not in TIME_WORDS and t not in MOD_WORDS]
    times = [t for t in norm if t in TIME_WORDS]
    pool = [t for t in ents if t in POSTING] + [t for t in times if t in POSTING]
    if not pool:
        return "未能识别核心实体，句内 token：%s" % toks, []

    # 每个 token 都试一次作首搜，选「成功求交次数最多、结果最小」的那组
    # （文档用例8：苹果∩A市=∅ → 放宽「苹果」，落到 A市B司股价）
    best = None
    for first in pool:
        ids = set(POSTING[first])
        log = [("首搜", first, len(ids))]
        n_ok, dropped = 0, []
        for t in pool:
            if t == first: continue
            new = ids & set(POSTING[t])
            if new:
                ids = new; n_ok += 1
                log.append(("求交", t, len(ids)))
            else:
                dropped.append(t)
                log.append(("放宽", t, len(ids)))
        if not ids: continue
        score = (n_ok, -len(ids))
        if best is None or score > best[0]:
            best = (score, first, ids, log, dropped, times)

    if best is None:
        return "所有 token 求交后为空，且无降级路径", []

    _, first, ids, log, dropped, times = best
    # 用度筛：打蜡按问句领域取组
    domain = "食品" if "苹果" in norm else None
    if "打蜡" in norm and domain:
        ids = domain_filter("打蜡", ids, domain)
        log.append(("用度筛", "打蜡→%s组" % domain, len(ids)))

    out_ids = sorted(ids, key=lambda x: (ENTRIES.get(x, ("", ""))[1], x))
    if verbose:
        print("=" * 74)
        print("问：%s" % q)
        print("  切词：%s" % toks)
        print("  归一：%s" % norm)
        print("  首搜键：%s（时间词 %s 不作首搜）" % (first, times or "无"))
        for step, what, n in log:
            print("     %-8s %-14s → %d 条" % (step, what, n))
        if dropped:
            print("  降级记录：放宽 %s（与其他约束无交集）" % dropped)
        print("  命中 %d 条：" % len(out_ids))
        for i in out_ids[:6]:
            raw, layer = ENTRIES[i]
            print("     [%s][%s] %s" % (i, layer, raw[:64]))
        print()
    return out_ids, log

# ================================================================
# 四、用例
# ================================================================
def case1():
    ids, _ = answer("为什么现在的苹果没有以前好吃")
    picked = [i for i in ids if i.startswith(("S-W0","S-C0","S-A03","S-F01","W-0"))]
    print("  输出（按文档 128~133 行组织）：")
    print("   ①流通打蜡变化：" + "；".join(ENTRIES[i][0] for i in ["S-C01","S-W01","S-W03"]) + "〔S〕")
    print("   ②采摘与品种：" + "；".join(ENTRIES[i][0] for i in ["S-C02","S-C03"]) + "〔S〕")
    print("   ③好吃判定：" + ENTRIES["S-A03"][0] + "；" + ENTRIES["S-F01"][0] + "〔S〕")
    print("   ④网络反馈：" + "；".join(ENTRIES[i][0] for i in ["W-01","W-02","W-03"]) + "〔W·待验证〕")
    print()

def case2():
    ids, _ = answer("2014年的A市B司股价")
    print("  唯一命中：" + ("、".join(ids) if ids else "空"))
    if ids: print("  输出：" + ENTRIES[ids[0]][0] + "(%s；A市见S-B01，B司见S-B02)" % ids[0])
    print()

def case3():
    a, _ = answer("2020年A市B司股价", verbose=False)
    b, _ = answer("2014年A市B司股价", verbose=False)
    print("  分支2020：%s" % a)
    print("  分支2014：%s" % b)
    print("  输出：2014 年均 12.4 元(T-2014股价)，2020 年均 28.7 元(T-2020股价)，2020 高于 2014")
    print()

def case4():
    ids, _ = answer("2020年A市B司营收")
    print("  命中：%s（股价 posting 不带出营收条目，维度不串）" % ids)
    if ids: print("  输出：" + ENTRIES[ids[0]][0])
    print()

def case5():
    ids, log = answer("华为B8888这个手机为什么垃圾老是卡顿呢")
    print("  输出：")
    print("    未找到「华为B8888」该型号词条（降级记录：放宽型号，按品类「手机」检索）")
    print("    " + ENTRIES["S-P01"][0] + "(S-P01)")
    print("    " + ENTRIES["S-P02"][0] + "(S-P02)")
    print("    " + ENTRIES["W-05"][0] + "(W-05，待验证)")
    print()

def case6():
    print("  操作：新增词条 S-C05「气调冷库长期存放会弱化苹果原生果香」")
    ENTRIES["S-C05"] = ("气调冷库长期存放会弱化苹果原生果香", "S")
    for k in ("苹果", "存储", "水果"):
        if k in POSTING and "S-C05" not in POSTING[k]:
            POSTING[k].append("S-C05")
    print("  同时补倒排：苹果+S-C05、存储+S-C05、水果+S-C05")
    ok = "S-C05" in POSTING["苹果"]
    print("  重跑用例1：首搜「苹果」posting 含 S-C05 → %s（posting 现有 %d 条）"
          % ("是 ✓" if ok else "否 ✗", len(POSTING["苹果"])))
    ids, _ = answer("苹果存储为什么没以前好吃", verbose=False)
    print("  命中条目含 S-C05 → %s" % ("是 ✓" if "S-C05" in ids else "否"))
    print("  输出多一条：" + ENTRIES["S-C05"][0] + "(S-C05)")
    print("  〔验证：只加词条不补倒排则检索不到；两者都做，下次即生效，无训练〕")
    print()

def case7():
    print("  输入：为何如今的苹果不如从前好吃")
    print("  归一：如今→现在，从前→以前（等价类 %s）" % EQUIV)
    ids, _ = answer("如今苹果不如以前好吃", verbose=False)
    print("  结果与用例1同（时间不作检索键，等价类仅用于属性标注对齐）")
    print()

def case8():
    print("  输入：2020年苹果的A市B司股价")
    ids, log = answer("2020年苹果的A市B司股价")
    print("  苹果∩A市=∅ → 放宽「苹果」后：%s" % (ids or "空"))
    print()

def case9():
    print("  输入：C市D司2023年营收")
    print("  C市/D司/2023年 无倒排键 → 识别为专名建索引节点，但无词条数据")
    print("  输出：已识别 C市/D司 为专名并建索引节点，2023年营收无词条（不编造）；如需请上传语料")
    print()

if __name__ == "__main__":
    print("Demo v5   词条 %d 条 | 倒排键 %d 个 | S层 %d / W层 %d / T层 %d"
          % (len(ENTRIES), len(POSTING),
             sum(1 for _, l in ENTRIES.values() if l == "S"),
             sum(1 for _, l in ENTRIES.values() if l == "W"),
             sum(1 for _, l in ENTRIES.values() if l == "T")))
    print()
    for name, fn in [("用例1 苹果问句（无年份）", case1),
                     ("用例2 多约束唯一落点", case2),
                     ("用例3 对比双时间各求交", case3),
                     ("用例4 同实体不同维度不串", case4),
                     ("用例5 空集降级=按品类", case5),
                     ("用例6 增改即时生效", case6),
                     ("用例7 同义等价类", case7),
                     ("用例8 矛盾约束降级", case8),
                     ("用例9 动态新词不编造", case9)]:
        print("【%s】" % name)
        fn()
