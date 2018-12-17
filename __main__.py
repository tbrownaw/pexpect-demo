import pexpect

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

def guess3_wrap():
    def gen():
        num = 0
        while num < 10:
            yield f"{num}\n"
            num += 1
    inner = gen()
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
                    r'(guess|try again).*: ': guess2}
            )
        print(f"Output: <<<{output}>>>")
        print(f"Exit status: {status}")


if __name__ == '__main__':
    main()
