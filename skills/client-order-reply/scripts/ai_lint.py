#!/usr/bin/env python3
"""给客户的回复做 AI 味体检。
用法  python3 ai_lint.py "回复内容" [--prev "上一条"] [--prev "上上条"]
      echo 回复 | python3 ai_lint.py
只是提示，不是判决。报出来的地方自己读一遍再决定怎么改。"""
import re
import sys

args = sys.argv[1:]
prev = []
while "--prev" in args:
    k = args.index("--prev")
    if k + 1 < len(args):
        prev.append(args[k + 1])
    del args[k:k + 2]
text = (" ".join(args) if args else sys.stdin.read()).strip()
prev = [p.strip() for p in prev if p.strip()]
hits = []


def flag(level, msg):
    hits.append((level, msg))


# 标点，只允许 ，。？ 和必要的数字字母（用户 2026-11-23）
# 放行 版本号小数点 15.1，数字后的 %，ASCII 术语内部的连字符和下划线 PSM-DID
def is_allowed(i, c):
    if c in "，。？" or c.isspace():
        return True
    if "\u4e00" <= c <= "\u9fff" or c.isascii() and c.isalnum():
        return True
    left = text[i - 1] if i > 0 else ""
    right = text[i + 1] if i + 1 < len(text) else ""
    if c == "." and left.isdigit() and right.isdigit():
        return True
    if c == "%" and left.isdigit():
        return True
    if c in "-_+" and left.isascii() and left.isalnum() and right.isascii() and right.isalnum():
        return True
    return False


bad = sorted({c for i, c in enumerate(text) if not is_allowed(i, c)})
if bad:
    flag("必改", "出现不该用的标点或符号 " + " ".join(bad) + "，只用 ，。？")
if re.search(r"\.(dta|xlsx|xls|csv|stp|step|pfd|slx|mdl|m|py|do|docx|pdf)(?![A-Za-z0-9])", text, re.I):
    flag("必改", "文件后缀带了点号，写成 dta文件 这种")

# 用词
words = {
    "必改": ["您", "亲", "宝", "老板", "家人们", "我们", "团队", "工作室", "同事", "为您", "感谢", "期待", "希望对你有帮助",
            "如有需要", "请注意", "提醒一下", "非常理解", "一站式", "量身定制", "性价比", "进行", "实现", "针对", "基于",
            "从而", "进而", "此外", "综上", "总的来说", "换句话说", "值得一提", "首先", "其次", "一方面",
            "不仅", "而是", "完全没问题", "绝对", "保证", "包过", "100%", "咋们", "你导", "心里有个数", "预算多少",
            "多少预算", "能接受多少", "你出多少", "思路很对", "想法很好", "问得好", "考虑得很周到", "很专业", "太对了",
            "说得对", "留v", "加微信", "加个微信", "微信细聊"],
    "留意": ["确实", "其实", "主要是", "关键是", "核心是", "本质上", "费用", "相应", "整体", "环节", "层面", "维度",
            "确保", "提供", "完成", "放心", "省心", "一步到位", "全方位", "高效", "优质", "尽力", "好好想想",
            "这样一来", "最晚什么时候", "所以", "因此", "以便", "相关"],
}
if re.search(r"(^|[，。？])(第一|第二|第三|最后)[，是]", text):
    flag("必改", "第一第二最后 这种列条结构，拆成自然的话")
for level, ws in words.items():
    got = [w for w in ws if w in text]
    if got:
        flag(level, "用词 " + " ".join(got))

if re.search(r"什么时候要([，。？]|$)", text):
    flag("留意", "什么时候要 是冷问，换成 方便的话跟我说下大概什么时候要用")

# 说话留余地（用户 2026-11-23）
hard = [w for w in ["我建议", "你应该", "一定要", "肯定是"] if w in text]
if hard:
    flag("留意", "说得太肯定 " + " ".join(hard) + "，换成 我觉得，要不，可以考虑，可能，一般，应该能")

# 开头
if re.match(r"^(图收到了|收到|好的|明白了|看了一下)", text):
    flag("必改", "开头是确认废话，第一句直接切重点（用户 2026-11-23）")
elif re.match(r"^(明白|当然|没关系，?.{0,6}确实|你好|您好)", text):
    flag("必改", "开头是客服式接话，从客户刚说的那句接，或者直接说判断")

openers = ["好的呢", "好嘞", "好的", "行呀", "可以的", "没问题呀", "没问题", "这个好办", "哈哈", "收到啦", "收到",
           "没事", "行", "可以"]


def opener(t):
    for o in openers:
        if t.startswith(o):
            return o
    return t[:3]


def particles(t):
    return frozenset(c for c in "呀呢哈嘞啦吧哦嘛" if c in t)


op, pt = opener(text), particles(text)
for p in prev:
    if opener(p) == op:
        flag("必改", f"开头 {op} 和前几条一样，换个开头或者直接从客户的话接")
        if particles(p) == pt:
            flag("留意", "语气没交叉，和前几条的语气词组合，句式开头都一样，按客户这条的情绪换成暖，热情或平实专业")
        break

# 祝福和内容重复
bless = ["一路发", "沾点喜气", "沾沾光", "沾点光", "顺顺利利", "图个吉利"]
for p in prev:
    same = [b for b in bless if b in p and b in text]
    if same:
        flag("必改", "祝福 " + " ".join(same) + " 前几条用过，换个说法或者这条不带")
    pc = re.sub(r"[，。？\s]", "", p)
    tc = re.sub(r"[，。？\s]", "", text)
    rep = {tc[i:i + 10] for i in range(len(tc) - 9) if tc[i:i + 10] in pc}
    if rep:
        flag("留意", "和前几条有整段重复 " + " ".join(sorted(rep)[:3]) + "，说过的不再说")

# 口头禅过密
for w, n in [("这块", 2), ("直接", 2), ("我这边", 1), ("你那边", 1), ("你这边", 1), ("咱们", 1), ("一下", 2),
             ("我会", 1), ("我可以", 1)]:
    c = text.count(w)
    if c > n:
        flag("留意", f"{w} 出现 {c} 次，最多 {n} 次")
c = sum(text.count(x) for x in "呀呢哈嘞")
if c > 2:
    flag("留意", f"语气词 呀呢哈嘞 共 {c} 个，一段最多2个")

# 送客式结尾
if re.search(r"(你先考虑|想好了|定了随时|随时联系)", text[-30:]):
    flag("留意", "结尾像送客，客户没说不做的话换成一句话能回的下一步")

# 排比和对称
if re.search(r"(，[^，。]{2,8}){3}，还有", text) or text.count("，还有") > 1:
    flag("留意", "三连并列，只挑最要紧的一两件说")
if re.search(r"(既|又|还能).{2,10}(又|还|也).{2,10}(还|也)", text):
    flag("留意", "既又还 排比")
if re.search(r"(小了|少了|多了).{0,4}(也|就).{0,6}(下来|上去|少|多)", text):
    flag("留意", "X了Y也Z 这种因果对称句，改成直说")
if text.count("？") > 1:
    flag("留意", "问号超过一个，一次只问一件")

# 问句位置随机（用户 2026-11-23）
def ends_with_q(t):
    last = [s for s in re.split(r"(?<=[。？])", t.strip()) if s.strip()]
    last = last[-1] if last else ""
    return "？" in last or bool(re.search(r"(吗|么|没有|呢)[。？]?$", last))


if prev and ends_with_q(text) and all(ends_with_q(p) for p in prev):
    flag("留意", "这条和前几条都以问句结尾，问句换到开头或中间，或者这条用一个动作收")

# 长短和前几条太接近（不设字数标准，只比相对长短）
n = len(re.sub(r"\s", "", text))
pl = [len(re.sub(r"\s", "", p)) for p in prev]
if pl and all(abs(x - n) <= max(8, n * 0.2) for x in pl):
    flag("留意", "长短和前几条差不多，按客户这条问了什么定，长短自然交叉")

if not hits:
    print("没查出明显 AI 味。机器查不出语气，最后自己念一遍，像不像本人在手机上打的。")
for level, msg in hits:
    print(f"[{level}] {msg}")
