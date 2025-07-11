"""
동시성 제어
여러 사용자가 동시에 데이터베이스에 접근하거나 트랜잭션을 실행할 때
데이터의 일관성과 무결성을 보장하기 위한 기술
예
- 한 트랜잭션이 커밋되지 않은 다른 트랜잭션의 데이터를 읽을 수 있음.
- 같은 쿼리를 두번 실행했을 때 그 사이에 다른 트랜잭션이 데이터를 수정 (ACID 중 Isolation 격리성 위반)
- Where 조건에 해당하는 수가 트랜잭션 중간에 변할 수 있음
- 같은 데이터를 읽고 쓸때 한쪽의 수정이 덮어씌워져버림. (마지막 커밋값만 남음)

제어 방법
비관적 락: 무조건 잠금을 건다 (무조건 충돌이 있을 것이다)

낙관적 락: 커밋 시점에 검증 후 실패시 롤백한다 (충돌이 없을 것이다)

분산 락: 여러 서버에서 공유된 자원에 접근하여 수정하는것을 방지하여 데이터를 동기화하기 위해 사용하는 방법
        (ex Redis분산락)


예제에서 사용한 sqlite 의 락

BEGIN Options
BEGIN DEFERRED (기본값) : 트랜잭션의 기본 동작 (읽기/쓰기 동작 전까지 Unlock 상태)
BEGIN IMMEDIATE : 트랜잭션 시작과 동시에 Reserved lock 획득 (다른 프로세스는 Immediate, exclusive lock 획득 불가능)
BEGIN EXCLUSIVE : 트랜잭션 시작과 동시에 Exclusive lock 획득 (다른 프로세스는 읽기/쓰기 불가능)
"""


import sqlite3
import time
import multiprocessing

## initial setup
def setup_pessimistic():
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS pessimistic")
    cur.execute("""
                CREATE TABLE pessimistic (id integer primary key,
                                        value integer)
                """)
    cur.execute("insert into pessimistic (id, value) values (1, 10)")
    conn.commit()
    conn.close()



## 비관적 락
def change_value_pessimistic(name, delay=0):
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    try:
        print(f"{name}: begin transaction..")
        cur.execute("BEGIN IMMEDIATE") # 락 획득
        time.sleep(delay)
        
        cur.execute("select value from pessimistic where id = 1")
        val = cur.fetchone()[0]
        
        print(f"{name}: current value {val}")
        if val > 0:
            print(f"{name}: decreasing value")
            cur.execute("Update pessimistic Set value = value - 1 where id = 1")
        else:
            print(f"{name}: value is 0")
        conn.commit()
        
        cur.execute("select value from pessimistic where id = 1")
        val = cur.fetchone()[0]
        print(f"{name}: current value {val}")

        
    except Exception as e:
        print(f"{name}: error {e}")
    finally:
        conn.close()
        
## 결과
# t1: begin transaction..
# t2: begin transaction..
# t1: current value 10
# t1: decreasing value
# t1: current value 9
# t2: current value 9
# t2: decreasing value
# t2: current value 8

# t1 이 먼저 db의 락을 획득. t2 는 대기
        


def setup_optimistic():
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS optimistic")
    conn.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging 모드

    cur.execute("""
                CREATE TABLE optimistic (id integer primary key,
                                        value integer, version integer)
                """)
    cur.execute("insert into optimistic (id, value, version) values (1, 10, 1)")
    conn.commit()
    conn.close()




def change_value_optimistic(name, delay):
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    try:
        print(f"{name}: begin transaction..")
        cur.execute("BEGIN")
        cur.execute("SELECT value, version FROM optimistic WHERE id = 1")
        val, version = cur.fetchone()
        print(f"{name}: initial {val} with version {version}")
        time.sleep(delay)  # 일부러 지연

        if val > 0:
            print(f"{name}: Trying update with version {version}")
            updated = cur.execute(
                "UPDATE optimistic SET value = value - 1, version = version + 1 WHERE id = 1 AND version = ?",
                (version,)
            ).rowcount
            print(f"{name}: update executed")
            if updated == 0:
                raise Exception("Optimistic lock failed — version mismatch")

            conn.commit()
            print(f"{name}: Success")
        else:
            print(f"{name}: No value")
    except Exception as e:
        print(f"{name}: error {e}")
    finally:
        conn.close()
        
        
### 결과
# 낙관적 락
# t1: begin transaction..
# t1: initial 10 with version 1
# t2: begin transaction..
# t2: initial 10 with version 1
# t2: Trying update with version 1
# t2: update executed
# t2: Success
# t1: Trying update with version 1
# t1: error database is locked

# t1 과 t2 가 같은 값에 접근
# t1 에게는 딜레이를 주고 t2는 바로 업데이트
# t2가 업데이트 된 이후 버전이 업데이트 됨 (2)
# t1 은 기존 버전(1) 에 업데이트를 하려고 해서 실패


if __name__ == "__main__":
    print("비관적 락")
    setup_pessimistic()
    t1 = multiprocessing.Process(target=change_value_pessimistic, args=("t1", 2))
    t2 = multiprocessing.Process(target=change_value_pessimistic, args=("t2", 0))
        
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()

    print("낙관적 락")
    setup_optimistic()
    t2 = multiprocessing.Process(target=change_value_optimistic, args=("t2", 0))
    t1 = multiprocessing.Process(target=change_value_optimistic, args=("t1", 5))
        
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()

