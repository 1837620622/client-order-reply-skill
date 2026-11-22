#!/usr/bin/env python3
"""给客户的回复做 AI 味体检。用法：python3 ai_lint.py "回复内容"  或  echo 回复 | python3 ai_lint.py
只是提示，不是判决。报出来的地方要自己读一遍再决定改不改。"""
import re, sys, statistics

args = sys.argv[1:]
prev = []
while "--prev" in args:
    k = args.index("--prev"); prev.append(args[k + 1]); del args[k:k + 2]
text = " ".join(args) if args else sys.stdin.read()
text = text.strip()
hits = []

def flag(level, msg):
    hits.append((level, msg))

# 标点
bad_punct = "、；：——（）()“”\"'‘’！!…;:"
found = sorted({c for c in text if c in bad_punct})
if found:
    flag("必改", "出现不该用的标点 " + " ".join(found))
if re.search(r"[A-Za-z]\.|\.[A-Za-z]", text) and re.search(r"\.(dta|xlsx|csv|stp|pfd|m|py)\b", text):
    flag("必改", "文件后缀带了点号，写成 dta文件 这种")
if re.search(r"[\U0001F300-\U0001FAFF]", text):
    flag("必改", "有表情")

# 客服腔和书面词
words = {
    "必改": ["您", "亲", "宝", "老板", "我们", "团队", "工作室", "为您", "感谢", "期待", "希望对你有帮助", "如有需要",
            "请注意", "提醒一下", "非常理解", "一站式", "量身定制", "性价比", "进行", "实现", "针对", "基于", "从而",
            "进而", "此外", "综上", "总的来说", "换句话说", "值得一提", "首先", "其次", "最后", "第一", "第二",
            "一方面", "不仅", "而是", "完全没问题", "绝对", "保证", "包过", "100%", "咋们", "你导"],
    "留意": ["确实", "其实", "主要是", "关键是", "核心是", "本质上", "费用", "相应", "整体", "环节", "层面", "维度",
            "确保", "提供", "完成", "放心", "省心", "一步到位", "全方位", "高效", "专业", "优质", "尽力", "好好想想",
            "这样一来", "也就", "所以", "因此", "以便", "相关"],
}
for level, ws in words.items():
    got = [w for w in ws if w in text]
    if got:
        flag(level, "用词 " + " ".join(got))

# 开头
if re.match(r"^(好的(?!呢)|明白|当然|收到|没关系，?.{0,6}确实|你好|您好)", text):
    flag("必改", "开头是客服式接话，换成 没事，理解的 / 行 / 可以的 / 这个好办 / 直接进判断")

# 开头和上一条重复
openers = ["好的呢", "好嘞", "好的", "行呀", "可以的", "没问题呀", "没问题", "这个好办", "哈哈", "收到", "没事", "行", "可以"]
def opener(t):
    t = t.strip()
    for o in openers:
        if t.startswith(o):
            return o
    return t[:3]
for p in prev:
    if p.strip() and opener(p) == opener(text):
        flag("必改", f"开头 {opener(text)} 和上一条一样，换个开头或者直接从客户的话接")

# 口头禅过密
for w, n in [("这块", 2), ("直接", 2), ("我这边", 1), ("你那边", 1), ("咱们", 1), ("一下", 2), ("我会", 1), ("我可以", 1)]:
    c = text.count(w)
    if c > n:
        flag("留意", f"{w} 出现 {c} 次，最多 {n} 次")

# 送客式结尾
if re.search(r"(你先考虑|想好了|定了随时|随时找我|随时联系|有需要再)", text[-30:]):
    flag("留意", "结尾像送客，客户没说不做的话换成一句话能回的下一步")

# 排比和对称
sents = [s for s in re.split(r"[。？?]", text) if s.strip()]
clauses = [c for c in re.split(r"[，。？?]", text) if c.strip()]
if len(clauses) >= 4:
    lens = [len(c) for c in clauses]
    if statistics.pstdev(lens) < 2.5:
        flag("留意", f"分句长短太平均（{lens}），读着像排好的，拆一两个短的出来")
if re.search(r"(，[^，。]{2,8}){3}，还有", text) or text.count("，还有") > 1:
    flag("留意", "三连并列，只挑最要紧的一两件说")
if re.search(r"(既|又|还能).{2,10}(又|还|也).{2,10}(还|也)", text):
    flag("留意", "既又还 排比")
if re.search(r"(小了|少了|多了).{0,4}(也|就).{0,6}(下来|上去|少|多)", text):
    flag("留意", "X了Y也Z 这种因果对称句，AI 很爱写，改成直说")

# 问句
q = text.count("？") + text.count("?") + len(re.findall(r"(吗|呢|没有|不)[。]?$", text))
if text.count("？") + text.count("?") > 1:
    flag("留意", "问号超过一个，一次只问一件")

n = len(re.sub(r"\s", "", text))
print(f"字数 {n}，句子 {len(sents)}，分句 {len(clauses)}")
if not hits:
    print("没查出明显 AI 味。机器查不出语气，最后还要自己念一遍，像不像本人在微信上打的。")
for level, msg in hits:
    print(f"[{level}] {msg}")
