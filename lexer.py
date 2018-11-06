import ply.lex as lex


class MyLexer(object):

    def __init__(self):

        self.lexer = None

        self.tokens = (
            'ID',
            'NUMBER',
            'PLUS',
            'MINUS',
            'TIMES',
            'DIVIDE',
            'EQUALS',
            'TEXT',
            'LPAREN',
            'RPAREN',
            'SHOW'
        )

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_EQUALS = r'\='
    t_SHOW = r'\$show'

    def t_NUMBER(self,t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = 'ID'  # Si no esta en las palabras reservadas retornamos el ID
        # Sino la palabra reservada
        return t

    def t_TEXT(self,t):
        r'\"(\s*\w*\_*\+*\-*\.*\,*\€*\!*\@*\#*\$*\%*\^*\**\(*\)*\;*\:*\\*\/*\|*\<*\>*\!*\¡*\?*\¿*\}*\{*\~*)*\"'
        t.value = str(t.value)

        return t

    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    t_ignore = ' \t'

    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)