#ifndef MC_TEST
#define MC_TEST

//#define DATA  {0,0,100,23}
#define CHARDATA  {'a', {'b'}, 23}
#define STRDATA  {"god", "(hi),{how are [you]?}", ",", {"inner_{1}",{"inner_{2}", "inner_{2}_(1)"}}}

 /*test*/ #define /*middle_1***/ COMSTRUCT /*middle_2*/ { {1, 2.0, "str"}, {'1', .0075e1f,  /*test*/ "\\\\\\\\\\\\\\\\\\//////////////////"},   /*test*/ { +0x1dCbAF, 1.2E+0,  /*""*/ "\v\'\"\f \"\n\r\t\b\a\\",},}  /*enddd*/ //end

#define special "'1~!@#$^&*()_+-={':[,]}|;.</>?"

#define controls "\v\'\"\f \"\n\r\t\b\a\\"
#define controls_v "\\v\\\'\\\"\f \\\"\n\r\\r\t\b\a\\"

#define c_hex '\x0c'
#define c_oct '\12'
#define c_squote '\''
#define c_quote '\"'
#define c_bell '\a'
#define c_back '\b'
#define c_formfeed '\f'
#define c_htab '\t'
#define c_vtab '\v'
#define c_bslash '\\'
#define c_newline '\n'

#define HEX_A -0xa4A8
#define HEX_B 0X3fdB9
#define HEX_C 0X4f3L

#define quote '"'
#define quotes "&#34; (0x0022) 0x21 034 &#x22;"
#define slash "/ &^ \\"
#define _wide_str L"This is a string literal."//wide string "This is a string literal."

#define splitstr "24'23't" "323df" //"123fg"
#define comment/*I am a comment!*/"// /* */<!-- --"


//comment/*test*//
/*comment//test*/

#define trap "#define AA 123"

#define backslash	'\\'
#define tab_		'\t'

#define NS1 "with tab	"
#define NSRT "XXX \\tYYY\\nZZZZ \\n"

#define testE 25E-4
#define testE1 -1.5E-4

#define long_double  100.0L
#define float_only 100.2F
#define decimal_only .0075
#define unsigned_intn 123u

#define long_unsigned_intn 776255UL
#define long_intn 4293955295L /* /*
//Stringizing Operator  (#)
#define stringer( x ) printf_s( #x "\\n" )

#define _X 0200
#define _Y 1234
//#define F abc/
#define B def

#define DATA  {210,41,78.0,323,-457}

/* */
# /*321*/ define TT 123123
/*
comment */#define _1X 32.0
#define _1Y -48.970
#define _XY {-23,41}
#define _X 0100 //0ctal /* Constants
#define _Y -0124

#define COMPDATA  { {{1,3}, {2,3,5}, {31}},  {{12,016}, {1,30,0}}, 23 }


#else

#endif // !MC_TEST

#ifndef MC_TEST
#define MC_TEST

//#define DATA  {0,0,100,23}
#define CHARDATA  {'a', {'b'}, 23}
#define STRDATA  {"god", "(hi),{how are [you]?}", ",", {"inner_{1}",{"inner_{2}", "inner_{2}_(1)"}}}

 /*test*/ #define /*middle_1***/ COMSTRUCT /*middle_2*/ { {1, 2.0, "str"}, {'1', .0075e1f,  /*test*/ "\\\\\\\\\\\\\\\\\\//////////////////"},   /*test*/ { +0x1dCbAF, 1.2E+0,  /*""*/ "\v\'\"\f \"\n\r\t\b\a\\",},}  /*enddd*/ //end

#define special "'1~!@#$^&*()_+-={':[,]}|;.</>?"

#define controls "\v\'\"\f \"\n\r\t\b\a\\"
#define controls_v "\\v\\\'\\\"\f \\\"\n\r\\r\t\b\a\\"

#define c_hex '\x0c'
#define c_oct '\12'
#define c_squote '\''
#define c_quote '\"'
#define c_bell '\a'
#define c_back '\b'
#define c_formfeed '\f'
#define c_htab '\t'
#define c_vtab '\v'
#define c_bslash '\\'
#define c_newline '\n'

#define HEX_A -0xa4A8
#define HEX_B 0X3fdB9
#define HEX_C 0X4f3L

#define quote '"'
#define quotes "&#34; (0x0022) 0x21 034 &#x22;"
#define slash "/ &^ \\"
#define _wide_str L"This is a string literal."//wide string "This is a string literal."

#define splitstr "24'23't" "323df" //"123fg"
#define comment/*I am a comment!*/"// /* */<!-- --"


//comment/*test*//
/*comment//test*/

#define trap "#define AA 123"

#define backslash	'\\'
#define tab_		'\t'

#define NS1 "with tab	"
#define NSRT "XXX \\tYYY\\nZZZZ \\n"

#define testE 25E-4
#define testE1 -1.5E-4

#define long_double  100.0L
#define float_only 100.2F
#define decimal_only .0075
#define unsigned_intn 123u

#define long_unsigned_intn 776255UL
#define long_intn 4293955295L /* /*
//Stringizing Operator  (#)
#define stringer( x ) printf_s( #x "\\n" )

#define _X 0200
#define _Y 1234
//#define F abc/
#define B def

#define DATA  {210,41,78.0,323,-457}

/* */
# /*321*/ define TT 123123
/*
comment */#define _1X 32.0
#define _1Y -48.970
#define _XY {-23,41}
#define _X 0100 //0ctal /* Constants
#define _Y -0124

#define COMPDATA  { {{1,3}, {2,3,5}, {31}},  {{12,016}, {1,30,0}}, 23 }


#else

#endif // !MC_TEST

/*
BRANCH_DIRECTIVES test
*/
#ifndef MC_TEST
#define MC_TEST
#define WIDTH  123.0//number
#define HEIGHT  123 //int number
#ifdef MAC1
	#undef MAC1
	#define XF 2.3e6
	#ifdef MAC2
	#undef HEIGHT
	#define HEIGHT 1e6
	#ifdef MAC1
	#define XF2  -2         /* name used but not defined in nested block */
	#else
	#endif //!MAC1 again
	#ifndef MAC3
	#define MAC3 "mac13"
	#define XF3 true
	#else
	#endif //!MAC3
	#else
	//redefine WIDTH!
	#undef WIDTH
	#define WIDTH 100
	//to define MAC2:
	#define MAC2 "mac12"
	#endif  //!MAC2
#else
	#define MAC1 "mac1"
	#define XF -1.2e8
#ifdef MAC2
	#ifdef MAC1
	#define XF2  3
	#else
	#define XF2  4
	#endif //!MAC1 again
	#ifndef MAC3
	#define MAC3 "mac03"
	#define XF3 "ok"
	#else
	#endif //!MAC3
	#else
	#undef WIDTH
	#define WIDTH 98.1
	//to define MAC2:
	#define MAC2 "mac02"
	#ifdef MAC3
	#define XF3 "unok"
	#endif
	#endif
	#define PLATFORM64
#endif  //!MAC1
#ifdef MAC1
#define TestMac1 "TestMac exist"
#else
#define TestMac1 "TestMac not exist"
#endif
#ifdef PLATFORM64
	/* On a 64-bit system, rename the MyInit */
	#define MyInit "MyInit_64"
#else
	#define MyInit "MyInit"
#endif
 ///line comment
#ifdef TRACE_REFS
 /* When we are tracing reference counts,
 rename MyInit */
#undef MyInit
#ifdef PLATFORM64
	#define MyInit "MyInitTraceRefs_64"
#else
	#define MyInit "MyInitTraceRefs"
#endif
#endif
#define TRACE_REFS
#else
#endif // !MC_TEST

#define comment "// /* */<!-- --"
#define long_unsigned_intn 776255
#define _X 64
#define testE1 -0.00015
#define c_hex 12
#define backslash 92
#define HEX_C 1267
#define HEX_B 261561
#define HEX_A "-0xa4A8"
#define _XY {-23, 41}
#define unsigned_intn "123u"
#define c_quote 34
#define special "`1~!@#$^&*()_+-={':[,]}|;.</>?"
#define _1X 32.0
#define c_newline 10
#define tab_ 9
#define _Y -124
#define float_only "100.2F"
#define TT 123123
#define c_back 8
#define controls "\v\'\"\f \"\n\r\t\b\a\\"
#define quotes "&#34; (0x0022) 0x21 034 &#x22;"
#define _1Y -48.97
#define slash "/ &^ \\"
#define NSRT "XXX \tYYY\nZZZZ \n"
#define c_formfeed 12
#define controls_v "\\v\\\'\\\"\f \\\"\n\r\\r\t\b\a\\"
#define c_oct 10
#define decimal_only 0.0075
#define CHARDATA {97, {98}, 23}
#define quote 34
#define STRDATA {"god", "(hi)", {"how are [you]?"}, "", "", "", {"inner_", {1}, "", {"inner_", {2}, "", "inner_", {2}, "_(1)"}}}
#define long_intn 4293957295
#define MC_TEST
#define COMPDATA {{{1, 3}, {2, 3, 5}, {31}}, {{12, 14}, {1, 30, 0}}, 23}
#define c_vtab 11
#define _wide_str L"This is a string literal."
#define NS1 "with tab "
#define c_bell 7
#define COMSTRUCT {{1, 2.0, "str"}, {49, ".0075e1f", "\\\\\\\\\\\\\\\\\\//////////////////"}, {"+0x1dCbAF", 1.2, "\v\'\"\f \"\n\r\t\b\a\\"}}
#define splitstr "24'23't323df"
#define c_squote 39
#define long_double "100.0L"
#define ADVANCED_DEFINE
#define testE 0.0025
#define trap "#define AA 123"
#define c_htab 9
#define c_bslash 92

#ifndef MC_TEST
#define MC_TEST

//#define DATA  {0,0,100,23}
#define CHARDATA  {'a', {'b'}, 23}
#define STRDATA  {"god", "(hi),{how are [you]?}", ",", {"inner_{1}",{"inner_{2}", "inner_{2}_(1)"}}}

 /*test*/ #define /*middle_1***/ COMSTRUCT /*middle_2*/ { {1, 2.0, "str"}, {'1', .0075e1f,  /*test*/ "\\\\\\\\\\\\\\\\\\//////////////////"},   /*test*/ { +0x1dCbAF, 1.2E+0,  /*""*/ "\v\'\"\f \"\n\r\t\b\a\\",},}  /*enddd*/ //end

#define special "'1~!@#$^&*()_+-={':[,]}|;.</>?"

#define controls "\v\'\"\f \"\n\r\t\b\a\\"
#define controls_v "\\v\\\'\\\"\f \\\"\n\r\\r\t\b\a\\"

#define c_hex '\x0c'
#define c_oct '\12'
#define c_squote '\''
#define c_quote '\"'
#define c_bell '\a'
#define c_back '\b'
#define c_formfeed '\f'
#define c_htab '\t'
#define c_vtab '\v'
#define c_bslash '\\'
#define c_newline '\n'

#define HEX_A -0xa4A8
#define HEX_B 0X3fdB9
#define HEX_C 0X4f3L

#define quote '"'
#define quotes "&#34; (0x0022) 0x21 034 &#x22;"
#define slash "/ &^ \\"
#define _wide_str L"This is a string literal."//wide string "This is a string literal."

#define splitstr "24'23't" "323df" //"123fg"
#define comment/*I am a comment!*/"// /* */<!-- --"


//comment/*test*//
/*comment//test*/

#define trap "#define AA 123"

#define backslash	'\\'
#define tab_		'\t'

#define NS1 "with tab	"
#define NSRT "XXX \\tYYY\\nZZZZ \\n"

#define testE 25E-4
#define testE1 -1.5E-4

#define long_double  100.0L
#define float_only 100.2F
#define decimal_only .0075
#define unsigned_intn 123u

#define long_unsigned_intn 776255UL
#define long_intn 4293955295L /* /*
//Stringizing Operator  (#)
#define stringer( x ) printf_s( #x "\\n" )

#define _X 0200
#define _Y 1234
//#define F abc/
#define B def

#define DATA  {210,41,78.0,323,-457}

/* */
# /*321*/ define TT 123123
/*
comment */#define _1X 32.0
#define _1Y -48.970
#define _XY {-23,41}
#define _X 0100 //0ctal /* Constants
#define _Y -0124

#define COMPDATA  { {{1,3}, {2,3,5}, {31}},  {{12,016}, {1,30,0}}, 23 }


#else

#endif // !MC_TEST

/*
BRANCH_DIRECTIVES test
*/
#ifndef MC_TEST
#define MC_TEST
#define WIDTH  123.0//number
#define HEIGHT  123 //int number
#ifdef MAC1
	#undef MAC1
	#define XF 2.3e6
	#ifdef MAC2
	#undef HEIGHT
	#define HEIGHT 1e6
	#ifdef MAC1
	#define XF2  -2         /* name used but not defined in nested block */
	#else
	#endif //!MAC1 again
	#ifndef MAC3
	#define MAC3 "mac13"
	#define XF3 true
	#else
	#endif //!MAC3
	#else
	//redefine WIDTH!
	#undef WIDTH
	#define WIDTH 100
	//to define MAC2:
	#define MAC2 "mac12"
	#endif  //!MAC2
#else
	#define MAC1 "mac1"
	#define XF -1.2e8
/*mac2*/#ifdef MAC2
	#ifdef MAC1
	#define XF2  3
	#else
	#define XF2  4
	#endif //!MAC1 again
	#ifndef MAC3
	#define MAC3 "mac03"
	#define XF3 "ok"
	#else
	#endif //!MAC3
	#else
	#undef WIDTH
	#define WIDTH 98.1
	//to define MAC2:
	#define MAC2 "mac02"
	#ifdef MAC3
	#define XF3 "unok"
	#endif
	#endif
	#define PLATFORM64
#endif  //!MAC1
#ifdef MAC1
#define TestMac1 "TestMac exist"
#else
#define TestMac1 "TestMac not exist"
#endif
# /*If*/ ifdef PLATFORM64
	/* On a 64-bit system, rename the MyInit */
	#define MyInit "MyInit_64"
# else
	#define MyInit "MyInit"
# /*End*/ endif
 ///line comment
#ifdef TRACE_REFS
 /* When we are tracing reference counts,
 rename MyInit */
# undef MyInit
#ifdef PLATFORM64
	#define MyInit "MyInitTraceRefs_64"
#else
	#define MyInit "MyInitTraceRefs"
#endif
#endif
#define TRACE_REFS
#else
#endif // !MC_TEST
/*
BRANCH_DIRECTIVES test
*/
#ifndef MC_TEST
#define MC_TEST
#define WIDTH  123.0//number
#define HEIGHT  123 //int number
#ifdef MAC1
	#undef MAC1
	#define XF 2.3e6
	#ifdef MAC2
	#undef HEIGHT
	#define HEIGHT 1e6
	#ifdef MAC1
	#define XF2  -2         /* name used but not defined in nested block */
	#else
	#endif //!MAC1 again
	#ifndef MAC3
	#define MAC3 "mac13"
	#define XF3 true
	#else
	#endif //!MAC3
	#else
	//redefine WIDTH!
	#undef WIDTH
	#define WIDTH 100
	//to define MAC2:
	#define MAC2 "mac12"
	#endif  //!MAC2
#else
	#define MAC1 "mac1"
	#define XF -1.2e8
#ifdef MAC2
	#ifdef MAC1
	#define XF2  3
	#else
	#define XF2  4
	#endif //!MAC1 again
	#ifndef MAC3
	#define MAC3 "mac03"
	#define XF3 "ok"
	#else
	#endif //!MAC3
	#else
	#undef WIDTH
	#define WIDTH 98.1
	//to define MAC2:
	#define MAC2 "mac02"
	#ifdef MAC3
	#define XF3 "unok"
	#endif
	#endif
	#define PLATFORM64
#endif  //!MAC1
#ifdef MAC1
#define TestMac1 "TestMac exist"
#else
#define TestMac1 "TestMac not exist"
#endif
#ifdef PLATFORM64
	/* On a 64-bit system, rename the MyInit */
	#define MyInit "MyInit_64"
#else
	#define MyInit "MyInit"
#endif
 ///line comment
#ifdef TRACE_REFS
 /* When we are tracing reference counts,
 rename MyInit */
#undef MyInit
#ifdef PLATFORM64
	#define MyInit "MyInitTraceRefs_64"
#else
	#define MyInit "MyInitTraceRefs"
#endif
#endif
#define TRACE_REFS
#else
#endif // !MC_TEST

#define comment "// /* */<!-- --"
#define long_unsigned_intn 776255
#define _X 64
#define testE1 -0.00015
#define c_hex 12
#define backslash 92
#define HEX_C 1267
#define HEX_B 261561
#define HEX_A -42152
#define _XY {-23,41}
#define unsigned_intn 123
#define c_quote 34
#define special "'1~!@#$^&*()_+-={':[,]}|;.</>?"
#define _1X 32.0
#define c_newline 10
#define tab_ 9
#define _Y -84
#define float_only 100.2
#define TT 123123
#define c_back 8
#define controls "\v\'\"\f \"\n\r\t\b\a\\"
#define quotes "&#34; (0x0022) 0x21 034 &#x22;"
#define _1Y -48.97
#define slash "/ &^ \\"
#define NSRT "XXX \\tYYY\\nZZZZ \\n"
#define c_formfeed 12
#define controls_v "\\v\\\'\\\"\f \\\"\n\r\\r\t\b\a\\"
#define c_oct 10
#define decimal_only 0.0075
#define CHARDATA {97,{98},23}
#define quote 34
#define STRDATA {"god","(hi),{how are [you]?}",",",{"inner_{1}",{"inner_{2}","inner_{2}_(1)"}}}
#define long_intn 4293955295
#define MC_TEST
#define COMPDATA {{{1,3},{2,3,5},{31}},{{12,14},{1,30,0}},23}
#define c_vtab 11
#define _wide_str L"This is a string literal."
#define NS1 "with tab	"
#define c_bell 7
#define COMSTRUCT {{1,2.0,"str"},{49,0.075,"\\\\\\\\\\\\\\\\\\//////////////////"},{1952687,1.2,"\v\'\"\f \"\n\r\t\b\a\\"}}
#define splitstr "24'23't323df"
#define c_squote 39
#define long_double 100.0
#define testE 0.0025
#define trap "#define AA 123"
#define c_htab 9
#define c_bslash 92