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

# char to encoding
u'%s' % ('ue5d0')

'\ued50'.decode('unicode-escape')

'\xe5'.decode('utf-8')


