from multiprocessing import Pool, cpu_count
import multiprocessing
from tqdm import tqdm
import sys
import os
import fcntl, json
from collections import deque
import datetime
#import gmpy2

from lib import check_pair

def update(a, b,error_list):
    CACHE_PATH="./run_cache.jsonl"
    formatted_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CACHE_PATH, 'a', encoding='utf-8') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX) #lock file
        record={"time":formatted_time,"A":a,"B":b, "error_cnt":len(error_list), "error_list":list(error_list)}
        f.write(json.dumps(record, ensure_ascii=False) + '\n')
        print("logged",record)
        f.flush() # unlock file

def resume():
    CACHE_PATH="./run_cache.jsonl"
    assert os.path.exists(CACHE_PATH), "CACHE_PATH not found"
    with open(CACHE_PATH, 'r', encoding='utf-8') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_SH) #lock file
        states = deque(f, maxlen=10)   
    for state in reversed(states):
        state=state.strip()
        try:
            return json.loads(state)
        except json.JSONDecodeError:
            continue
    return None

if __name__== "__main__":

    log_step=int(1e7+123)
    processes=1+cpu_count()*0.20
    #processes=5
    mininterval=2
    chunksize=5000

    print(f"log_step: ", "%.2e"%log_step)

    s = sys.argv[1] if len(sys.argv) > 1 else input("test scale:")
    scale = int(float(s.split('e')[0]) * (10 ** int(s.split('e')[1]))) if 'e' in s else int(s)

    print(f"scale inputed: ", "%.2e"%scale)
    total = scale*scale
    A,B=1,1
    A_backup,B_backup=1,1
    error_list=[]
    from_cache=resume()
    if from_cache:
        for x in from_cache["error_list"]:
            error_list.append(x)
        A,B=from_cache["A"],from_cache["B"]
        A_backup,B_backup=A,B
        if B < scale:
            B += 1
        else:
            A += 1
            B = 1
        if A > scale:
            print("ready done!")
            exit(1)
        print("resumed from cache:",(A,B),error_list)
    tasks = ((a, b) for a in range(A, scale + 1) for b in range(B if a==A else 1, scale + 1))

    pool = Pool(processes=int(processes))
    print(f"Using {int(processes)} processes")

    #bar_format='{desc}: {percentage:3.0f}%| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]'
    
    with tqdm(total=total-(A_backup-1)*scale-B_backup,mininterval=mininterval) as pbar:
        log_cnt=0
        for res in pool.imap(check_pair, tasks, chunksize=chunksize):
            a,b,is_false=res
            if is_false:
                error_list.append((a,b))
                print(res)

            log_cnt+=1
            if log_cnt==log_step:
                log_cnt=0
                update(a,b,error_list)

            pbar.update(1)
    pool.close()
    pool.join()


    print("run end")
    error_count = len(error_list)
    for a, b in error_list:
        print(a, b)
    update(scale,scale,error_list) 

    print(f"total: {total}, error(s): {error_count}")