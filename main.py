import lexer
import parse
if __name__ == '__main__':
    lexico = lexer.MyLexer()
    lexico.build()
    data = '''
    3 + 4 * 10
      + -20 *2 x =
    '''
    lexico.test(data)
    par = parse.Parser()
    par.evaluate('3+3')

    while True:
        s = input('Calc > ')
        par.evaluate(s)