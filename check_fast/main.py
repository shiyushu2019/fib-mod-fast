from time import time
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

while True:
    
    low,high,repeat=map(int,input().split())
    #设定数据组上下界
    #每个计算重复repeat次减少偶然误差

    #my计算
    start=time()
    for a in range(low,high+1):
        a_mpz=mpz(a)
        for b in range(low,high+1):
            b_mpz=mpz(b)
            for _ in range(repeat):
                buf1=my(a_mpz,b_mpz)
    end=time()
    #my计算耗时总计
    my_t=(end-start)/(high-low)**2/repeat
    my_t*=1000000
    print(f"{my_t:.4f}")

    #her_violet计算
    start=time()
    for a in range(low,high+1):
        a_mpz=mpz(a)
        for b in range(low,high+1):
            b_mpz=mpz(b)
            for _ in range(repeat):
                buf2=her(a_mpz,b_mpz)
    end=time()
    #公式计算耗时总计
    tradition_t=(end-start)/(high-low)**2/repeat
    tradition_t*=1000000
    print(f"{tradition_t:.4f}")




    