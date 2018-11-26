import ply.yacc as yacc
from .lexer import Lexer

class Parser:
    def __init__(self):
        self.lexer = Lexer()
        self.lexer.build()
        self.tokens = self.lexer.tokens
        self.variables = {}

    def p_quote_assign(self,p):
        "quote : assign"
        p[0] = p[1]

    def p_quote_expr(self,p):
        "quote : expr"
        p[0] = p[1]

    def p_assign(self,p):
        "assign : ID EQUALS expr"
        #print("Assigning variable", p[1], "to", p[3])
        self.variables[p[1]] = p[3]
        p[0] = "Assigning "+str(p[3])+" To Variable : "+str(p[1])

    def p_expr_sum(self,p):
        "expr : expr PLUS term"
        try:
            p[0] = p[1] + p[3]
        except:
            #print("Tipos de datos incompatibles")
            p[0] = "Tipos de datos incompatibles"

    def p_expr_min(self,p):
        "expr : expr MINUS term"
        try:
            p[0] = p[1] - p[3]
        except:
            #print("Tipos de datos incompatibles")
            p[0] = "Tipos de datos incompatibles"

    def p_expr_div(self,p):
        "expr : expr DIVIDE term"
        try:
            p[0] = p[1] / p[3]
        except:
            #print("Tipos de datos incompatibles")
            p[0] = "Tipos de datos incompatibles"

    def p_expr_time(self,p):
        "expr : expr TIMES term"
        try:
            p[0] = p[1] * p[3]
        except:
            #print("Tipos de datos incompatibles")
            p[0] = "Tipos de datos incompatibles"

    def p_expr_term(self,p):
        "expr : term"
        p[0] = p[1]

    def p_term_num(self,p):
        "term : NUMBER"
        p[0] = p[1]

    def p_command(self,p):
        "term : SHOW"
        print(self.variables)
        p[0] = self.variables

    def p_term_id(self,p):
        "term : ID"
        p[0] = self.variables[p[1]]

    def p_term_text(self,p):
        "term : TEXT"
        p[0] = str(p[1].replace("\"",""))


    def p_error(self,p):
        #print("Syntax error in input!")
        p[0] = "Syntax error in input!"

    def evaluate(self,s):
        par = yacc.yacc(module=self)
        result = par.parse(s, tracking=True, lexer= self.lexer.lexer)
        print(result)
        return result