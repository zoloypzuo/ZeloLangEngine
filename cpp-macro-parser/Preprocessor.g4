grammar Preprocessor;

chunk : block EOF;

// MSDN本来用text这个词，但是很模糊，text还包含C++代码部分，不只是宏语言
// 这里我使用block
// MSDN在这里描述模糊，我自己的理解是，每行至多一个宏指令语句
// 所以换行符被算入语法，不是当作空白符跳过
// text: Any sequence of text
//
// 首先源文本可以是空的
// 然后最后一行可以没有换行
block : (stat? Newline)* stat?;

stat
    : control_line
	| conditional
	;

// 经过实验，#和define之间是可以有空白符的，不过这里简化一下
control_line
    : '#define' Identifier token_string?
    | '#undef' Identifier
    ;

// 这里不会有if-else匹配错误的问题，LL算法进到block后if总是匹配正确的else
conditional : if_part /*elif_parts?*/ else_parts? endif_line;

if_part : if_line Newline block;

if_line
    : /*#if constant_expression
	|*/ '#ifdef' Identifier
	| '#ifndef' Identifier
	;
/*
elif_parts : elif_line text
	| elif_parts elif_line text
	;

elif_line : #elif constant_expression
*/
else_parts : else_line Newline block;

else_line : '#else';

endif_line : '#endif';

// token_string定义被题目简化和限制，其实是字面量表达式
/*token_string : token+;

token : keyword
	| identifier
	| constant
	| operator
	| punctuator
	;
*/
token_string
    : Bool
	| Char  // 忽略宽字符
	| number
	| string
	| aggregate_exp
	;

// MSDN没有找到BNF描述，自己照着lua的table-constructor写一个
aggregate_exp : '{' fieldlist? '}';

fieldlist : token_string (',' token_string)* ','?;

// antlr提示不支持\v
// [ \t\v\f]+ -> skip
Whitespace : [ \t]+ -> skip;

Newline: ( '\r\n' | '\n'); // 保留空白符

// 转为空格不知道antlr怎么写
LineComment: '//' ~[\r\n]* -> skip;  // to ' '

BlockComment: '/*' .*? '*/' -> skip;  // to ' '


Bool : 'true' | 'false';

Char : '\'' ~'\''  '\'';

// number和string先参考一下lua

number
    : INT | HEX | FLOAT
    ;

string
    : NORMALSTRING
    | LONGSTRING
    ;

NORMALSTRING : '"' ( EscapeSequence | ~'"' )* '"';

LONGSTRING : 'L' NORMALSTRING;

INT
    : Digit+
    ;

HEX
    : '0' [xX] HexDigit+
    ;

// 这里加了f后缀
FLOAT
    : Digit+ '.' Digit* ExponentPart? 'f'?
    | '.' Digit+ ExponentPart? 'f'?
    | Digit+ ExponentPart 'f'?
    ;

fragment
ExponentPart
    : [eE] [+-]? Digit+
    ;

fragment
EscapeSequence
    : '\\' [abfnrtvz"'\\]
    | '\\' '\r'? '\n'
    | DecimalEscape
    | HexEscape
    | UtfEscape
    ;

fragment
DecimalEscape
    : '\\' Digit
    | '\\' Digit Digit
    | '\\' [0-2] Digit Digit
    ;

fragment
HexEscape
    : '\\' 'x' HexDigit HexDigit
    ;

fragment
UtfEscape
    : '\\' 'u{' HexDigit+ '}'
    ;

fragment
Digit
    : [0-9]
    ;

fragment
HexDigit
    : [0-9a-fA-F]
    ;

// 印象笔记 《true被识别为标识符》
Identifier :  [a-zA-Z_][a-zA-Z_0-9]*;