import gmpy2
from gmpy2 import fib
from gmpy2 import mpz

def my(a,b):
    #0为偶，1为奇
    aa=a%2
    bb=b%2
    c=aa+bb
    if (a==1 and b==2) or (a==3 and b==2) or (a==5 and b==2) or (a==7 and b==2):
        return 0
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

def her(a,b):
    return fib(a) % fib(b)

def check_pair(args): # (a,b,if_false)
    a, b = args
    a_gmp=mpz(a)
    b_gmp=mpz(b)
    a1 = my(a_gmp, b_gmp)
    a2 = her(a_gmp, b_gmp)
    if a1 != a2:
        return (a, b,1)
    else:
        return (a,b,0)