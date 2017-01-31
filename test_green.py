from greenlet import greenlet, GreenletExit

def test1():
    print(12)
    doit()
    print(34)

def test2():
    try:
        print(56)
        gr1.switch()
        print(78)
    except GreenletExit as x:
        print("EXIT")
        pass

def doit():
    gr2.switch()

gr1 = greenlet(test1)
gr2 = greenlet(test2)
print(gr1.switch())
gr2=None
#gr2.switch
