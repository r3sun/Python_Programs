nums = [1, 3, 5, 7, 9, 11, 13, 15]

for i in nums:
    for j in nums:
        for k in nums:
            s = i + j + k
            if s == 30:
                print("{} + {} + {} = {}".format(i, j, k, s))
