import pexpect

# Fun fact: `pexpect.run` can't take a generator.
# String, method, or function only.
def guess(arg):
    num = 0
    while num < 10:
        yield f"{num}\n"
        num += 1


num2 = -1
def guess2(arg):
    global num2
    print(f"\n>>>called guess2 with arg '{arg}'\n\n")
    num2 += 1
    return f"{num2}\n"

# "But what if I *like* generators?"
def guess3_wrap():
    inner = guess(None)
    def wrapped(arg):
        return inner.send(None)
    return wrapped

class guess4:
    def __init__(self):
        self.num = -1

    def get(self, arg):
        self.num = self.num + 1
        return f"{self.num}\n"


def main():
    with open('out.log', 'wb') as log:
        (output, status) = pexpect.run('./the-script', logfile=log,
            withexitstatus=True,
            events={'First Name: ': 'Tim\n',
                    'Last Name: ': 'Brownawell\n',
                    # guess guess2 guess3_wrap() guess4().get
                    r'(guess|try again).*: ': guess3_wrap()}
            )
        print(f"Output: <<<{output}>>>")
        print(f"Exit status: {status}")


def main2():
    with open('out.log', 'wb') as log:
        child = pexpect.spawn('./the-script', logfile=log)
        child.expect('First Name: ')
        child.sendline('Tim')
        child.expect('Last Name: ')
        child.sendline('Brownawell')
        num = 0
        try:
            while True:
                child.expect(['guess.*: ', 'try again.*: '])
                child.sendline(f"{num}")
                num += 1
        except pexpect.exceptions.EOF:
            pass
        child.close()
        print("See `out.log` for output.")
        print(f"Exit status: {child.exitstatus}")


if __name__ == '__main__':
    main2()
