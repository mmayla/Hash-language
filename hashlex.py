import sys
sys.path.insert(0,"../..")

import ply.lex as lex

reserved = (
	'NUMBER', 'STRING', 'BOOLEAN',
	)

tokens = reserved + (
	# Literals (identifier, number, string, boolean)
    'ID', 'NCONST', 'SCONST', 'BCONST',
    
    # Operators (+,-,*,/,%,|,&,**,^,||,&&,!,<,<=,>,>=,==,!=)
	'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
    'OR', 'AND', 'XOR', 'POWER',
    'LOR', 'LAND', 'LNOT',
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',
    
    # Other Operators (=,?,'@','#')
    'EQUALS', 'COND','AT','HASH',
    
    # Delimeters ( ) [ ] { } , . ; :
    'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET',
    'LBRACE', 'RBRACE',
    'COMMA', 'PERIOD', 'COLON',
    )
    
# Completely ignored characters
t_ignore           = ' \t\x0c'

# Newlines
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
# Operators
t_PLUS             = r'\+'
t_MINUS            = r'-'
t_TIMES            = r'\*'
t_DIVIDE           = r'/'
t_MOD              = r'%'
t_OR               = r'\|'
t_AND              = r'&'
t_XOR              = r'\*\*'
t_POWER			   = r'\^'
t_LOR              = r'\|\|'
t_LAND             = r'&&'
t_LNOT             = r'!'
t_LT               = r'<'
t_GT               = r'>'
t_LE               = r'<='
t_GE               = r'>='
t_EQ               = r'=='
t_NE               = r'!='

# Others operators
t_EQUALS           = r'='
t_COND 			   = r'\?'
t_AT			   = r'@'
t_HASH 			   = r'\#'

# Delimeters
t_LPAREN           = r'\('
t_RPAREN           = r'\)'
t_LBRACKET         = r'\['
t_RBRACKET         = r'\]'
t_LBRACE           = r'\{'
t_RBRACE           = r'\}'
t_COMMA            = r','
t_PERIOD           = r'\.'
t_COLON            = r':'

# Literals

reserved_map = { }
for r in reserved:
    reserved_map[r.lower()] = r
    
def t_ID(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved_map.get(t.value,"ID")
    return t
    
# Number literal
t_NCONST = """(\d+(\.\d*)?|\.\d+)([eE][-+]? \d+)?"""

# String literal
t_SCONST = r'\"([^\\\n]|(\\.))*?\"'

# Boolean literal
t_BCONST = r'like|dislike'

# Preprocessor directive (ignored)
def t_preprocessor(t):
    r'\#(.)*?\n'
    t.lexer.lineno += 1
    
def t_error(t):
    print("Illegal character %s" % repr(t.value[0]))
    t.lexer.skip(1)
    
lexer = lex.lex()
if __name__ == "__main__":
    lex.runmain(lexer)
