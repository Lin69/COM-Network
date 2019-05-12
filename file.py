# encoding

class Data:
    
    def ReadFile(self,file_name):
        
        text = []
        data = ""
        with open(file_name,'r+') as f:
            for line in f:
                text.append(line)
        data = "".join(text)
        return data

    def Coding_to_bin(self,data):
        
        return ''.join([bin(ord(c))[2:].zfill(8) for c in data])
                
    def code_to_ham(self,data):

        result=[]
        for i in range(len(data)//4):
            word = self.three_to_eight(data[i*4:i*4+4])
            result.append(word)

        return result

    def three_to_eight(self,code):

        hamcode=[0,0,0,0,0,0,0,0]
        hamcode[3],hamcode[5],hamcode[6],hamcode[7]=int(code[0]), int(code[1]), int(code[2]), int(code[3])
        hamcode[1] = (hamcode[3] + hamcode[5] + hamcode[7])%2
        hamcode[2] = (hamcode[3] + hamcode[6] + hamcode[7])%2
        hamcode[4] = (hamcode[5] + hamcode[6] + hamcode[7])%2
        strcode = [str(i) for i in hamcode]
        return ''.join(strcode)

    def Code_to_str(self,code):

        return ''.join([chr(int(x, 2)) for x in code])

    def decoding_ham(self,data):

        lst = []
        for i in range(len(data)//8):
            word = data[i*8:i*8+8]
            self.mistakes(word)
            newword = ''.join([word[3],word[5],word[6],word[7]])
            lst.append(newword)
        return self.getting_bytes(lst)


    def mistakes(self,word):
        
        syn001 = str((int(word[1])+int(word[3])+int(word[5])+int(word[7]))%2)
        syn010 = str((int(word[2])+int(word[3])+int(word[6])+int(word[7]))%2)
        syn100 = str((int(word[4])+int(word[5])+int(word[6])+int(word[7]))%2)
        
        syndrom = int(''.join([syn100,syn010,syn001]))
        if syndrom !=0:
            raise AssertionError("Ошибка при передаче данных")

    def getting_bytes(self,lst):
        
        newlst = []
        for i in range(len(lst)//2):
            word = ''.join([lst[i*2],lst[i*2+1]])
            newlst.append(word)
        return newlst





