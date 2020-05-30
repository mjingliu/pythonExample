from functools import partial
'''
step 1: write one class
step 2: construct __getattr__
step 3: define normal function
step 4: define partial function
step 5: print the passed parameter
step 6: verify what is running of partial
'''

class testPFA:
    def __init__(self, num):
        self.num = num
        print("num = %d" % num)
    def funTest(self, api_name, field = '',**kwargs):

        print("para : %s" % kwargs)
        print("field: %s" % field)
        testArr = {
            'api_name' : api_name,
            'num' : self.num,
            'para': kwargs,
            'field': field
        }
        print(testArr)

    def __getattr__(self, name):
        print("name = %s" % name)
        print("base: %s" % super(partial))
        return partial(self.funTest, name)

if __name__ == '__main__':
    pfa = testPFA(22)
    print("test! %s\n" % pfa.__dict__)
    print("class:%0x\n" % id(testPFA.funTest))
    print(testPFA.__dict__)
    print(pfa.__dict__)
    pfa.daily(88,ts_code="600890", start_date="2019-09-10")
    pfa.weekly(1, st= 'aa')
    
    
