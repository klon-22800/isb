import multiprocessing as mp
import time

from matplotlib import pyplot as plt 
from hashlib import sha3_256



def check(last_num: str, hash: str, bin: str, middle_number: str):
    middle_number = int(middle_number.zfill(6))
    card_number = f"{bin}{middle_number}{last_num}"
    if sha3_256(card_number.encode()).hexdigest() == hash:
        return card_number
    else:
        return None


def num_bruteforce(last_num: str, hash: str, bin_list: list, cores: int):
    start = time.time()
    with mp.Pool(processes=cores) as pool:
        card_num = pool.starmap(
            check,
            [
                (last_num, hash, bin, str(mid))
                for bin in bin_list
                for mid in range(0, 1000000)
            ],
        )
        for res in card_num:
            if res != None:
                return res, (time.time()-start)
    return None, (time.time()-start)

def time_test()->float:
    res = []
    bin_list = [426890, 427326]
    for cores in range(1, int(mp.cpu_count()*1.5)):
        res.append(num_bruteforce("0956", "0b08d71bd3e26721ff32542069442d82811bff4a1e61134dfeedc14848cd0e39", bin_list,cores,)[1])
    x = [i for i in range(1, int(mp.cpu_count()*1.5))]
    plt.plot(x,res, marker = 'o')
    plt.show()



def luna(card_num: str)->bool:
    last = int(card_num[-1])
    card_num_list = [int(i) for i in card_num]
    for i in range(0, len(card_num_list)-1, 2):
        card_num_list[i] *= 2
        if card_num_list[i] > 9:
            card_num_list[i] = sum(map(int, str(card_num_list[i])))
    res_sum = sum(card_num_list[-2::-1])
    res = (10 - (res_sum % 10)) % 10
    return last == res


if __name__ == "__main__":
    print(time_test())
   