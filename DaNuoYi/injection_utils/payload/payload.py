import random

from DaNuoYi.injection_utils.payload.payload_dict import PayloadDict


class Payload(object):

    def __init__(self, dict_type, tag=None, cld=None, length=0, auto=True):
        self.ctx = list()
        self.ctx.append(tag)
        self.injection = ''
        self.cld = cld
        self.tag = tag

        self.length = length
        self.sub_ctx = None
        self.target = None
        self.i = 1

        if auto:
            if dict_type.upper() == 'XSS':
                self.generate_ctx('root', PayloadDict().ebnfXSS)
                self.payload_dict = PayloadDict().ebnfXSS
            elif dict_type.upper() == 'SQLI':
                self.generate_ctx('root', PayloadDict().ebnfSQLi)
                self.payload_dict = PayloadDict().ebnfSQLi
            elif dict_type.upper() == 'PHPI':
                self.generate_ctx('root', PayloadDict().ebnfPHPi)
                self.payload_dict = PayloadDict().ebnfPHPi
            elif dict_type.upper() == 'OSI':
                self.generate_ctx('root', PayloadDict().ebnfOSi)
                self.payload_dict = PayloadDict().ebnfOSi
            elif dict_type.upper() == 'XMLI':
                self.generate_ctx('root', PayloadDict().ebnfXMLi)
                self.payload_dict = PayloadDict().ebnfXMLi
            elif dict_type.upper() == 'HTMLI':
                self.generate_ctx('root', PayloadDict().ebnfHTMLi)
                self.payload_dict = PayloadDict().ebnfHTMLi
            else:
                print('Error injection_utils task name!')
            self.injection = self.generate_str(self.ctx)
        else:
            self.payload_dict = dict_type

    def generate_ctx(self, tag, dictory):
        if tag not in dictory.keys():
            return tag
        sub_table = dictory[tag]
        cld = random.choice(sub_table) if len(sub_table) > 1 else sub_table[0]
        children = dict(tag=tag, cld=cld, ctx=list())
        children['ctx'].append(tag)
        # self.length += 1

        # children = Payload(tag=tag, cld=cld)
        for child in children['cld']:
            temp = self.generate_ctx(child, dictory)[:]
            children['ctx'].append(temp)
        self.ctx = children['ctx']
        self.length += 1
        return children['ctx']

    def traversal(self, ctx):
        res = list()
        for i in ctx:
            if isinstance(i, list):
                res.extend(self.traversal(ctx=i[1:]))
            else:
                res.append(i + ' ')
                # res.append(i)
        return res

    def generate_str(self, ctx):
        return ''.join(self.traversal(ctx)[1:])

    def get_tag_slice(self, ctx, tag):
        res = list()
        for i in range(len(ctx)):
            if isinstance(ctx[i], list):
                if ctx[i][0] == tag:
                    res.append(ctx[i])
                else:
                    res.extend(self.get_tag_slice(ctx[i][1:], tag))
        return res

    def get_index_slice(self, ctx, index=999, begin=True):
        if begin:
            self.i = 1
        for j in ctx:
            if isinstance(j, list):
                self.i += 1
                if self.i > index:
                    self.target = j[0]
                    self.sub_ctx = j
                else:
                    self.get_index_slice(j[1:], index, False)
        return self.target, self.sub_ctx

    def set_slice(self, option_slice, option, slices):
        try:
            # same tag
            if option_slice[option][0] == slices[0]:
                option_slice[option][1:] = slices[1:]
            if option_slice[0] == slices[option][0]:
                option_slice[1:] = slices[option][1:]
            if option_slice[0] == slices[0]:
                option_slice[1:] = slices[1:]
        except Exception as e:
            print('Index overstep: %s' % IndexError)
