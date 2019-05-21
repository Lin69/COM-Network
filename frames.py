class Data:
    
    def __init__(self,data):
        self.data = data

    def code_data(self):
        
        self.bindata = self.Coding_to_bin()
        
        return self.Code_to_str(self.code_to_ham())

    def decode_data(self):

        self.bindata = self.Coding_to_bin()

        return self.Code_to_str(self.decoding_ham())


    # def ReadFile(self,file_name):
        
    #     text = []
    #     data = ""
    #     with open(file_name,'r+') as f:
    #         for line in f:
    #             text.append(line)
    #     data = "".join(text)
    #     return data

    def Coding_to_bin(self):
        
        return ''.join([bin(ord(c))[2:].zfill(8) for c in self.data])
                
    def code_to_ham(self):

        result=[]
        for i in range(len(self.bindata)//4):
            word = self.three_to_eight(self.bindata[i*4:i*4+4])
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

    def decoding_ham(self):

        lst = []
        for i in range(len(self.bindata)//8):
            word = self.bindata[i*8:i*8+8]
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

class Frames:

    def create_frame(self,f_type,info=None):

        if f_type == 'A' or f_type == 'L' or f_type == 'U' or f_type == 'N': # по факту все эти кадры состоят только из управляющего блока так что на этой стадии они готовы
            return f_type
        elif f_type == 'H' or f_type == 'I': 
            return self.main_frame(f_type,info)

    def main_frame(self,typ,info):

        frame =[typ]

        l = self.num_to_str(2*len(info))
        frame.append(l)
        h = Data(info)
        l = str(h.code_data())
        frame.append(l)
        return ''.join(frame)
        
    def num_to_str(self,n):
        a = []
        for i in range(8): 
            a.append('0')
        i =0
        while True:
            
            a[7-i]=str(n%2)

            n= n//2
            if n == 0:
                break
            i+=1
            
        st = ''.join(a)
        return chr(int(st, 2))

    def str_to_num(self,st):
        
        binnum = str(bin(ord(st))[2:].zfill(8))
        
        num = 0
        for i in range(8):
            num+=int(binnum[7-i])*(2**i)
        return num


    def deconstract_frame(self,frame):
        
        if frame[0] != 'H' and frame[0] != 'I':
            return (frame[0],)
        else:
            return self.de_main_frame(frame)



    def de_main_frame(self,frame):
        
        typ = frame[0]
        
        size = self.str_to_num(frame[1])

        if size != len(frame[2:]):
            return('Mistake',)
        info = Data(frame[2:])
        try:
            info_part = info.decode_data()
        except AssertionError:
            return('Mistake',)
        
        return typ,info_part

    def tosingle_string(self,lst):
        return ''.join(lst)