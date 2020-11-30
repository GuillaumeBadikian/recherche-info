import pandas as pd
class Compare():
    def compare(self, file, file2):
        f = open(file)
        buff = f.readlines()
        f.close()
        f2 = open(file2)
        buff2 = f2.readlines()
        f2.close()
        res = []
        for line in buff:

            for l2 in buff2:
                if line.split(" ")[2] == l2.split(" ")[2]:
                    print(line.split(" ")[2],line.split(" ")[3],l2.split(" ")[2],l2.split(" ")[3],int(line.split(" ")[3])-int(l2.split(" ")[3])  )
                    res.append([line.split(" ")[2],line.split(" ")[3],l2.split(" ")[2],l2.split(" ")[3],int(line.split(" ")[3])-int(l2.split(" ")[3])])
                    break


        #pd.DataFrame(res, columns=['doc1','pos','doc2','pos','diff'])
        #print(pd[:20])