import simu

global CACHE_MISS
CACHE_MISS = 0

cache1_size = 8
cache2_size = 16
block1_size = 4
block2_size = 4
# latency1 = 10
# latency2 = 20

assoc1 = 1
assoc2 = 2

# to be changed later...
stalls1 = 2
stalls2 = 4
stalls3 = 10  # for memory penalty

set1 = int(cache1_size / (block1_size * assoc1))
set2 = int(cache2_size / (block2_size * assoc2))


# no_of_blocks_in_cache1 = cache1_size/block1_size
# no_of_sets = no_of_blocks_in_cache1/assoc1

def update_settings(cache1, cache2, block1, block2, assco1, assco2, stall1, stall2, stall3):
    global cache1_size, cache2_size, block1_size, block2_size, assoc1, assoc2, stalls1, stalls2, stalls3, set1, set2
    print("Updating", cache1, cache2, block1, block2, assco1, assco2, stall1, stall2, stall3)
    cache1_size = int(cache1 or cache1_size)
    cache2_size = int(cache2 or cache2_size)
    block1_size = int(block1 or block1_size)
    block2_size = int(block2 or block2_size)
    assoc1 = int(assco1 or assoc1)
    assoc2 = int(assco2 or assoc2)
    stalls1 = int(stall1 or stalls1)
    stalls2 = int(stall2 or stalls2)
    stalls3 = int(stall3 or stalls3)
    set1 = int(cache1_size / (block1_size * assoc1))
    set2 = int(cache2_size / (block2_size * assoc2))

    print("Updated", cache1_size, cache2_size, block1_size, block2_size, assoc1, assoc2, stalls1, stalls2, stalls3)
    CacheHit.change_caches()


global counter1
global counter2
counter1 = 0
counter2 = 0


class CacheHit:
    global cache1
    global cache2

    cache1 = []
    cache2 = []

    for _ in range(set1):
        cache1.append([[-1, -1, counter1]] * assoc1)
        # indices -> tag, data, counter(for LRU)

    for _ in range(set2):
        cache2.append([[-1, -1, counter2]] * assoc2)
        # indices -> tag, data, counter(for LRU)
    print("=" * 100)
    print(cache1)
    print(cache2)
    print("=" * 100)

    def change_caches():
        global cache1
        global cache2

        cache1 = []
        cache2 = []

        for _ in range(set1):
            cache1.append([[-1, -1, counter1]] * assoc1)
            # indices -> tag, data, counter(for LRU)

        for _ in range(set2):
            cache2.append([[-1, -1, counter2]] * assoc2)
            # indices -> tag, data, counter(for LRU)
        print("=" * 100)
        print(cache1)
        print(cache2)
        print("=" * 100)

    # Cache 1. Checking if the data is present or not
    def cache_hit_1(self, adrs):
        global cachehit1
        cachehit1 = False

        set_id = adrs % set1
        for j in range(assoc1):
            if adrs == cache1[set_id][j][0]:
                cachehit1 = True
                global counter1
                cache1[set_id][j] = [adrs, simu.RAM[adrs], counter1]
                counter1 += 1
                return cache1[set_id][j][1], stalls1

        if not cachehit1:
            temp1 = self.cache_hit_2(adrs)
            self.insert_cache1(adrs)
            return temp1

    # Cache 2. Checking if the data is present or not if it is not present in Cache 1
    def cache_hit_2(self, adrs):
        global cachehit2
        cachehit2 = False

        set_id = adrs % set2
        for j in range(assoc2):
            if adrs == cache2[set_id][j][0]:
                cachehit2 = True
                global counter2
                cache2[set_id][j] = [adrs, simu.RAM[adrs], counter2]
                counter2 += 1
                print(2222, cache2)
                return cache2[set_id][j][1], stalls1 + stalls2

        if not cachehit2:
            temp2 = self.memory_operation(adrs)
            self.insert_cache2(adrs)
            return temp2

    # Checking in memory if the data is not present in both the Caches
    def memory_operation(self, adrs):
        print("Cache Miss!")
        global CACHE_MISS
        CACHE_MISS += 1
        return simu.RAM[adrs], stalls1 + stalls2 + stalls3

    # Inserting Data in Cache1 if not present
    def insert_cache1(self, adrs):
        cache1inserted = False
        set_id = adrs % set1
        for j in range(assoc1):
            if cache1[set_id][j][0] == -1:
                global counter1
                cache1[set_id][j] = [adrs, simu.RAM[adrs], counter1]
                counter1 += 1
                cache1inserted = True
                break

        if not cache1inserted:
            self.replace_in_cache1(adrs)

    # Inserting Data in Cache2 if not present
    def insert_cache2(self, adrs):
        cache2inserted = False
        set_id = adrs % set2
        for j in range(assoc2):
            if cache2[set_id][j][0] == -1:
                global counter2
                cache2[set_id][j] = [adrs, simu.RAM[adrs], counter2]
                counter2 += 1
                cache2inserted = True
                break
        if not cache2inserted:
            self.replace_in_cache2(adrs)

    # If Cache1 is full, then replacing the existing data with new one acc to LRU policy
    def replace_in_cache1(self, adrs):
        ilru = 0
        jlru = 0
        set_id = adrs % set1
        for j in range(assoc1):
            if cache1[set_id][j][2] < cache1[ilru][jlru][2]:
                ilru = set_id
                jlru = j
        global counter1
        cache1[ilru][jlru] = [adrs, simu.RAM[adrs], counter1]
        counter1+=1

    # If Cache2 is full, then replacing the existing data with new one acc to LRU policy
    def replace_in_cache2(self, adrs):
        ilru = 0
        jlru = 0
        set_id = adrs % set2
        for j in range(assoc2):
            if cache2[set_id][j][2] < cache2[ilru][jlru][2]:
                ilru = set_id
                jlru = j
        global counter2
        cache2[ilru][jlru] = [adrs, simu.RAM[adrs], counter2]
        counter2+=1


CacheOP = CacheHit()
