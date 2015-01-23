# opcosts.py

This is a microbenchmark that attempts to give a quantitative picture of the
cost of various common operations under the CPython interpreter.

I will avoid reciting the usual dogma about the interpretation of benchmark 
results. Suffice it to say that attempting to time operations in this way is a 
dubious proposition, and the results should be taken with a grain of salt.

### Test Run

Here are the results of a test run under Python 2.7.

```
Python 2.7.2 (default, Jun 12 2011, 14:24:46) [MSC v.1500 64 bit (AMD64)] on win32
```

```
-= Basic Operations =-

       41ns threading.local attribute read
       39ns Integer **
       32ns Bitwise &, |, ^
       31ns Integer /
       30ns Integer << and >>
       26ns Integer *
       26ns Instance attribute read with __slots__
       26ns Instance attribute read
       25ns Integer + and -
       20ns Class attribute read
       19ns Built-in variable read
       16ns Global variable write
       14ns Global variable read
       10ns Local variable read
        5ns Local variable write
        0ns Control, should be about zero

-= Function Overhead =-

      181ns Call to an empty 3-parameter function using both vararg (*) and kwarg (**) expansion
      165ns Call to an empty 3-parameter function using kwarg (**) expansion
      133ns Call to an empty 3-parameter function using vararg (*) expansion
      118ns Call to an empty 3-parameter function
       93ns Call to an empty method with no parameters
       93ns Call to an empty function with a **kwargs parameter
       92ns Call to an empty function with a *args parameter
       84ns Call to an empty nested function with no parameters
       80ns Call to an empty function with no parameters

-= Tuple and List Creation =-

       17ns Creation of an empty list
        6ns Creation of empty tuple

-= Object Creation =-

      556ns Creation of a 4-entry dict from tuples using dict()
      375ns Creation of a 4 item generator using ( n for n in xrange(...) )
      308ns Creation of a 4 item list using list.append()
      236ns Creation of a 4 item list using list += (item,)
      200ns Creation of a 4 item list using list(xrange(...))
      199ns Instantiation of a class with an empty __init__
      174ns Creation of a 4 item list using a [ n for n in xrange(...) ]
      131ns Creation of a 4-entry dict using {...}
      109ns Instantiation of a class by calling __new__
       92ns Creation of a 4 item list using [ k, k, k, k ]
       68ns Instantiation of a class with no __init__
       56ns Instantiation of a class without an __init__ and with __slots__
       54ns Creation of a 4-tuple
       17ns Creation of an empty list
       15ns Creation of empty dict
        6ns Creation of empty tuple

-= Exception Handling =-

      496ns "try...except (E)" block when an exception is raised and caught
      402ns "try...except" block when an exception is raised and caught
       14ns "try...except" block when no exception is raised

-= Built-in Functions =-

      294ns hasattr() when the attribute doesn't exist
      140ns isinstance() when the result is False
       70ns isinstance() when the result is True
       60ns hasattr() when the attribute exists
       56ns type(obj)
       36ns len()

-= Iteration (time per item) =-

       50ns Iteration over a genexpr: time per item
       43ns Iteration over [] (start/stop overhead)
       35ns Iteration over xrange(0) (start/stop overhead)
       13ns Iteration over a chain(repeat(None)): time per item
       12ns Iteration over a list: time per item
       11ns Iteration over an xrange: time per item
        9ns Iteration over a repeat(None): time per item

-= Dictionaries =-

    1,256ns update() an empty dict with a 32-entry dict.
    1,130ns dict.copy() a 32 entry dict
      306ns update() an empty dict passing 4 keyword args
      272ns update() an empty dict with a 4-entry dict.
      166ns dict.copy() a 4 entry dict
       90ns get() on a 32 entry dict
       89ns get() on a 4 entry dict
       82ns pop() on a 32 entry dict
       55ns d[key] = val on a 32 entry dict
       30ns "in" test on a 32 entry dict
       29ns "in" test on a 4 entry dict
       28ns d[key] = val on a 4 entry dict
       26ns d["key"] on a 32 entry dict
       25ns d["key"] on a 4 entry dict
       16ns del d["key"] on a 32 entry dict

-= zip() vs. izip() =-

    4,744ns zip() and iterate over two 100-item lists
    3,533ns izip() and iterate over two 100-item lists
      626ns zip() and iterate over two 8-item lists
      486ns izip() and iterate over two 8-item lists

-= Duck Typing Tests =-

      773ns Attribute access in a try...except when the attribute doesn't exist
      294ns hasattr() when the attribute doesn't exist
      140ns isinstance() when the result is False
       70ns isinstance() when the result is True
       60ns hasattr() when the attribute exists
       56ns type(obj)
       33ns Attribute access in a try...except when the attribute exists
```
