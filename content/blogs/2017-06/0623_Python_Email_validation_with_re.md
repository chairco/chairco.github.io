---
Title: Python 上使用REGEXP(Regular Expression) 驗證 Email
Slug: Python email validate with REGEXP
Date: 2017-06-23 14:06:24
Tags: Python
Category: Python

---

在 Google 下個關鍵字： **Python, Regular Expression or REGEXP, email, validate, validation** 在 Google 應該不下數十篇在論壇、網誌使用正規表達式（Regular Expression）來驗證 email 格式的文章或是問題、甚至有人實作 package。

使用這個東西也一陣子，但好像從來沒認真去研究究竟細節有哪些，ctrl + c, ctrl + r 成了常態，自然踩雷無可避免。剛好最近要修一個東西，因此順便整理細節。


## 瞭解套件實作方法

首先我的 Python 環境目前是 3.6.0。而切入點是從別人實作出來的套件去 implement

+ validate_email
先瞭解一下大概比較紅的套件實作細節，找了一個星星數挺多的 [validate_email](https://github.com/syrusakbary/validate_email.git) 最後的更新大概是兩年前，不知道在 3.6.0 上運作狀態，總之先 clone 嘗試看看。

首先要先安裝一個叫 pyDNS package，然後立刻 gg。
在 `DNS/__ini__.py` 有 Type, `Type,Opcode,Status,Class` 幾個套件卻用 `import Type,Opcode,Status,Class` 這種 relative import 來處理 @@，就噴出錯誤訊息像是：

```
Traceback (most recent call last):
  File "setup.py", line 12, in <module>
    import DNS
  File "/Users/chairco/OneDrive/SourceCode/django/temp/pydns-2.3.6/DNS/__init__.py", line 14, in <module>
    import Type,Opcode,Status,Class
ModuleNotFoundError: No module named 'Type'

```

return 變數方法也用了古老的奇怪方法：

```
Traceback (most recent call last):
  File "setup.py", line 12, in <module>
    import DNS
  File "/Users/chairco/OneDrive/SourceCode/django/temp/pydns-2.3.6/DNS/__init__.py", line 14, in <module>
    from . import Type,Opcode,Status,Class
  File "/Users/chairco/OneDrive/SourceCode/django/temp/pydns-2.3.6/DNS/Type.py", line 54
    else: return `type`
                 ^
SyntaxError: invalid syntax

```

raise 的語法也都是 2.7 的：

```
Traceback (most recent call last):
  File "setup.py", line 12, in <module>
    import DNS
  File "/Users/chairco/OneDrive/SourceCode/django/temp/pydns-2.3.6/DNS/__init__.py", line 15, in <module>
    from .Base import DnsRequest, DNSError
  File "/Users/chairco/OneDrive/SourceCode/django/temp/pydns-2.3.6/DNS/Base.py", line 119
    raise TimeoutError, 'Timeout'
                      ^
SyntaxError: invalid syntax
```


看起來 pyDNS 非常古老，裡面的寫法用了許多舊的語法糖，要改起來實在不容易，不過看起來和我們要做 email validate 也沒什麼相關性。

再來在 **validate_email** 套件的 issue tracker 和 PR 一堆人發了 PR 和 issue，作者明顯就是射後不想理會，總之這種作者自己不想維護的東西又不想放給其他人維護的專案大概就看看囉。不過參考一下大概的邏輯還是美德。

先看看的 USAGE (使用說明)，看起來使用了一個 validate_email 的一級函式來處理：

```
from validate_email import validate_email
is_valid = validate_email('example@example.com')
```

來看看程式碼：

```python
def validate_email(email, check_mx=False, verify=False, debug=False, smtp_timeout=10):
    """Indicate whether the given string is a valid email address
    according to the 'addr-spec' portion of RFC 2822 (see section
    3.4.1).  Parts of the spec that are marked obsolete are *not*
    included in this test, and certain arcane constructions that
    depend on circular definitions in the spec may not pass, but in
    general this should correctly identify any email address likely
    to be in use as of 2011."""
    if debug:
        logger = logging.getLogger('validate_email')
        logger.setLevel(logging.DEBUG)
    else:
        logger = None

    try:
        assert re.match(VALID_ADDRESS_REGEXP, email) is not None
        check_mx |= verify
        if check_mx:
            if not DNS:
                raise Exception('For check the mx records or check if the email exists you must '
                                'have installed pyDNS python package')
            hostname = email[email.find('@') + 1:]
            mx_hosts = get_mx_ip(hostname)
            if mx_hosts is None:
                return False
            for mx in mx_hosts:
                try:
                    if not verify and mx[1] in MX_CHECK_CACHE:
                        return MX_CHECK_CACHE[mx[1]]
                    smtp = smtplib.SMTP(timeout=smtp_timeout)
                    smtp.connect(mx[1])
                    MX_CHECK_CACHE[mx[1]] = True
                    if not verify:
                        try:
                            smtp.quit()
                        except smtplib.SMTPServerDisconnected:
                            pass
                        return True
                    status, _ = smtp.helo()
                    if status != 250:
                        smtp.quit()
                        if debug:
                            logger.debug(u'%s answer: %s - %s', mx[1], status, _)
                        continue
                    smtp.mail('')
                    status, _ = smtp.rcpt(email)
                    if status == 250:
                        smtp.quit()
                        return True
                    if debug:
                        logger.debug(u'%s answer: %s - %s', mx[1], status, _)
                    smtp.quit()
                except smtplib.SMTPServerDisconnected:  # Server not permits verify user
                    if debug:
                        logger.debug(u'%s disconected.', mx[1])
                except smtplib.SMTPConnectError:
                    if debug:
                        logger.debug(u'Unable to connect to %s.', mx[1])
            return None
    except AssertionError:
        return False
    except (ServerError, socket.error) as e:
        if debug:
            logger.debug('ServerError or socket.error exception raised (%s).', e)
        return None
    return True


```

看起來也很單純用了斷句 aasert 處理 re 判斷 `re.match(VALID_ADDRESS_REGEXP, email) is not None` 如果錯誤就拋出 False。其他大概可以省去不看。所以直接來看看 VALID_ADDRESS_REGEXP 怎麼處理。

```python
WSP = r'[\s]'                                        # see 2.2.2. Structured Header Field Bodies
CRLF = r'(?:\r\n)'                                   # see 2.2.3. Long Header Fields
NO_WS_CTL = r'\x01-\x08\x0b\x0c\x0f-\x1f\x7f'        # see 3.2.1. Primitive Tokens
QUOTED_PAIR = r'(?:\\.)'                             # see 3.2.2. Quoted characters
FWS = r'(?:(?:' + WSP + r'*' + CRLF + r')?' + \
      WSP + r'+)'                                    # see 3.2.3. Folding white space and comments
CTEXT = r'[' + NO_WS_CTL + \
        r'\x21-\x27\x2a-\x5b\x5d-\x7e]'              # see 3.2.3
CCONTENT = r'(?:' + CTEXT + r'|' + \
           QUOTED_PAIR + r')'                        # see 3.2.3 (NB: The RFC includes COMMENT here
# as well, but that would be circular.)
COMMENT = r'\((?:' + FWS + r'?' + CCONTENT + \
          r')*' + FWS + r'?\)'                       # see 3.2.3
CFWS = r'(?:' + FWS + r'?' + COMMENT + ')*(?:' + \
       FWS + '?' + COMMENT + '|' + FWS + ')'         # see 3.2.3
ATEXT = r'[\w!#$%&\'\*\+\-/=\?\^`\{\|\}~]'           # see 3.2.4. Atom
ATOM = CFWS + r'?' + ATEXT + r'+' + CFWS + r'?'      # see 3.2.4
DOT_ATOM_TEXT = ATEXT + r'+(?:\.' + ATEXT + r'+)*'   # see 3.2.4
DOT_ATOM = CFWS + r'?' + DOT_ATOM_TEXT + CFWS + r'?' # see 3.2.4
QTEXT = r'[' + NO_WS_CTL + \
        r'\x21\x23-\x5b\x5d-\x7e]'                   # see 3.2.5. Quoted strings
QCONTENT = r'(?:' + QTEXT + r'|' + \
           QUOTED_PAIR + r')'                        # see 3.2.5
QUOTED_STRING = CFWS + r'?' + r'"(?:' + FWS + \
                r'?' + QCONTENT + r')*' + FWS + \
                r'?' + r'"' + CFWS + r'?'
LOCAL_PART = r'(?:' + DOT_ATOM + r'|' + \
             QUOTED_STRING + r')'                    # see 3.4.1. Addr-spec specification
DTEXT = r'[' + NO_WS_CTL + r'\x21-\x5a\x5e-\x7e]'    # see 3.4.1
DCONTENT = r'(?:' + DTEXT + r'|' + \
           QUOTED_PAIR + r')'                        # see 3.4.1
DOMAIN_LITERAL = CFWS + r'?' + r'\[' + \
                 r'(?:' + FWS + r'?' + DCONTENT + \
                 r')*' + FWS + r'?\]' + CFWS + r'?'  # see 3.4.1
DOMAIN = r'(?:' + DOT_ATOM + r'|' + \
         DOMAIN_LITERAL + r')'                       # see 3.4.1
ADDR_SPEC = LOCAL_PART + r'@' + DOMAIN               # see 3.4.1

# A valid address will match exactly the 3.4.1 addr-spec.
VALID_ADDRESS_REGEXP = '^' + ADDR_SPEC + '$'

```
覺得看完這串正規表方式快暈了。到底是要相依多少變數啊 QQ。

但我們可以嘗試把 VALID_ADDRESS_REGEXP 變數印出來看看他的正規表達式怎麼做的。從作者說明看起來是根據 [RFC 2822 SEPC](https://www.ietf.org/rfc/rfc2822.txt) 所定義實作，因此在每個正規表達式也說明出自於哪些章節。就從上到下一個個看正規表達式意思吧。


### 2.2.2. Structured Header Field Bodies

`WSP = r'[\s]'` 白字元族(Character class)同等 [\t\n\r\f] or [:space:]


### 2.2.3. Long Header Fields

`CRLF = r'(?:\r\n)'` 標定所有 `\r\n` 字元


### 3.2.1. Primitive Tokens

`NO_WS_CTL = r'\x01-\x08\x0b\x0c\x0f-\x1f\x7f'` 十六進位 1-8, 11, 12, 14-31, 127 等字元


### 3.2.2. Quoted characters

`QUOTED_PAIR = r'(?:\\.)'` 標定特殊字元 `.`


### 3.2.3. Folding white space and comments
白字元，像是隱藏在資料中的空白鍵、換行和跳格等等

`FWS = r'(?:(?:' + WSP + r'*' + CRLF + r')?' + WSP + r'+)'` 

+ `WSP`：是指空白字元, `?:WSP`：標定所有空白字元
+ `*`: 前一個比對字元可以任意多次
+ `CRLF`: 標定所有 `\r\n` 字元
+ `?` 匹配零次或一次
+ `'(?:(?:[\\s]*(?:\\r\\n))?[\\s]+)'`： 只要是 `__字元`, `__ 指的是空白`。

`CTEXT = r'[' + NO_WS_CTL + \r'\x21-\x27\x2a-\x5b\x5d-\x7e]'`

        
`CCONTENT = r'(?:' + CTEXT + r'|' + QUOTED_PAIR + r')'`
           
           
`COMMENT = r'\((?:' + FWS + r'?' + CCONTENT + \r')*' + FWS + r'?\)'`
 
 
`CFWS = r'(?:' + FWS + r'?' + COMMENT + ')*(?:' + FWS + '?' + COMMENT + '|' + FWS + ')'`


### 3.2.4. Atom

```ATEXT = r'[\w!#$%&\'\*\+\-/=\?\^`\{\|\}~]'```
       
`ATOM = CFWS + r'?' + ATEXT + r'+' + CFWS + r'?'`
    
`DOT_ATOM_TEXT = ATEXT + r'+(?:\.' + ATEXT + r'+)*'`

`DOT_ATOM = CFWS + r'?' + DOT_ATOM_TEXT + CFWS + r'?'`


### 3.2.5. Quoted strings

`QTEXT = r'[' + NO_WS_CTL + \r'\x21\x23-\x5b\x5d-\x7e]'`

`QCONTENT = r'(?:' + QTEXT + r'|' + \QUOTED_PAIR + r')'`

`QUOTED_STRING = CFWS + r'?' + r'"(?:' + FWS + \r'?' + QCONTENT + r')*' + FWS + \r'?' + r'"' + CFWS + r'?'`


### 3.4.1. Addr-spec specification

`LOCAL_PART = r'(?:' + DOT_ATOM + r'|' + \QUOTED_STRING + r')'`

`DTEXT = r'[' + NO_WS_CTL + r'\x21-\x5a\x5e-\x7e]'`

`DCONTENT = r'(?:' + DTEXT + r'|' + \QUOTED_PAIR + r')'`

`DOMAIN_LITERAL = CFWS + r'?' + r'\[' + \r'(?:' + FWS + r'?' + DCONTENT + \r')*' + FWS + r'?\]' + CFWS + r'?'`

`DOMAIN = r'(?:' + DOT_ATOM + r'|' + \DOMAIN_LITERAL + r')'`

`ADDR_SPEC = LOCAL_PART + r'@' + DOMAIN`


## 比較其他方法異同

TBD(筆者有點偷懶，稍晚再補上。)

***











