
def ispassword(password, part1=True):
    hasDouble = False
    hasDuplicate = False
    for i in range(5):
        if int(password[i]) > int(password[i + 1]):
            # If it decreases its invalid.
            return False
        if password[i] == password[i + 1]:
            hasDuplicate = True
            # check the before and after numbers to make sure this is just a double.
            if i == 0 or password[i - 1] != password[i]:
                if i == 4 or password[i + 2] != password[i]:
                    hasDouble = True

    # If it doesn't have a double its invalid.
    if part1:
        return hasDuplicate
    return hasDouble


start = 206938
end = 679128

count1 = 0
count2 = 0
for i in range(start, end):
    s = str(i)
    if ispassword(s):
        count1 += 1
    if ispassword(s, part1=False):
        count2 += 1

    print(i)

print("Part 1:", count1)
print("Part 2:", count2)
