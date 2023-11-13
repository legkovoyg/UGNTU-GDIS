import pandas as pd

# test1= [[1,2,3,4,5,6]]
# test1= [[val[0][0] for val in row] for row in test1]
#
# test2 = [[1,5,3,2,4,5]]
#
# fff = pd.DataFrame({'Тест1':test1,'Тест2':test2})
# fff.to_excel('./test.xlsx',sheet_name="Тест",index=False,)
#


test = [[1,2,3,4],[1,3,5,6],[1,2,7,7]]
test2=[]
A = [ [1, 2, 3], [4, 5, 6] ]
for i in range(len(test)):
    for j in range(len(test[i])):
        test2.append(test[i][j])

print(test2)