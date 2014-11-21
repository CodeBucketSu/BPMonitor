import sys
if sys.version_info[:2] < (2, 5):
    def partial(func, arg):
        def callme():
            return func(arg)
        return callme
else:
    from functools import partial

def action(text):
    print text

funclist = []
for i in range(3):
    funclist.append(partial(action, i))

for func in funclist:
    func()