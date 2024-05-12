import multiprocessing as mp
import time
import serialization

from hashlib import sha3_256

class Card:
    def __init__(self, last_num, hash, bin_list):
        self.last_num = last_num
        self.hash = hash
        self.bin_list = bin_list

    def check(self, bin: str, middle_number: str):
        middle_number = int(middle_number.zfill(13))
        card_number = f"{bin}{middle_number}{self.last_num}"
        if sha3_256(card_number.encode()).hexdigest() == self.hash:
            return card_number
        else:
            return None


    def num_bruteforce(self, cores: int):
        start = time.time()
        with mp.Pool(processes=cores) as pool:
            card_num = pool.starmap(
                self.check,
                [
                    (bin, str(mid))
                    for bin in self.bin_list
                    for mid in range(0, 1000000)
                ],
            )
            for res in card_num:
                if res != None:
                    return res, (time.time()-start)
        return None, (time.time()-start)

    def time_test(self):
        res = []
        for cores in range(1, int(mp.cpu_count()*1.5)):
            res.append(self.num_bruteforce(cores)[1])
        x = [i for i in range(1, int(mp.cpu_count()*1.5))]
        return x, res



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
    data = serialization.read_json("lab_4//card.json")
    hash = data["HASH"]
    last_num = data["LAST_NUM"]
    bin_list = data["BIN_LIST"]
    card = Card(last_num, hash, bin_list)