# CScript-lang
cscript programming language prototype

## Statements
- [x] import statement
- [x] var declairation
- [x] let declairation
- [x] if statement
- [ ] for statement
- [x] while statement
- [x] do|while statement
- [x] switch|case statement
- [x] try/except/finally statement
- [x] print (print is a statement here.)
- [x] class declairation
- [x] continue statement
- [x] break statement
- [ ] enum declairation
- [x] function declairation
- [x] function expression
- [x] statement block
- [x] expression statement


## Datatype
- [x] CSObject(Hashmap based)
- [x] CSInteger
- [x] CSDouble
- [x] CSString
- [x] CSBoolean(to be re-implemented using singleton)
- [x] CSNullType(to be re-implemented using singleton)
- [x] CSArray
- [x] CSMap
- [x] CSCallable
- [x] CSClass
- [x] CSClassInstance
- [x] CSClassBoundMethod
- [x] CSBound
- [x] CSException
- [x] CSTypeError
- [x] CSAttributeError
- [x] CSIndexError

## Other feature(s)
- [x] operator overloading(few)

# TODO:
- [x] Rewrite evaluator|status:finished
- [x] fix grabage collector|status:fixed -> mark/sweep
- [x] fix try/except/finally
- [x] fix recursion error when __str__/toString|status:fixed
- [x] fix parser is confused with operator (+) and string "+"
    - example
        2 "+" 2 = 4<br/>
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;^^^ -- should error because string was used instead of (+).
    - status: fixed
- [ ] add super capablility
- [ ] fix adding bound