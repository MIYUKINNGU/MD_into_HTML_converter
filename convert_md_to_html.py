# Markdownからhtmlにするコードを作るよ
# 私のブログを楽に書けるようにするために作るよ
# ブログが雑い作りすぎるというか技術力なさ過ぎってのは言っちゃだめよ
# 構文解析が必須だよ(泣)
from collections import deque

class Automaton:
    def __init__(self, label=""):
        self.label = label
        self.nexts = deque([])
        self.conds = deque([])

    def add_next(self, next, cond):
        self.nexts.append(next)
        self.conds.append(cond)
    
    def add_left_next(self, next, cond):
        self.nexts.appendleft(next)
        self.conds.appendleft(cond)
    
    def get_next(self, char):
        l = []
        for i in range(len(self.nexts)):
            if self.conds[i](char):
                l.append(self.nexts[i])
        if len(l) == 0:
            return None
        return l[0]

def does_accept_automaton(automaton, text, does_cond_includes_token=False):
    d = {}
    a = automaton
    for c in text:
        a = a.get_next(c)
        if a.label in d:
            d[a.label].append(c)
        else:
            d[a.label] = [c]
    
    nd = {}
    for v in d:
        nd[v] = "".join(d[v])
    
    if "" not in nd:
        nd[""] = ""
    
    if a.label == "success":
        return True, nd
    if does_cond_includes_token and a.label == "token":
        nd["success"] = ""
        return True, nd
    return False, nd

class Automaton_Conditions:
    @staticmethod
    def Always(c):
        return True
    
    @staticmethod
    def Match(char):
        return lambda c: c == char
    
    @staticmethod
    def Includes(chars):
        return lambda c: c in set(chars)
    
    @staticmethod
    def Not(fn):
        return lambda c: not fn(c)

class Automatons:
    @staticmethod
    def recursive(label=""):
        A0 = Automaton(label)
        A0.add_next(A0, Automaton_Conditions.Always)
        return A0
    
    @staticmethod
    def unordered_list_object():
        A0 = Automaton() # start at
        A1 = Automaton("token") # -/*/+
        A2 = Automaton("token") # space
        success = Automatons.recursive("success") # success
        fail = Automatons.recursive("fail") # fail
        A0.add_next(A1, Automaton_Conditions.Includes(["-", "*", "+"]))
        A0.add_next(fail, Automaton_Conditions.Always)
        A1.add_next(A2, Automaton_Conditions.Match(" "))
        A1.add_next(fail, Automaton_Conditions.Always)
        A2.add_next(success, Automaton_Conditions.Always)
        return A0
    
    @staticmethod
    def header1():
        A0 = Automaton() # start at
        A1 = Automaton("token") # #
        A2 = Automaton("token") # space
        success = Automatons.recursive("success") # success
        fail = Automatons.recursive("fail") # fail
        A0.add_next(A1, Automaton_Conditions.Match("#"))
        A0.add_next(fail, Automaton_Conditions.Always)
        A1.add_next(A2, Automaton_Conditions.Match(" "))
        A1.add_next(fail, Automaton_Conditions.Always)
        A2.add_next(success, Automaton_Conditions.Always)
        return A0
    
    @staticmethod
    def header2():
        A0 = Automaton() # start at
        A1 = Automaton("token") # #
        A2 = Automaton("token") # #
        A3 = Automaton("token") # space
        success = Automatons.recursive("success") # success
        fail = Automatons.recursive("fail") # fail
        A0.add_next(A1, Automaton_Conditions.Match("#"))
        A0.add_next(fail, Automaton_Conditions.Always)
        A1.add_next(A2, Automaton_Conditions.Match("#"))
        A1.add_next(fail, Automaton_Conditions.Always)
        A2.add_next(A3, Automaton_Conditions.Match(" "))
        A2.add_next(fail, Automaton_Conditions.Always)
        A3.add_next(success, Automaton_Conditions.Always)
        return A0
    
    @staticmethod
    def header3():
        A0 = Automaton() # start at
        A1 = Automaton("token") # #
        A2 = Automaton("token") # #
        A3 = Automaton("token") # #
        A4 = Automaton("token") # space
        success = Automatons.recursive("success") # success
        fail = Automatons.recursive("fail") # fail
        A0.add_next(A1, Automaton_Conditions.Match("#"))
        A0.add_next(fail, Automaton_Conditions.Always)
        A1.add_next(A2, Automaton_Conditions.Match("#"))
        A1.add_next(fail, Automaton_Conditions.Always)
        A2.add_next(A3, Automaton_Conditions.Match("#"))
        A2.add_next(fail, Automaton_Conditions.Always)
        A3.add_next(A4, Automaton_Conditions.Match(" "))
        A3.add_next(fail, Automaton_Conditions.Always)
        A4.add_next(success, Automaton_Conditions.Always)
        return A0
    
    @staticmethod
    def bold_token():
        A0 = Automatons.recursive() # start at
        A1 = Automaton("token") # *
        A2 = Automaton("token") # *
        success = Automatons.recursive("success") # success
        A0.add_left_next(A1, Automaton_Conditions.Match("*"))
        A1.add_next(A2, Automaton_Conditions.Match("*"))
        A1.add_next(A0, Automaton_Conditions.Always)
        A2.add_next(success, Automaton_Conditions.Always)
        return A0
    
    @staticmethod
    def delete_token():
        A0 = Automatons.recursive() # start at
        A1 = Automaton("token") # ~
        A2 = Automaton("token") # ~
        success = Automatons.recursive("success") # success
        A0.add_left_next(A1, Automaton_Conditions.Match("~"))
        A1.add_next(A2, Automaton_Conditions.Match("~"))
        A1.add_next(A0, Automaton_Conditions.Always)
        A2.add_next(success, Automaton_Conditions.Always)
        return A0
    
    @staticmethod
    def underline_token():
        A0 = Automatons.recursive() # start at
        A1 = Automaton("token") # _
        A2 = Automaton("token") # _
        success = Automatons.recursive("success") # success
        A0.add_left_next(A1, Automaton_Conditions.Match("_"))
        A1.add_next(A2, Automaton_Conditions.Match("_"))
        A1.add_next(A0, Automaton_Conditions.Always)
        A2.add_next(success, Automaton_Conditions.Always)
        return A0
    
    @staticmethod
    def italic_token():
        A0 = Automatons.recursive() # start at
        A1 = Automaton("token") # */_
        success = Automatons.recursive("success") # success
        A0.add_left_next(A1, Automaton_Conditions.Includes(["*", "_"]))
        A1.add_next(success, Automaton_Conditions.Always)
        return A0
    
    @staticmethod
    def hyperlink_text():
        A0 = Automatons.recursive() # start at
        A1 = Automaton("token") # [
        A2 = Automatons.recursive("title")
        A3 = Automaton("token") # ]
        success = Automatons.recursive("success")
        A0.add_left_next(A1, Automaton_Conditions.Match("["))
        A1.add_next(A2, Automaton_Conditions.Always)
        A2.add_left_next(A3, Automaton_Conditions.Match("]"))
        A3.add_next(success, Automaton_Conditions.Always)
        return A0
    
    @staticmethod
    def hyperlink_link():
        A0 = Automaton() # start at
        A1 = Automaton("token") # (
        A2 = Automatons.recursive("link")
        A3 = Automaton("token") # )
        success = Automatons.recursive("success")
        fail = Automatons.recursive("fail")
        A0.add_left_next(A1, Automaton_Conditions.Match("("))
        A0.add_next(fail, Automaton_Conditions.Always)
        A1.add_next(A2, Automaton_Conditions.Always)
        A2.add_left_next(A3, Automaton_Conditions.Match(")"))
        A3.add_next(success, Automaton_Conditions.Always)
        return A0

class Converter:
    def __init__(self,
                 text,
                 base_html="{}\n{}",
                 automatons=Automatons,
                 escape_command_c={'<': '&lt;', '>': '&gt;', '\\': '\\', '&': '&amp;', '.': '.', '#': '#', '~': '~', '*': '*', '+': '+', '`': '`', '-': '-', '[': '[', ']': ']', '(': '(', ')': ')', 'n': '\n', '\n': ''},
                 unordered_list_s="<ul>\n{}\n</ul>",
                 unordered_list_objects_s="<li>{}</li>",
                 normal_text_s="<p>{}</p>",
                 header1_s="<h1>{}</h1>",
                 header2_s="<h2 id=\"{}\">{}</h2>",
                 header3_s="<h3>{}</h3>",
                 hyperlink_s="<a href=\"{}\">{}</a>",
                 bold_s="<b>{}</b>",
                 italic_s="<i>{}</i>",
                 underline_s="<u>{}</u>",
                 delete_s="<s>{}</s>",
                 table_s="<ul>\n{}\n</ul>",
                 table_object_s="<li>{}</li>",
                 table_object_link_s="<a href=\"{}\">{}</a>"):
        self.base = base_html
        self.text = text
        self.escape_command_c = escape_command_c
        self.unordered_list_s = unordered_list_s
        self.unordered_list_objects_s = unordered_list_objects_s
        self.automatons = automatons
        self.normal_text_s = normal_text_s
        self.header1_s = header1_s
        self.header2_s = header2_s
        self.header3_s = header3_s
        self.hyperlink_s = hyperlink_s
        self.bold_s = bold_s
        self.italic_s = italic_s
        self.underline_s = underline_s
        self.delete_s = delete_s
        self.table_of_contents = []
        self.table_data = ""
        self.table_s= table_s
        self.table_object_s = table_object_s
        self.table_object_link_s = table_object_link_s
    
    def renew_text_constructor(self, text):
        value = Converter("")
        for v in self.__dict__:
            setattr(value, v, getattr(self, v))
        value.text = text
        return value
    
    def parse_escape_char(self, is_only_specific_char=True):
        l = []
        bksl_b = False
        for v in self.text:
            if bksl_b and v in self.escape_command_c:
                bksl_b = False
                l.append(self.escape_command_c[v])
            elif bksl_b and is_only_specific_char:
                bksl_b = False
                l.append(v)
            elif bksl_b:
                bksl_b = False
                l.append("\\")
                l.append(v)
            elif v == "\\":
                bksl_b = True
            else:
                l.append(v)
        return self.renew_text_constructor("".join(l))
    
    def parse_markdown(self):
        status = []
        H1 = Automatons.header1()
        H2 = Automatons.header2()
        H3 = Automatons.header3()
        UL = Automatons.unordered_list_object()
        for line in self.text.split("\n"):
            s = 0
            ds = [{"success": line}, {}, {}, {}, {}]
            b4, ds[1] = does_accept_automaton(H1, line)
            s = 1 if b4 else s
            b4, ds[2] = does_accept_automaton(H2, line)
            s = 2 if b4 else s
            b4, ds[3] = does_accept_automaton(H3, line)
            s = 3 if b4 else s
            b4, ds[4] = does_accept_automaton(UL, line)
            s = 4 if b4 else s
            status.append([s, ds[s]["success"]])
        
        BOLD = Automatons.bold_token()
        ITALIC = Automatons.italic_token()
        UNDERLINE = Automatons.underline_token()
        DELETE = Automatons.delete_token()
        HYPERLINK_TEXT = Automatons.hyperlink_text()
        HYPERLINK_LINK = Automatons.hyperlink_link()
        
        for i in range(len(status)):
            status[i][1] = Converter.inline_parser(status[i][1], BOLD, self.bold_s)
            status[i][1] = Converter.inline_parser(status[i][1], UNDERLINE, self.underline_s)
            status[i][1] = Converter.inline_parser(status[i][1], DELETE, self.delete_s)
            status[i][1] = Converter.inline_parser(status[i][1], ITALIC, self.italic_s)
            
            b4, d = does_accept_automaton(HYPERLINK_TEXT, status[i][1])
            if b4:
                ab, ad = does_accept_automaton(HYPERLINK_LINK, d["success"], True)
                if ab:
                    status[i][1] = d[""] + self.hyperlink_s.format(ad["link"], d["title"]) + ad["success"]
        
        table = ["{}", self.header1_s, self.header2_s, self.header3_s, self.unordered_list_objects_s]
        for i in range(len(status)):
            if status[i][0] == 2:
                header_id = status[i][1].replace('"', '\\"')
                self.table_of_contents.append((header_id, status[i][1]))
                status[i][1] = table[status[i][0]].format(header_id, status[i][1])
            else: status[i][1] = table[status[i][0]].format(status[i][1])
        
        l = []
        ll = []
        lll = []
        b4 = False
        b0 = False
        for s, line in status:
            if s == 0:
                b0 = True
            if (s != 0 or line == "") and b0:
                l.append(self.normal_text_s.format("<br>\n".join(lll)))
                lll = []
                b0 = False
            if s == 4:
                b4 = True
            if s != 4 and b4:
                l.append(self.unordered_list_s.format("\n".join(ll)))
                ll = []
                b4 = False
            if b4:
                ll.append(line)
            elif b0:
                lll.append(line)
            else:
                l.append(line)
        
        if b4:
            l.append(self.unordered_list_s.format("\n".join(ll)))
        
        return self.renew_text_constructor("\n".join(l))
    
    def generate_table_of_contents(self):
        self.table_data = self.table_s.format(
            "\n".join(map(
                lambda a: self.table_object_s.format(
                     self.table_object_link_s.format(a[0], a[1])),
                self.table_of_contents)))
        return self
    
    def generate_html(self):
        return self.base.format(self.table_data, self.text)
    
    def parse(self):
        return self.parse_markdown()\
                   .parse_escape_char()\
                   .generate_table_of_contents()\
                   .generate_html()
    
    @staticmethod
    def inline_parser(text, automaton, string):
        b, d = does_accept_automaton(automaton, text)
        if b:
            ab, ad = does_accept_automaton(automaton, d["success"], True)
            if ab:
                return d[""] + string.format(ad[""]) + ad["success"]
        return text

if __name__ == "__main__":
    import sys
    data = ""
    defines = ""
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = f.read()
    with open(sys.argv[2], "r", encoding="utf-8") as f:
        defines = f.read()
    defines_l = defines.split("{}")
    if len(defines_l) != 3:
        raise Exception()
    head = defines_l[0]
    middle = defines_l[1]
    footer = defines_l[2]
    conv = Converter(data, "{}"+middle+"{}", header1_s="<h1 class=\"page-title\">{}</h1>", table_s="<ul>\n<li><h2>目次</h2></li>\n{}\n</ul>")
    
    with open(sys.argv[3], "w", encoding="utf-8") as f:
        f.write((head+conv.parse()+footer).replace("{\\}", "{}"))
    
    