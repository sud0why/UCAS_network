file1 = open("data.txt", "r")
accounts = []
for line in file1.readlines():
    if line[19:23] != "2019":
        accounts.append(line)

accounts = list(set(accounts))
print(accounts)

file2 = open("account.txt", "w")
for account in accounts:
    file2.write(account)

file1.close()
file2.close()
