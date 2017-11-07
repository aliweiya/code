# identify charset
import chardet

s = ''

encoding = chardet.detect(s)

# callback
def a():
    print 555

def test(callback):
    callback()

if __name__  == '__main__':
    test(a)

