import ply.yacc as yacc
from .lexer import Lexer

class Parser:
    """
        contiene todo lo relacionado con el analisis sintactico y semantico
        de los algoritmos digitados por el usuario
    """
    def __init__(self):
        """
            Constructor donde se inicializan la variables necesarias para
            el análisis de los códigos
        """
        self.lexer = Lexer() # Instancia del analizador lexico
        self.lexer.build()
        self.tokens = self.lexer.tokens #tokens del analizdor lexico para construir las reglas
        self.variables = {}  # Diccionario que contiene las variables declaradas

    # -------------------------------------------------------------------------------------------------
    #   produccion principal de el analizador sintactico - semantico
    #
    #   las producciones se definen de la siguiente manera:
    #       siempre se utilizan metodos para definirla con el prefijo p_ y reciben como parametro un p
    #       que contiene lo que ha subido el arbol mediante las reglas semanticas
    #       ejemplo:
    #               para una sola produccion
    #               def p_nombreprocuccion(p):
    #                   'nombreProduccion : produccion'
    #
    #               para varias producciones
    #               def p_nombreproduccion(p):
    #                   ''' nombreProduccion : produccion1
    #                                        | produccion2 '''
    #
    #               para reglas semanticas
    #               def p_nombreproduccion(p):
    #                   #aqui se pone la produccion de las formas ya especificadas
    #                   'nombreproduccion : token1 token2 prodcuccion1 token3'
    #                   #reglas semanticas
    #                   p[0] = p[1] + p[3]
    #
    #                   donde p[0] -> nombreproduccion , p[1] -> token1 , p[2] -> lo que devuelve produccion1
    #
    # -------------------------------------------------------------------------------------------------
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
        """
        Método que ejecuta el análisis de un código
        :param s: sentencia a analizar
        :return: respuesta de la operación despues del análisis
        """
        par = yacc.yacc(module=self)
        result = par.parse(s, tracking=True, lexer= self.lexer.lexer)
        print(result)
        return result