import sys
import time
import operator
from itertools import repeat, chain, izip, count
from collections import defaultdict
import threading

NUM_OPS = 100000
REPETITIONS = 10
       
class Candidate(object):
    name = None
    categories = []
    tags = []
    overheads = []
    
    def __init__(self, num_ops=NUM_OPS):
        self.num_ops = num_ops
        self.times = []
        overheads = []
        for item in self.overheads:
            try:
                tag, multiplier = item
            except ValueError:
                tag, multiplier = item, 1.0
            overheads.append((tag, multiplier))
        self.overheads = overheads
            
    def prepare(self):
        pass
        
    def cleanup(self):
        pass
        
    def run(self, num_ops):
        pass
        
    def time(self):
        timer = self.timer_func
        num_ops = self.num_ops
        t0 = timer()
        self.run(num_ops)
        t = timer() - t0
        self.times.append(t)
        return t
        
    @classmethod
    def setup(cls):
        if sys.platform == "win32":
            cls.timer_func = time.clock
        else:
            cls.timer_func = time.time
                
# Overheads.

class BenchPass(Candidate):
    "A pass statement."
    tags = ["pass"]
    
    def run(self, num_ops):
        pass
        
class BenchStraight(Candidate):
    tags = ["straight"]
    
    def run(self, num_ops):
        for i in xrange(num_ops):
            pass
       
class BenchUnrolled32(Candidate):
    tags = ["unrolled32"]
    
    def run(self, num_ops):
        for i in xrange(0, num_ops, 32):
            pass

class BenchUnrolled100(Candidate):
    tags = ["unrolled100"]
    
    def run(self, num_ops):
        for i in xrange(0, num_ops, 100):
            pass
        
class BenchUnrolled1000(Candidate):
    tags = ["unrolled1000"]
    
    def run(self, num_ops):
        for i in xrange(0, num_ops, 1000):
            pass
        
# Base classes for candidates with particular overheads.  

class Straight(Candidate):
    overheads = ["straight"]

class Unrolled32(Candidate):
    overheads = ["unrolled32"]
        
# Control.

class BenchControl(Straight):
    "Control."
    name = "Control, should be about zero"
    categories = ["basic"]
    
    def run(self, num_ops):
        for i in xrange(num_ops):
            pass
        
# Arithmetic and bitwise logical operators.

class BenchAddSubtract(Unrolled32):
    "In-place integer addition and subtraction from a local variable."    
    name = "Integer + and -"
    categories = ["basic"]

    def run(self, num_ops):
        n = 0
        for n in xrange(0, num_ops, 32):
            n += 1; n -= 1; n += 1; n -= 1; n += 1; n -= 1; n += 1; n -= 1;
            n += 1; n -= 1; n += 1; n -= 1; n += 1; n -= 1; n += 1; n -= 1;
            n += 1; n -= 1; n += 1; n -= 1; n += 1; n -= 1; n += 1; n -= 1;
            n += 1; n -= 1; n += 1; n -= 1; n += 1; n -= 1; n += 1; n -= 1;
        
class BenchMultiply(Unrolled32):
    "In-place integer multiplication of a local variable."
    name = "Integer *"
    categories = ["basic"]
    
    def run(self, num_ops):
        n = 0
        for n in xrange(0, num_ops, 32):
            n *= 1; n *= 1; n *= 1; n *= 1; n *= 1; n *= 1; n *= 1; n *= 1;
            n *= 1; n *= 1; n *= 1; n *= 1; n *= 1; n *= 1; n *= 1; n *= 1;
            n *= 1; n *= 1; n *= 1; n *= 1; n *= 1; n *= 1; n *= 1; n *= 1;
            n *= 1; n *= 1; n *= 1; n *= 1; n *= 1; n *= 1; n *= 1; n *= 1;

class BenchDivide(Unrolled32):
    "In-place integer division of a local variable."
    name = "Integer /"
    categories = ["basic"]
    
    def run(self, num_ops):
        n = 0
        for i in xrange(0, num_ops, 32):
            n /= 1; n /= 1; n /= 1; n /= 1; n /= 1; n /= 1; n /= 1; n /= 1;
            n /= 1; n /= 1; n /= 1; n /= 1; n /= 1; n /= 1; n /= 1; n /= 1;
            n /= 1; n /= 1; n /= 1; n /= 1; n /= 1; n /= 1; n /= 1; n /= 1;
            n /= 1; n /= 1; n /= 1; n /= 1; n /= 1; n /= 1; n /= 1; n /= 1;
        
class BenchShifts(Unrolled32):
    "In-place left and right (arithmetic) shifts on a local variable."
    name = "Integer << and >>"
    categories = ["basic"]
    
    def run(self, num_ops):
        n = 0
        for i in xrange(0, num_ops, 32):
            n <<= 1; n >>= 1; n <<= 1; n >>= 1; n <<= 1; n >>= 1;
            n <<= 1; n >>= 1; n <<= 1; n >>= 1; n <<= 1; n >>= 1;
            n <<= 1; n >>= 1; n <<= 1; n >>= 1; n <<= 1; n >>= 1;
            n <<= 1; n >>= 1; n <<= 1; n >>= 1; n <<= 1; n >>= 1;
            n <<= 1; n >>= 1; n <<= 1; n >>= 1; n <<= 1; n >>= 1;
            n <<= 1; n >>= 1;
        
class BenchBitwiseLogical(Unrolled32):
    "In-place binary bitwise logical operations on a local variable."
    name = "Bitwise &, |, ^"
    categories = ["basic"]
    
    def run(self, num_ops):
        n = 0
        for i in xrange(0, num_ops, 32):
            n &= 1; n |= 1; n ^= 1; n &= 1; n |= 1; n ^= 1;
            n &= 1; n |= 1; n ^= 1; n &= 1; n |= 1; n ^= 1;
            n &= 1; n |= 1; n ^= 1; n &= 1; n |= 1; n ^= 1;
            n &= 1; n |= 1; n ^= 1; n &= 1; n |= 1; n ^= 1;
            n &= 1; n |= 1; n ^= 1; n &= 1; n |= 1; n ^= 1;
            n &= 1; n |= 1;

class BenchPower(Unrolled32):
    "Use of the power operator with non-negative integer arguments on a local variable."
    name = "Integer **"
    categories = ["basic"]
    
    def run(self, num_ops):
        n = 0
        for i in xrange(0, num_ops, 32):
            n **= 0;  n **= 1;  n **= 2;  n **= 3;  n **= 4;  n **= 5; 
            n **= 6;  n **= 7;  n **= 8;  n **= 9;  n **= 10; n **= 11;
            n **= 12; n **= 13; n **= 14; n **= 15; n **= 0;  n **= 1; 
            n **= 2;  n **= 3;  n **= 4;  n **= 5;  n **= 6;  n **= 7; 
            n **= 8;  n **= 9;  n **= 10; n **= 11; n **= 12; n **= 13;
            n **= 14; n **= 15;
       
# Variable access.

G = 123

class LoadBench(Candidate):
    categories = ["basic"]
    overheads = ["unrolled100", ("empty_closure_call", 1e-2)]
    
    def prepare(self):
        def f(a0,  a1,  a2,  a3,  a4,  a5,  a6,  a7, 
              a8,  a9,  a10, a11, a12, a13, a14, a15,
              a16, a17, a18, a19, a20, a21, a22, a23,
              a24, a25, a26, a27, a28, a29, a30, a31,
              a32, a33, a34, a35, a36, a37, a38, a39,
              a40, a41, a42, a43, a44, a45, a46, a47,
              a48, a49, a50, a51, a52, a53, a54, a55,
              a56, a57, a58, a59, a60, a61, a62, a63,
              a64, a65, a66, a67, a68, a69, a70, a71,
              a72, a73, a74, a75, a76, a77, a78, a79,
              a80, a81, a82, a83, a84, a85, a86, a87,
              a88, a89, a90, a91, a92, a93, a94, a95,
              a96, a97, a98, a99):
            pass        
        self.f = f


class BenchLoadLocal(LoadBench):
    "Local variable reads."
    name = "Local variable read"
    categories = ["basic"]
    overheads = ["unrolled100", ("empty_closure_call", 1e-2)]
    
    def run(self, num_ops):
        # The result of this is still high by about a factor of two, so another
        # approach is needed. I can't think of a way to measure and subtract
        # the overhead of POP_TOPs, or to do the pops for free.
                
        k = 123
        f = self.f
        for i in xrange(0, num_ops, 100):
            f(k, k, k, k, k, k, k, k, k, k, k, k, k, k, k, k,
              k, k, k, k, k, k, k, k, k, k, k, k, k, k, k, k,
              k, k, k, k, k, k, k, k, k, k, k, k, k, k, k, k,
              k, k, k, k, k, k, k, k, k, k, k, k, k, k, k, k,
              k, k, k, k, k, k, k, k, k, k, k, k, k, k, k, k,
              k, k, k, k, k, k, k, k, k, k, k, k, k, k, k, k,
              k, k, k, k)
            
class BenchLoadGlobal(LoadBench):
    "Global variable read."
    name = "Global variable read"
    categories = ["basic"]
    
    def run(self, num_ops):
        f = self.f
        for i in xrange(0, num_ops, 100):
            f(G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G,
              G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G,
              G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G,
              G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G,
              G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G,
              G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G,
              G, G, G, G)

class BenchStoreLocal(Unrolled32):
    "Storage of a constant into a local variable."
    name = "Local variable write"
    categories = ["basic"]
    
    def run(self, num_ops):
        for i in xrange(0, num_ops, 32):
            (n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n,
             n, n, n, n, n, n, n, n, n, n, n, n, n, n, n, n) = \
            (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            
class BenchStoreGlobal(Unrolled32):
    "Storage of a constant into a global variable."
    name = "Global variable write"
    categories = ["basic"]
    
    def run(self, num_ops):
        global G
        for i in xrange(0, num_ops, 32):
            (G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G,
             G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G) = \
            (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

class BenchLoadBuiltin(Unrolled32):
    "Read of a variable in the builtin namespace."
    name = "Built-in variable read"
    categories = ["basic"]
    
    def run(self, num_ops):
        for i in xrange(0, num_ops, 32):
            abs;        all;         any;       apply;    
            basestring; bool;        buffer;    callable; 
            chr;        classmethod; cmp;       coerce;   
            compile;    complex;     copyright; credits;  
            delattr;    dict;        dir;       divmod;   
            enumerate;  eval;        execfile;  exit;     
            file;       filter;      float;     frozenset;
            getattr;    globals;     hasattr;   hash;               

class AbcReader(Unrolled32):
    def run(self, num_ops):
       o = self.o
       for i in xrange(0, num_ops, 32):
           o.a; o.b; o.c; o.a;
           o.b; o.c; o.a; o.b;
           o.c; o.a; o.b; o.c;
           o.a; o.b; o.c; o.a;
           o.b; o.c; o.a; o.b;
           o.c; o.a; o.b; o.c;
           o.a; o.b; o.c; o.a;
           o.b; o.c; o.a; o.b;    
        
class BenchAttrReadInstance(AbcReader):
    "Read of an attribute from an object instance dictionary."
    name = "Instance attribute read"
    categories = ["basic"]
    
    def prepare(self):
        class AbcInInstance(object):
            def __init__(self):
                self.a = 1
                self.b = 2
                self.c = 3
        self.o = AbcInInstance()
        
class BenchAttrReadClass(AbcReader):
    "Read of an attribute from a class dictionary."
    name = "Class attribute read"
    categories = ["basic"]
    
    def prepare(self):
        class AbcInClass(object):
            a = 1
            b = 2
            c = 3
        self.o = AbcInClass()

class BenchAttrReadSlots(AbcReader):
    "Reads of a variables from __slots__ descriptors."
    name = "Instance attribute read with __slots__"
    categories = ["basic"]
    
    def prepare(self):
        class AbcInSlots(object):
            __slots__ = ("a", "b", "c")
            def __init__(self):
                self.a = 1
                self.b = 2
                self.c = 3
        self.o = AbcInSlots()
        
class BenchThreadingLocalRead(AbcReader):
    "Read of an attribute of a threading.locals object."
    name = "threading.local attribute read"
    categories = ["basic"]
    
    def prepare(self):
        tls = threading.local()
        tls.a = 1
        tls.b = 2
        tls.c = 3
        self.o = tls

# Function call overhead.

def nop(): pass
def nop_varargs(*args): pass
def nop_kwargs(**kwargs): pass
def nop3(a, b, c): pass

class CallNoArgsBase(Unrolled32):
    categories = ["function"]
    
    def run(self, num_ops):
        f = self.func
        for i in xrange(0, num_ops, 32):
            f(); f(); f(); f(); f(); f(); f(); f();
            f(); f(); f(); f(); f(); f(); f(); f();
            f(); f(); f(); f(); f(); f(); f(); f();
            f(); f(); f(); f(); f(); f(); f(); f();
                      
    
class BenchCallEmptyFunction(CallNoArgsBase):
    "Call to an empty function."
    name = "Call to an empty function with no parameters"
    
    def prepare(self):
        self.func = nop
            
class BenchCallEmptyMethod(CallNoArgsBase):
    "Calls to a bound method object."
    name = "Call to an empty method with no parameters"
    
    def prepare(self):
        class C(object):
            def m(self):
                pass
        o = C()
        self.func = o.m
 
class BenchCallEmptyClosure(CallNoArgsBase):
    "Calls to an empty nested function."
    name = "Call to an empty nested function with no parameters"
    tags = ["empty_closure_call"]
    
    def prepare(self):
        def f():
            pass
        self.func = f

class BenchCallEmptyVarargs(CallNoArgsBase):
    "Calls to an empty function with a * parameter. No arguments are passed."
    name = "Call to an empty function with a *args parameter"
    
    def prepare(self):
        self.func = nop_varargs

class BenchCallEmptyKwargs(CallNoArgsBase):
    "Calls to an empty function with a ** parameter. No arguments are passed."
    name = "Call to an empty function with a **kwargs parameter"
    
    def prepare(self):
        self.func = nop_kwargs
        
class BenchCall3Positional(Unrolled32):
    "Call to an empty function with three formal parameters using positional " \
    "arguments."
    name = "Call to an empty 3-parameter function"
    categories = ["function"]
    
    def run(self, num_ops):
        f = nop3
        for i in xrange(0, num_ops, 32):
             f(1, 2, 3); f(1, 2, 3); f(1, 2, 3); f(1, 2, 3);
             f(1, 2, 3); f(1, 2, 3); f(1, 2, 3); f(1, 2, 3);
             f(1, 2, 3); f(1, 2, 3); f(1, 2, 3); f(1, 2, 3);
             f(1, 2, 3); f(1, 2, 3); f(1, 2, 3); f(1, 2, 3);
             f(1, 2, 3); f(1, 2, 3); f(1, 2, 3); f(1, 2, 3);
             f(1, 2, 3); f(1, 2, 3); f(1, 2, 3); f(1, 2, 3);
             f(1, 2, 3); f(1, 2, 3); f(1, 2, 3); f(1, 2, 3);
             f(1, 2, 3); f(1, 2, 3); f(1, 2, 3); f(1, 2, 3);
            
class BenchCall3VarargExpand(Unrolled32):
    "Call to an empty function with three formal parameters using vararg " \
    "expansion."
    name = "Call to an empty 3-parameter function using vararg (*) expansion"
    categories = ["function"]
    
    def run(self, num_ops):
        f = nop3
        a = (1, 2, 3)
        for i in xrange(0, num_ops, 32):
             f(*a); f(*a); f(*a); f(*a);
             f(*a); f(*a); f(*a); f(*a);
             f(*a); f(*a); f(*a); f(*a);
             f(*a); f(*a); f(*a); f(*a);
             f(*a); f(*a); f(*a); f(*a);
             f(*a); f(*a); f(*a); f(*a);
             f(*a); f(*a); f(*a); f(*a);
             f(*a); f(*a); f(*a); f(*a);
            
class BenchCall3KwargExpand(Unrolled32):
    "Call to an empty function with three formal parameters using kwarg (**) " \
    "expansion."
    name = "Call to an empty 3-parameter function using kwarg (**) expansion"
    categories = ["function"]
    
    def prepare(self):
        self.a = { "a": 1, "b": 2, "c": 3 }
    
    def run(self, num_ops):
        f = nop3
        a = self.a
        for i in xrange(0, num_ops, 32):
             f(**a); f(**a); f(**a); f(**a);
             f(**a); f(**a); f(**a); f(**a);
             f(**a); f(**a); f(**a); f(**a);
             f(**a); f(**a); f(**a); f(**a);
             f(**a); f(**a); f(**a); f(**a);
             f(**a); f(**a); f(**a); f(**a);
             f(**a); f(**a); f(**a); f(**a);
             f(**a); f(**a); f(**a); f(**a);
            
class BenchCall3BothExpands(Unrolled32):
    "Call to an empty function with three formal parameters using both " \
    "vararg (*) and kwarg (**) expansion."
    name = "Call to an empty 3-parameter function using both vararg (*) and " \
    "kwarg (**) expansion"
    categories = ["function"]
    
    def prepare(self):
        self.b = { "b": 2, "c": 3 }
    
    def run(self, num_ops):
        f = nop3
        a = (1,)
        b = self.b
        for i in xrange(0, num_ops, 32):
             f(*a, **b); f(*a, **b); f(*a, **b); f(*a, **b);
             f(*a, **b); f(*a, **b); f(*a, **b); f(*a, **b);
             f(*a, **b); f(*a, **b); f(*a, **b); f(*a, **b);
             f(*a, **b); f(*a, **b); f(*a, **b); f(*a, **b);
             f(*a, **b); f(*a, **b); f(*a, **b); f(*a, **b);
             f(*a, **b); f(*a, **b); f(*a, **b); f(*a, **b);
             f(*a, **b); f(*a, **b); f(*a, **b); f(*a, **b);
             f(*a, **b); f(*a, **b); f(*a, **b); f(*a, **b);             

# Built-in type construction.

class BenchCreateEmptyTuple(Unrolled32):
    "Building empty tuples. Actually just loads constants."
    name = "Creation of empty tuple"
    categories = ["object_creation", "list"]
    
    def run(self, num_ops):
        for i in xrange(0, num_ops, 32):
            (); (); (); (); (); (); (); (); (); (); (); (); (); (); (); ();
            (); (); (); (); (); (); (); (); (); (); (); (); (); (); (); ();
        
class BenchCreateTuple4(Unrolled32):
    "Creation of 4-tuples from local variables."
    name = "Creation of a 4-tuple"
    categories = ["object_creation"]
    
    def run(self, num_ops):
        k = 123
        for i in xrange(0, num_ops, 32):
            (k, k, k, k); (k, k, k, k); (k, k, k, k); (k, k, k, k);
            (k, k, k, k); (k, k, k, k); (k, k, k, k); (k, k, k, k);
            (k, k, k, k); (k, k, k, k); (k, k, k, k); (k, k, k, k);
            (k, k, k, k); (k, k, k, k); (k, k, k, k); (k, k, k, k);
            (k, k, k, k); (k, k, k, k); (k, k, k, k); (k, k, k, k);
            (k, k, k, k); (k, k, k, k); (k, k, k, k); (k, k, k, k);
            (k, k, k, k); (k, k, k, k); (k, k, k, k); (k, k, k, k);
            (k, k, k, k); (k, k, k, k); (k, k, k, k); (k, k, k, k);            
        
class BenchCreateEmptyList(Unrolled32):
    "Creation of empty lists."
    name = "Creation of an empty list"
    categories = ["object_creation", "list"]
    
    def run(self, num_ops):
        for i in xrange(0, num_ops, 32):
            []; []; []; []; []; []; []; []; []; []; []; []; []; []; []; [];
            []; []; []; []; []; []; []; []; []; []; []; []; []; []; []; [];
        
class BenchCreateList4(Unrolled32):
    "Creation of 4 item lists from local variables."
    name = "Creation of a 4 item list using [ k, k, k, k ]"
    categories = ["object_creation"]
    
    def run(self, num_ops):
        k = 123
        for i in xrange(0, num_ops, 32):
           [ k, k, k, k ]; [ k, k, k, k ]; [ k, k, k, k ]; [ k, k, k, k ];
           [ k, k, k, k ]; [ k, k, k, k ]; [ k, k, k, k ]; [ k, k, k, k ];
           [ k, k, k, k ]; [ k, k, k, k ]; [ k, k, k, k ]; [ k, k, k, k ];
           [ k, k, k, k ]; [ k, k, k, k ]; [ k, k, k, k ]; [ k, k, k, k ];
           [ k, k, k, k ]; [ k, k, k, k ]; [ k, k, k, k ]; [ k, k, k, k ];
           [ k, k, k, k ]; [ k, k, k, k ]; [ k, k, k, k ]; [ k, k, k, k ];
           [ k, k, k, k ]; [ k, k, k, k ]; [ k, k, k, k ]; [ k, k, k, k ];
           [ k, k, k, k ]; [ k, k, k, k ]; [ k, k, k, k ]; [ k, k, k, k ];
                       
        
class BenchCreateEmptyDict(Unrolled32):
    "Creation of an empty dictionary."
    name = "Creation of empty dict"
    categories = ["object_creation"]
    tags = ["create_empty_dict"]
    
    def run(self, num_ops):
        for i in xrange(0, num_ops, 32):
            {}; {}; {}; {}; {}; {}; {}; {}; {}; {}; {}; {}; {}; {}; {}; {};
            {}; {}; {}; {}; {}; {}; {}; {}; {}; {}; {}; {}; {}; {}; {}; {};
        
class BenchBuildDict4(Unrolled32):
    "Creation of 4-entry dict from constants."
    name = "Creation of a 4-entry dict using {...}"
    categories = ["object_creation"]
    
    def run(self, num_ops):
        for i in xrange(0, num_ops, 32):
            { "a": 0, "b": 1, "c": 2, "d": 3 };
            { "e": 0, "f": 1, "g": 2, "h": 3 };
            { "i": 0, "j": 1, "k": 2, "l": 3 };
            { "m": 0, "n": 1, "o": 2, "p": 3 };
            { "q": 0, "r": 1, "s": 2, "t": 3 };
            { "u": 0, "v": 1, "w": 2, "x": 3 };
            { "y": 0, "z": 1, "a": 2, "b": 3 };
            { "c": 0, "d": 1, "e": 2, "f": 3 };
            { "g": 0, "h": 1, "i": 2, "j": 3 };
            { "k": 0, "l": 1, "m": 2, "n": 3 };
            { "o": 0, "p": 1, "q": 2, "r": 3 };
            { "s": 0, "t": 1, "u": 2, "v": 3 };
            { "w": 0, "x": 1, "y": 2, "z": 3 };
            { "a": 0, "b": 1, "c": 2, "d": 3 };
            { "e": 0, "f": 1, "g": 2, "h": 3 };
            { "i": 0, "j": 1, "k": 2, "l": 3 };
            { "m": 0, "n": 1, "o": 2, "p": 3 };
            { "q": 0, "r": 1, "s": 2, "t": 3 };
            { "u": 0, "v": 1, "w": 2, "x": 3 };
            { "y": 0, "z": 1, "a": 2, "b": 3 };
            { "c": 0, "d": 1, "e": 2, "f": 3 };
            { "g": 0, "h": 1, "i": 2, "j": 3 };
            { "k": 0, "l": 1, "m": 2, "n": 3 };
            { "o": 0, "p": 1, "q": 2, "r": 3 };
            { "s": 0, "t": 1, "u": 2, "v": 3 };
            { "w": 0, "x": 1, "y": 2, "z": 3 };
            { "a": 0, "b": 1, "c": 2, "d": 3 };
            { "e": 0, "f": 1, "g": 2, "h": 3 };
            { "i": 0, "j": 1, "k": 2, "l": 3 };
            { "m": 0, "n": 1, "o": 2, "p": 3 };
            { "q": 0, "r": 1, "s": 2, "t": 3 };
            { "u": 0, "v": 1, "w": 2, "x": 3 };            

class BenchCreateDict4WithConstructor(Unrolled32):
    "Creation of 4 entry dict using dict()."
    name = "Creation of a 4-entry dict from tuples using dict()"
    categories = ["object_creation"]
    DATA = (("a", 0), ("b", 1), ("c", 2), ("d", 3))
    
    def run(self, num_ops):
        d = self.DATA
        f = dict
        for i in xrange(0, num_ops, 32):
            f(d); f(d); f(d); f(d); f(d); f(d); f(d); f(d);
            f(d); f(d); f(d); f(d); f(d); f(d); f(d); f(d);
            f(d); f(d); f(d); f(d); f(d); f(d); f(d); f(d);
            f(d); f(d); f(d); f(d); f(d); f(d); f(d); f(d);            
        
# Object creation.
    
class BenchObjectCreation(Unrolled32):
    "Instantiation of a completely empty class (no __init__)."
    name = "Instantiation of a class with no __init__"
    categories = ["object_creation"]
    
    def run(self, num_ops):
        class C(object):
            pass
        for i in xrange(0, num_ops, 32):
            C(); C(); C(); C(); C(); C(); C(); C();
            C(); C(); C(); C(); C(); C(); C(); C();
            C(); C(); C(); C(); C(); C(); C(); C();
            C(); C(); C(); C(); C(); C(); C(); C();

         
class BenchObjectCreationWithSlots(Unrolled32):
    "Instantiation of a class with empty __slots__ and without __init__."
    name = "Instantiation of a class without an __init__ and with __slots__"
    categories = ["object_creation"]
    
    def run(self, num_ops):
        class C(object):
            __slots__ = ()
        for i in xrange(0, num_ops, 32):
            C(); C(); C(); C(); C(); C(); C(); C();
            C(); C(); C(); C(); C(); C(); C(); C();
            C(); C(); C(); C(); C(); C(); C(); C();
            C(); C(); C(); C(); C(); C(); C(); C();
            
class BenchObjectCreationWithInit(Unrolled32):
    "Instantiation of a class with an empty __init__."
    name = "Instantiation of a class with an empty __init__"
    categories = ["object_creation"]
    
    def run(self, num_ops):
        class C(object):
            def __init__(self):
                pass
        for i in xrange(0, num_ops, 32):
            C(); C(); C(); C(); C(); C(); C(); C();
            C(); C(); C(); C(); C(); C(); C(); C();
            C(); C(); C(); C(); C(); C(); C(); C();
            C(); C(); C(); C(); C(); C(); C(); C();
            
class BenchObjectNew(Unrolled32):
    "Instantiation of a class by calling __new__."
    name = "Instantiation of a class by calling __new__"
    categories = ["object_creation"]
    
    def run(self, num_ops):
        class C(object):
            pass
        
        for i in xrange(0, num_ops, 32):
            C.__new__(C); C.__new__(C); C.__new__(C); C.__new__(C);
            C.__new__(C); C.__new__(C); C.__new__(C); C.__new__(C);
            C.__new__(C); C.__new__(C); C.__new__(C); C.__new__(C);
            C.__new__(C); C.__new__(C); C.__new__(C); C.__new__(C);
            C.__new__(C); C.__new__(C); C.__new__(C); C.__new__(C);
            C.__new__(C); C.__new__(C); C.__new__(C); C.__new__(C);
            C.__new__(C); C.__new__(C); C.__new__(C); C.__new__(C);
            C.__new__(C); C.__new__(C); C.__new__(C); C.__new__(C);            
       
# List comprehensions and generators.

class BenchListComp4(Unrolled32):
    "Creation of 4 item lists from an xrange iterable using a comprehension."
    name = "Creation of a 4 item list using a [ n for n in xrange(...) ]"
    categories = ["object_creation"]
    
    def run(self, num_ops):
        s = xrange(4)
        for i in xrange(0, num_ops, 32):
            [ n for n in s ]; [ n for n in s ]; [ n for n in s ];
            [ n for n in s ]; [ n for n in s ]; [ n for n in s ];
            [ n for n in s ]; [ n for n in s ]; [ n for n in s ];
            [ n for n in s ]; [ n for n in s ]; [ n for n in s ];
            [ n for n in s ]; [ n for n in s ]; [ n for n in s ];
            [ n for n in s ]; [ n for n in s ]; [ n for n in s ];
            [ n for n in s ]; [ n for n in s ]; [ n for n in s ];
            [ n for n in s ]; [ n for n in s ]; [ n for n in s ];
            [ n for n in s ]; [ n for n in s ]; [ n for n in s ];
            [ n for n in s ]; [ n for n in s ]; [ n for n in s ];
            [ n for n in s ]; [ n for n in s ];
        
class BenchGenExpr4(Unrolled32):
    "Creation of a 4 item iterator using a generator expression."
    name = "Creation of a 4 item generator using ( n for n in xrange(...) )"
    categories = ["object_creation"]
    
    def run(self, num_ops):
       s = xrange(4)
       for i in xrange(0, num_ops, 32):
           ( n for n in s ); ( n for n in s ); ( n for n in s );
           ( n for n in s ); ( n for n in s ); ( n for n in s );
           ( n for n in s ); ( n for n in s ); ( n for n in s );
           ( n for n in s ); ( n for n in s ); ( n for n in s );
           ( n for n in s ); ( n for n in s ); ( n for n in s );
           ( n for n in s ); ( n for n in s ); ( n for n in s );
           ( n for n in s ); ( n for n in s ); ( n for n in s );
           ( n for n in s ); ( n for n in s ); ( n for n in s );
           ( n for n in s ); ( n for n in s ); ( n for n in s );
           ( n for n in s ); ( n for n in s ); ( n for n in s );
           ( n for n in s ); ( n for n in s );
        
class BenchCreateListAppend4(Candidate):
    "Creation of 4 item lists using list.append()."
    name = "Creation of a 4 item list using list.append()"
    categories = ["object_creation"]
    overheads = ["straight"]
       
    def run(self, num_ops):
        for i in xrange(num_ops):
            l = []
            l.append(0); l.append(1); l.append(2); l.append(3)
            
class BenchCreateListExtend4(Candidate):
    "Creation of 4 item lists using list += (item,)."
    name = "Creation of a 4 item list using list += (item,)"
    categories = ["object_creation"]
    overheads = ["straight"]
       
    def run(self, num_ops):
        for i in xrange(num_ops):
            l = []
            l += 0,; l += 1,; l += 2,; l += 3,
            
class BenchCreateList4WithConstructor(Straight):
    "Creation of a 4 item list from an xrange iterable using list()."
    name = "Creation of a 4 item list using list(xrange(...))"
    categories = ["object_creation"]
    
    def run(self, num_ops):
        s = xrange(4)
        f = list
        for i in xrange(num_ops):
            f(s)

# Iteration.

class BenchIterationGenExpr(Candidate):
    "Iteration over an iterator created by a generator expression."
    name = "Iteration over a genexpr: time per item"
    categories = ["iteration"]
    overheads = ["pass"]

    def prepare(self):
        self.iterator = (i for i in xrange(self.num_ops))
    
    def run(self, num_ops): 
        for item in self.iterator:
            pass
        
class BenchIterationList(Candidate):
    "Iteration over a list."
    name = "Iteration over a list: time per item"
    categories = ["iteration"]
    overheads = ["unrolled1000"]
    
    def prepare(self):
        self.data = [ i for i in xrange(1000) ]
    
    def run(self, num_ops):
        # This doesn't use one mammoth list so the data fits in L1.
        data = self.data
        for i in xrange(0, num_ops, 1000):
            for item in data:
                pass
            
class IterationOverheadBench(Unrolled32):
    categories = ["iteration"]
    
    def run(self, num_ops):
        it = self.iterable
        for i in xrange(0, num_ops, 32):
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            for x in it: pass
            
        
class BenchIterationOverheadList(IterationOverheadBench):
    "Iteration over an empty list."
    name = "Iteration over [] (start/stop overhead)"
    categories = ["iteration"]
    iterable = []
    
class BenchIterationOverheadXrange(IterationOverheadBench):
    "Iteration over an xrange(0)."
    name = "Iteration over xrange(0) (start/stop overhead)"
    categories = ["iteration"]
    iterable = xrange(0)
            
class BenchIterationXrange(Candidate):
    "Iteration over an xrange object."
    name = "Iteration over an xrange: time per item"
    categories = ["iteration"]
    overheads = ["pass"]
    
    def run(self, num_ops):
        for item in xrange(num_ops):
            pass
          
class BenchIterationRepeat(Candidate):
    "Iteration over an itertools repeat object."
    name = "Iteration over a repeat(None): time per item"
    categories = ["iteration"]
    overheads = ["pass"]
    
    def run(self, num_ops):
        for item in repeat(None, NUM_OPS):
            pass
        
class BenchIterationChainedRepeat(Candidate):
    "Iteration over an itertools chain made from repeat iterators."
    name = "Iteration over a chain(repeat(None)): time per item"
    categories = ["iteration"]
    overheads = ["pass"]

    def prepare(self):
        ranges = [ repeat(None, 1000) for i in xrange(0, self.num_ops, 1000) ]
        self.iterator = chain(*ranges)
    
    def run(self, num_ops):
        for item in self.iterator:
            pass
        
# Zip functions.

class Zip2BenchBase(Unrolled32):
    def prepare(self):
        self.list_a = [ i for i in xrange(self.LIST_SIZE) ]
        self.list_b = [ i for i in xrange(self.LIST_SIZE) ]
    
    def run(self, num_ops):
        f = self.zipfunc
        a = self.list_a
        b = self.list_b
        for i in xrange(0, num_ops, 32):
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
            for p in f(a, b): pass
                   
class BenchZip8(Zip2BenchBase):
    "Creation of and iteration over a 'zip' zip of two 8-item lists."
    name = "zip() and iterate over two 8-item lists"
    categories = ["zip"]
    zipfunc = zip
    LIST_SIZE = 8
    
class BenchIzip8(Zip2BenchBase):
    "Creation of and iteration over an 'izip' zip of two 8-item lists."
    name = "izip() and iterate over two 8-item lists"
    categories = ["zip"]
    zipfunc = izip
    LIST_SIZE = 8
    
class BenchZip100(Zip2BenchBase):
    "Creation of and iteration over a 'zip' zip of two 100-item lists."
    name = "zip() and iterate over two 100-item lists"
    categories = ["zip"]
    zipfunc = zip
    LIST_SIZE = 100

class BenchIzip100(Zip2BenchBase):
    "Creation of and iteration over an 'izip' zip of two 100-item lists."
    name = "izip() and iterate over two 100-item lists"
    categories = ["zip"]
    zipfunc = izip
    LIST_SIZE = 100

# Dictionary tests.

class DictBench(Unrolled32):
    categories = ["dict"]
    
    DICT4 = dict([ ("item %d" % i, i) for i in xrange(4) ])
    DICT32 = dict([ ("item %d" % i, i) for i in xrange(32) ])
      
class BenchDict4Lookup(DictBench):
    "Lookups in a 4-entry dictionary."
    name = 'd["key"] on a 4 entry dict'
    
    def run(self, num_ops):   
        d = self.DICT4
        for i in xrange(0, num_ops, 32):
            d["item 0"]; d["item 1"]; d["item 2"]; d["item 3"];
            d["item 0"]; d["item 1"]; d["item 2"]; d["item 3"];
            d["item 0"]; d["item 1"]; d["item 2"]; d["item 3"];
            d["item 0"]; d["item 1"]; d["item 2"]; d["item 3"];
            d["item 0"]; d["item 1"]; d["item 2"]; d["item 3"];
            d["item 0"]; d["item 1"]; d["item 2"]; d["item 3"];
            d["item 0"]; d["item 1"]; d["item 2"]; d["item 3"];
            d["item 0"]; d["item 1"]; d["item 2"]; d["item 3"];            
            
class BenchDict32Lookup(DictBench):
    "Lookups in a 32-entry dictionary."
    name = 'd["key"] on a 32 entry dict'
    
    def run(self, num_ops):
        d = self.DICT32
        for i in xrange(0, num_ops, 32):
            d["item 0"];  d["item 1"];  d["item 2"];  d["item 3"]; 
            d["item 4"];  d["item 5"];  d["item 6"];  d["item 7"]; 
            d["item 8"];  d["item 9"];  d["item 10"]; d["item 11"];
            d["item 12"]; d["item 13"]; d["item 14"]; d["item 15"];
            d["item 16"]; d["item 17"]; d["item 18"]; d["item 19"];
            d["item 20"]; d["item 21"]; d["item 22"]; d["item 23"];
            d["item 24"]; d["item 25"]; d["item 26"]; d["item 27"];
            d["item 28"]; d["item 29"]; d["item 30"]; d["item 31"];            
        
class BenchDict4In(DictBench):
    '"in" operator tests on a 4-entry dictionary.'
    name = '"in" test on a 4 entry dict'

    def run(self, num_ops):
        d = self.DICT4
        for i in xrange(0, num_ops, 32):
            "item 0" in d; "item 1" in d; "item 2" in d; "item 3" in d;
            "item 0" in d; "item 1" in d; "item 2" in d; "item 3" in d;
            "item 0" in d; "item 1" in d; "item 2" in d; "item 3" in d;
            "item 0" in d; "item 1" in d; "item 2" in d; "item 3" in d;
            "item 0" in d; "item 1" in d; "item 2" in d; "item 3" in d;
            "item 0" in d; "item 1" in d; "item 2" in d; "item 3" in d;
            "item 0" in d; "item 1" in d; "item 2" in d; "item 3" in d;
            "item 0" in d; "item 1" in d; "item 2" in d; "item 3" in d;
            
class BenchDict32In(DictBench):
    '"in" operator tests on a 32-entry dictionary.'
    name = '"in" test on a 32 entry dict'
    
    def run(self, num_ops):
        d = self.DICT32
        for i in xrange(0, num_ops, 32):
             "item 0" in d;  "item 1" in d;  "item 2" in d;  "item 3" in d; 
             "item 4" in d;  "item 5" in d;  "item 6" in d;  "item 7" in d; 
             "item 8" in d;  "item 9" in d;  "item 10" in d; "item 11" in d;
             "item 12" in d; "item 13" in d; "item 14" in d; "item 15" in d;
             "item 16" in d; "item 17" in d; "item 18" in d; "item 19" in d;
             "item 20" in d; "item 21" in d; "item 22" in d; "item 23" in d;
             "item 24" in d; "item 25" in d; "item 26" in d; "item 27" in d;
             "item 28" in d; "item 29" in d; "item 30" in d; "item 31" in d;             
        
class BenchDict4Get(DictBench):
    "get() calls on a 4-entry dictionary."
    name = "get() on a 4 entry dict"
    
    def run(self, num_ops):
        d = self.DICT4
        for i in xrange(0, num_ops, 32):
            d.get("item 0"); d.get("item 1"); d.get("item 2");
            d.get("item 3"); d.get("item 0"); d.get("item 1");
            d.get("item 2"); d.get("item 3"); d.get("item 0");
            d.get("item 1"); d.get("item 2"); d.get("item 3");
            d.get("item 0"); d.get("item 1"); d.get("item 2");
            d.get("item 3"); d.get("item 0"); d.get("item 1");
            d.get("item 2"); d.get("item 3"); d.get("item 0");
            d.get("item 1"); d.get("item 2"); d.get("item 3");
            d.get("item 0"); d.get("item 1"); d.get("item 2");
            d.get("item 3"); d.get("item 0"); d.get("item 1");
            d.get("item 2"); d.get("item 3");
            
            
class BenchDict32Get(DictBench):
    "get() calls on a 32-entry dictionary."
    name = "get() on a 32 entry dict"
    
    def run(self, num_ops):
        d = self.DICT32
        for i in xrange(0, num_ops, 32):
            d.get("item 0");  d.get("item 1");  d.get("item 2"); 
            d.get("item 3");  d.get("item 4");  d.get("item 5"); 
            d.get("item 6");  d.get("item 7");  d.get("item 8"); 
            d.get("item 9");  d.get("item 10"); d.get("item 11");
            d.get("item 12"); d.get("item 13"); d.get("item 14");
            d.get("item 15"); d.get("item 16"); d.get("item 17");
            d.get("item 18"); d.get("item 19"); d.get("item 20");
            d.get("item 21"); d.get("item 22"); d.get("item 23");
            d.get("item 24"); d.get("item 25"); d.get("item 26");
            d.get("item 27"); d.get("item 28"); d.get("item 29");
            d.get("item 30"); d.get("item 31");            
            
class BenchDict4Assign(DictBench):
    "Item assignment to a 4-entry dictionary."
    name = "d[key] = val on a 4 entry dict"
    overheads = ["unrolled32", ("create_empty_dict", 1.0 / 32.0)]
       
    def run(self, num_ops):
        for i in xrange(0, num_ops, 32):
            d = {}
            d["item 0"] = 0;  d["item 1"] = 1;  d["item 2"] = 2; 
            d["item 3"] = 3;  d["item 0"] = 4;  d["item 1"] = 5; 
            d["item 2"] = 6;  d["item 3"] = 7;  d["item 0"] = 8; 
            d["item 1"] = 9;  d["item 2"] = 10; d["item 3"] = 11;
            d["item 0"] = 12; d["item 1"] = 13; d["item 2"] = 14;
            d["item 3"] = 15; d["item 0"] = 16; d["item 1"] = 17;
            d["item 2"] = 18; d["item 3"] = 19; d["item 0"] = 20;
            d["item 1"] = 21; d["item 2"] = 22; d["item 3"] = 23;
            d["item 0"] = 24; d["item 1"] = 25; d["item 2"] = 26;
            d["item 3"] = 27; d["item 0"] = 28; d["item 1"] = 29;
            d["item 2"] = 30; d["item 3"] = 31;            
            
class BenchDict32Assign(DictBench):
    "Item assignment to a 32-entry dictionary."
    name = "d[key] = val on a 32 entry dict"
    overheads = ["unrolled32", ("create_empty_dict", 1.0 / 32.0)]
   
    def run(self, num_ops):
        for i in xrange(0, num_ops, 32):
            d = {}
            d["item 0"] = 0;   d["item 1"] = 1;   d["item 2"] = 2;  
            d["item 3"] = 3;   d["item 4"] = 4;   d["item 5"] = 5;  
            d["item 6"] = 6;   d["item 7"] = 7;   d["item 8"] = 8;  
            d["item 9"] = 9;   d["item 10"] = 10; d["item 11"] = 11;
            d["item 12"] = 12; d["item 13"] = 13; d["item 14"] = 14;
            d["item 15"] = 15; d["item 16"] = 16; d["item 17"] = 17;
            d["item 18"] = 18; d["item 19"] = 19; d["item 20"] = 20;
            d["item 21"] = 21; d["item 22"] = 22; d["item 23"] = 23;
            d["item 24"] = 24; d["item 25"] = 25; d["item 26"] = 26;
            d["item 27"] = 27; d["item 28"] = 28; d["item 29"] = 29;
            d["item 30"] = 30; d["item 31"] = 31; 
            
class BenchDict4Copy(DictBench):
    "dict.copy() on a 4-entry dict."
    name = "dict.copy() a 4 entry dict"
    tags = ["dict4_copy"]
    overheads = ["straight"]
    
    def run(self, num_ops):
        d = self.DICT4
        f = dict.copy
        for i in xrange(num_ops):
            f(d)
            
class BenchDict32Copy(DictBench):
    "dict.copy() on a 32-entry dict."
    name = "dict.copy() a 32 entry dict"
    tags = ["dict32_copy"]
    overheads = ["straight"]
    
    def run(self, num_ops):
        d = self.DICT32
        f = dict.copy
        for i in xrange(num_ops):
            f(d)
            
class BenchDict4Update(DictBench):
    "dict.update() an empty dict with a 4-entry dict."
    name = "update() an empty dict with a 4-entry dict."
    overheads = ["straight", "create_empty_dict"]
    
    def run(self, num_ops):
        s = self.DICT4
        f = dict.update
        for i in xrange(num_ops):
            f({}, s)
            
class BenchDict32Update(DictBench):
    "dict.update() an empty dict with a 32-entry dict."
    name = "update() an empty dict with a 32-entry dict."
    overheads = ["straight", "create_empty_dict"]
    
    def run(self, num_ops):
        s = self.DICT32
        f = dict.update
        for i in xrange(num_ops):
            f({}, s)
            
class BenchDict4UpdateKwargs(DictBench):
    "dict.update() an empty dict passing 4 keyword args."
    name = "update() an empty dict passing 4 keyword args"
    overheads = ["straight", "create_empty_dict"]
    
    def run(self, num_ops):
        s = self.DICT4
        f = dict.update
        for i in xrange(num_ops):
            f({}, a=1, b=2, c=3, d=4)


class BenchDict32Pop(DictBench):
    "dict.pop() on a 32 entry dictionary."
    name = "pop() on a 32 entry dict"
    categories = ["dict"]
    overheads = ["unrolled32", ("dict32_copy", 1.0 / 32.0)]
    
    def run(self, num_ops):
        src = self.DICT32
        for i in xrange(0, num_ops, 32):
            d = src.copy()
            d.pop("item 0");  d.pop("item 1");  d.pop("item 2"); 
            d.pop("item 3");  d.pop("item 4");  d.pop("item 5"); 
            d.pop("item 6");  d.pop("item 7");  d.pop("item 8"); 
            d.pop("item 9");  d.pop("item 10"); d.pop("item 11");
            d.pop("item 12"); d.pop("item 13"); d.pop("item 14");
            d.pop("item 15"); d.pop("item 16"); d.pop("item 17");
            d.pop("item 18"); d.pop("item 19"); d.pop("item 20");
            d.pop("item 21"); d.pop("item 22"); d.pop("item 23");
            d.pop("item 24"); d.pop("item 25"); d.pop("item 26");
            d.pop("item 27"); d.pop("item 28"); d.pop("item 29");
            d.pop("item 30"); d.pop("item 31");            
            
class BenchDict32Del(DictBench):
    'del dict["item"] on a 32-entry dictionary.'
    name = 'del d["key"] on a 32 entry dict'
    categories = ["dict"]
    overheads = ["unrolled32", ("dict32_copy", 1.0 / 32.0)]
    
    def run(self, num_ops):
        src = self.DICT32
        for i in xrange(0, num_ops, 32):
            d = src.copy()
            del d["item 0"];  del d["item 1"];  del d["item 2"]; 
            del d["item 3"];  del d["item 4"];  del d["item 5"]; 
            del d["item 6"];  del d["item 7"];  del d["item 8"]; 
            del d["item 9"];  del d["item 10"]; del d["item 11"];
            del d["item 12"]; del d["item 13"]; del d["item 14"];
            del d["item 15"]; del d["item 16"]; del d["item 17"];
            del d["item 18"]; del d["item 19"]; del d["item 20"];
            del d["item 21"]; del d["item 22"]; del d["item 23"];
            del d["item 24"]; del d["item 25"]; del d["item 26"];
            del d["item 27"]; del d["item 28"]; del d["item 29"];
            del d["item 30"]; del d["item 31"];
            
# Built-in functions.

class HasattrBase(Unrolled32):        
    def run(self, num_ops):
        f = hasattr
        o = self.o
        for i in xrange(0, num_ops, 32):
            f(o, "a"); f(o, "a"); f(o, "a"); f(o, "a");
            f(o, "a"); f(o, "a"); f(o, "a"); f(o, "a");
            f(o, "a"); f(o, "a"); f(o, "a"); f(o, "a");
            f(o, "a"); f(o, "a"); f(o, "a"); f(o, "a");
            f(o, "a"); f(o, "a"); f(o, "a"); f(o, "a");
            f(o, "a"); f(o, "a"); f(o, "a"); f(o, "a");
            f(o, "a"); f(o, "a"); f(o, "a"); f(o, "a");
        
class BenchHasattr(HasattrBase):
    "hasattr() call for an attribute that exists."
    name = "hasattr() when the attribute exists"
    categories = ["builtin", "duck"]

    def prepare(self):
        class C(object):
            a = 123
        self.o = C()
 
class BenchHasattrMissing(HasattrBase):
    "hasattr() call for an attribute that doesn't exist."
    name = "hasattr() when the attribute doesn't exist"
    categories = ["builtin", "duck"]

    def prepare(self):
        class C(object):
            pass
        self.o = C()
        
class BenchType(Unrolled32):
    "A call to type(obj)."
    name = "type(obj)"
    categories = ["builtin", "duck"]
    
    def prepare(self):
        class C(object):
            pass
        self.o = C()
        
    def run(self, num_ops):
        f = type 
        o = self.o
        for t in xrange(0, num_ops, 32):
            f(o); f(o); f(o); f(o); f(o); f(o); f(o); f(o);
            f(o); f(o); f(o); f(o); f(o); f(o); f(o); f(o);
            f(o); f(o); f(o); f(o); f(o); f(o); f(o); f(o);
            f(o); f(o); f(o); f(o); f(o); f(o); f(o); f(o);           

class BenchLen(Unrolled32):
    "len() calls on lists and tuples."
    name = "len()"
    categories = ["builtin"]
    
    def prepare(self):
        self.data1 = [ 1, 2, 3 ]
        self.data2 = (1, 2, 3, 4, 5, 6, 7)
        
    def run(self, num_ops):
        f = len
        a = self.data1
        b = self.data2
        for i in xrange(0, num_ops, 32):
            f(a); f(b); f(a); f(b); f(a); f(b); f(a); f(b);
            f(a); f(b); f(a); f(b); f(a); f(b); f(a); f(b);
            f(a); f(b); f(a); f(b); f(a); f(b); f(a); f(b);
            f(a); f(b); f(a); f(b); f(a); f(b); f(a); f(b);            

class IsInstanceBench(Unrolled32):
    categories = ["builtin", "duck"]
    
    class C(object): 
        pass    
    
    def run(self, num_ops):
        o = self.o
        C = self.C
        f = isinstance
        for i in xrange(0, num_ops, 32):
            f(o, C); f(o, C); f(o, C); f(o, C);
            f(o, C); f(o, C); f(o, C); f(o, C);
            f(o, C); f(o, C); f(o, C); f(o, C);
            f(o, C); f(o, C); f(o, C); f(o, C);
            f(o, C); f(o, C); f(o, C); f(o, C);
            f(o, C); f(o, C); f(o, C); f(o, C);
            f(o, C); f(o, C); f(o, C); f(o, C);
            f(o, C); f(o, C); f(o, C); f(o, C);
            

class BenchIsInstanceTrue(IsInstanceBench):
    "isinstance() calls."
    name = "isinstance() when the result is True"
       
    def prepare(self):
        self.o = self.C()
        
class BenchIsInstanceFalse(IsInstanceBench):
    "isinstance() calls."
    name = "isinstance() when the result is False"
    
    def prepare(self):
        class D(object): 
            pass
        self.o = D()
    
# Exceptions.

class BenchTryExcept(Straight):
    "The overhead of a try...except block when no exception is raised."
    name = '"try...except" block when no exception is raised'
    categories = ["exceptions"]
    
    def run(self, num_ops):
        for i in xrange(num_ops):
            try:
                pass
            except:
                pass
            
class BenchTryRaiseExcept(Straight):
    "A try...except where an exception is raised and caught."
    name = '"try...except" block when an exception is raised and caught'
    categories = ["exceptions"]
    
    def prepare(self):
        self.e = Exception()
        
    def run(self, num_ops):
        e = self.e
        for i in xrange(num_ops):
            try:
                raise e
            except:
                pass
            
class BenchTryRaiseExceptFilter(Straight):
    "A try...except E where an exception is raised and caught."
    name = '"try...except (E)" block when an exception is raised and caught'
    categories = ["exceptions"]
    
    class E(Exception):
        pass
    
    def prepare(self):
        self.e = self.E()
        
    def run(self, num_ops):
        e = self.e
        E = self.E
        for i in xrange(num_ops):
            try:
                raise e
            except E:
                pass

# Duck typing.

class TryExceptAttributeTest(Straight):
    categories = ["duck"]
    
    def run(self, num_ops):
        o = self.o
        for i in xrange(num_ops):
            try:
                o.a
            except AttributeError:
                pass
            
class BenchTryExceptAttrTestAttrExists(TryExceptAttributeTest):
    "An attribute access wrapped in a try...except block which catches " \
    "AttributeError. The attribute exists."
    name = "Attribute access in a try...except when the attribute exists"
    
    def prepare(self):
        class C(object):
            a = 123
        self.o = C()

class BenchTryExceptAttrTestAttrDoesntExist(TryExceptAttributeTest):
    "An attribute access wrapped in a try...except block which catches " \
    "AttributeError. The attribute doesn't exist."
    name = "Attribute access in a try...except when the attribute doesn't exist"
    
    def prepare(self):
        class C(object):
            pass
        self.o = C()
        
overhead_candidate_classes = [
    BenchPass,
    BenchStraight,
    BenchUnrolled32,
    BenchUnrolled100,
    BenchUnrolled1000
]

def benchmark(unit="us", candidates=[], categories=[]):
    MULTIPLIERS = { 
        "s" : 1e0,
        "ms": 1e3, 
        "us": 1e6, 
        "ns": 1e9 
    }
    
    def pretty(n):
        if n >= 0.0:    
            s = "%.0f" % n   
            return ",".join([s[max(i, 0):i + 3] for i in 
                xrange(len(s) % -3, len(s), 3)])
        else:
            return "-" + pretty(-n)

    base = [cls() for cls in overhead_candidate_classes]
    base += [candidate for candidate in candidates if candidate not in base]
    candidates = base

    Candidate.setup()
    
    # Run the benchmarks. The gc module throws exceptions under IronPython.
    for ps in xrange(REPETITIONS):
        for candidate in candidates:
            candidate.prepare()
            try:
                gc.disable()
            except:
                pass
            candidate.time()
            try:
                gc.enable()
            except:
                pass
            candidate.cleanup()
    
    # Take the shortest time achieved for each benchmark and normalize per-op.
    mean = lambda v: sum(v) / len(v)
    for candidate in candidates:
        candidate.time_per_op = min(candidate.times) / candidate.num_ops
        
    # Resolve overheads.
    unresolved = candidates
    overheads = defaultdict(float)
    while unresolved:
        work = unresolved
        unresolved = []
        for candidate in work:
            t = candidate.time_per_op
            for tag, multiplier in candidate.overheads:
                if tag not in overheads:
                    unresolved.append(candidate)
                    break
                t -= overheads[tag] * multiplier
            else:
                candidate.time_per_op = t
                for tag in candidate.tags:
                    overheads[tag] = t
        if len(unresolved) == len(work):
            raise Exception("Mutually dependent overheads")
                            
    # Do unit conversion.
    multiplier = MULTIPLIERS[unit]
    for candidate in candidates:
        candidate.time_per_op *= multiplier
        
    # Make a list of categories to print.
    priority = count()
    catorder = dict((name, priority.next()) for name, desc in categories)
    catitems = defaultdict(set)
    fieldwidth1 = None
    for candidate in candidates:
        if not candidate.name:
            continue
        fieldwidth1 = max(fieldwidth1, len(pretty(candidate.time_per_op)))
        for catname in candidate.categories:
            catitems[catname].add(candidate)
            if catname not in catorder:
                catorder[catname] = priority.next()
    catitems = sorted(catitems.iteritems(), key=lambda item: catorder[item[0]])

    # Print the list.
    catdescs = dict(categories) 
    for name, items in catitems:
        fieldwidth2 = max(len(candidate.name) for candidate in items)
        sorted_items = sorted(items, key=operator.attrgetter("time_per_op"), 
            reverse=True)
        print "-= %s =-\n" % catdescs.get(name, name)
        for candidate in sorted_items:
            print "%*s%s %-*s" % (
                fieldwidth1 + 4, 
                pretty(candidate.time_per_op), 
                unit, fieldwidth2, candidate.name
                )
        print ""

if __name__ == '__main__':
    candidates = [cls() for name, cls in globals().items() if 
        name.startswith("Bench")]
    categories = [
        ("basic", "Basic Operations"),
        ("function", "Function Overhead"),
        ("list", "Tuple and List Creation"),
        ("object_creation", "Object Creation"),
        ("exceptions", "Exception Handling"),
        ("builtin", "Built-in Functions"),
        ("iteration", "Iteration (time per item)"),
        ("dict", "Dictionaries"),
        ("zip", "zip() vs. izip()"),
        ("duck", "Duck Typing Tests")
    ]    
    benchmark(unit="ns", candidates=candidates, categories=categories)
