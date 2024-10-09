import csv

def Finder():
    chosen =0
    with open("/home/egb320/Documents/EGB320-REPO-MAIN/EGB320-Robo-Go-Brr/navigation/Order_1.csv", mode="r", encoding='utf-8-sig') as csv_file:
        csv.reader = csv.reader(csv_file)
        for row in csv.reader:
            if row[3]=='0':
                print('Here!')
                if row[4]!="Weetbots":
                    print('HERE')
                    chosen=row
    return(chosen)
l=Finder()
print(l)