from database_management import find_all_bots
bots = find_all_bots()
string = ''
for bot in bots:
    string += bot + ','
# print(a + ',' + b)
print(string)