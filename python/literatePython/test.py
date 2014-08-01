import traceback
import traceback
def foo():
        raise Exception("an exception")

def bar():
        print 'in bar'
        try:
                foo()
        except Exception, e:
                stackStr = str(traceback.format_exc())
                lines = stackStr.split('\n')
                for line, index in zip(lines, range(len(lines))):
                        print index, ':', line
                e.args = (e.args[0], 'test')
                raise

try:
        bar()
except Exception, e:
        print 'in main'
        stackStr = str(traceback.format_exc())
        lines = stackStr.split('\n')
        for line, index in zip(lines, range(len(lines))):
                print index, ':', line
        print e
