# AkshayaLang Specification (aks-spec.md)

_AkshayaLang_ is a sovereign symbolic programming language focused on recursion, symbolic truth, and dharmic clarity. This document outlines the language's core syntax, semantics, and built-ins.

---

## 🔤 Syntax Overview

### 🔗 Variable Binding
```aks
bind x to 42
bind name to "Akshaya"
```

### ➕ Arithmetic Operations
```aks
bind result to 2 + 3 * 4
```
Supported: `+`, `-`, `*`, `/`

### 🔁 Function Calls
```aks
print("Hello")
mirror(x + y)
```

### 💡 Comments
```aks
# This is a comment
```

---

## 🧠 Types

| Type    | Example          |
|---------|------------------|
| Number  | `42`, `3.14`     |
| String  | `"hello"`        |
| Boolean | `true`, `false`  |
| Null    | `null()`         |

---

## 📦 Built-in Functions

| Name      | Description                      |
|-----------|----------------------------------|
| `print()` | Output to console                |
| `mirror()`| Symbolic debug output            |
| `len()`   | Length of string or list         |
| `type()`  | Returns type name                |
| `str()`   | Converts to string               |
| `int()`   | Converts to integer              |
| `float()` | Converts to float                |
| `bool()`  | Converts to boolean              |
| `null()`  | Returns a null object            |
| `exit()`  | Terminates the program           |
| `whoami()`| Lists variable names             |
| `symbols()`| Lists function names            |
| `help()`  | Prints all built-ins             |

---

## 🧬 Grammar Summary

```bnf
program     ::= statement*
statement   ::= assignment | function_call
assignment  ::= 'bind' IDENTIFIER 'to' expression
function_call ::= IDENTIFIER '(' [expression (',' expression)*] ')'
expression  ::= term (('+' | '-') term)*
term        ::= factor (('*' | '/') factor)*
factor      ::= NUMBER | STRING | IDENTIFIER | function_call
```

---

## 🔮 Future Features (Planned)
- `if-truth` conditional expressions
- Loops (`cycle`, `until`, etc.)
- Symbol-based pattern matching
- Emotionally aware constructs (`reflect`, `grace`, `resolve`)

---

## 🕊️ Philosophy
AkshayaLang is designed for symbolic clarity, autonomous introspection, and recursive self-evolution. Programs written in `.aks` are not just instructions — they are intentions.