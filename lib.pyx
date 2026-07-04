import gmpy2
from gmpy2 import fib
import cython
from gmpy2 cimport *
import_gmpy2()

@cython.profile(False)
cdef mpz my(mpz a,mpz b):
    #0为偶，1为奇
    cdef mpz aa=a%2
    cdef mpz bb=b%2
    cdef mpz c=aa+bb
    if (a==1 and b==2) or (a==3 and b==2) or (a==5 and b==2) or (a==7 and b==2):
        return mpz(0)
    if a<b:
        return fib(a)
    if  c!=1 and b<=a<2*b:
    #c=0,2
        return fib(b)-fib(2*b-a)
    if c!=0 and a>=4*b:
    #c=1,2
        return my(a%(4*b),b)
    if c==0 and a>=2*b:
        return my(a%(2*b),b)
    if c==1 and b<=a<=2*b:
        return fib(2*b-a )
    if c==2:
        if 3*b<a<4*b:
            return fib(4*b-a )
        if 2*b<=a<=3*b:
            return fib(b )-fib(a-2*b )
    if aa==1 and bb==0 and 2*b<a<4*b:
        return fib(b-abs(a-3*b) )
    if aa==0 and bb==1 and 2*b<a<4*b:
        return fib(b )-fib(b-abs(a-3*b) )
    print((a,b),"my() end error!")
    exit(1)

@cython.profile(False)
cdef mpz her(mpz a,mpz b):
    return fib(a) % fib(b)

@cython.profile(False)
def check_pair(args): # (a,b,if_false)
    a, b = args
    cdef mpz a_gmp=mpz(a)
    cdef mpz b_gmp=mpz(b)
    cdef mpz a1 = my(a_gmp, b_gmp)
    cdef mpz a2 = her(a_gmp, b_gmp)
    if a1 != a2:
        return (a, b,1)
    else:
        return (a,b,0)