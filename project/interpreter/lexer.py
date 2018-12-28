import ply.lex as lex

class Lexer(object):
    """
        contiene todo lo relacionado con el analisis léxico
        de los algoritmos digitados por el usuario
    """
    def __init__(self):

        self.lexer = None

        #Lista de tokens simples
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

    # -------------------------------------------------------------------------------------------------
    #        las variables que incian con t_ contienen la expresion regular de tokens que nececitan
    #        exp regular simple, se nombran así : t_nombrevar = r'expresion regular'
    # -------------------------------------------------------------------------------------------------
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_EQUALS = r'\='
    t_SHOW = r'\$show'

    # --------------------------------------------------------------------------------------------------------
    #       los metodos que contienen t_ son para las expresiones regulares de tokens (con exp mas complejas)
    #       y siempre recibe como parametro un t-> indicador de token
    #       normalmente se nombran así: def t_nombretoken(t):
    #                                      r'expresion regular'
    #
    # --------------------------------------------------------------------------------------------------------
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
        """
        Métodoque construye el analizador léxico para ser usado en los posteriores análisis
        """
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self, data):
        """
        Método que obtiene los tokens de una sentencia
        """
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)