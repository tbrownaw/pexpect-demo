import pexpect

def guess(arg):
    num = 0
    while num < 10:
        yield f"{num}\n"
        num += 1


num2 = -1
def guess2(arg):
    global num2
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

def main():
    with open('out.log', 'wb') as log:
        (output, status) = pexpect.run('./the-script', logfile=log,
            withexitstatus=True,
            events={'First Name: ': 'Tim\n',
                    'Last Name: ': 'Brownawell\n',
                    r'(guess|try again).*: ': guess3_wrap()}
            )
        print(f"Output: <<<{output}>>>")
        print(f"Exit status: {status}")


if __name__ == '__main__':
    main()
