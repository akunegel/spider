def getUrl(args) -> str:
    if (len(args) == 1):
        print("Error : Usage python3 spider.py [-rlp] [args] URL.")
        exit(1)

    url = args[-1]

    args.pop(len(args) - 1)
    args.pop(0)

    return (url)


def getFlags(args) -> list:
    flags = []

    for arg in args:
        if (arg[0] == '-'):
            for i in range(1, len(arg)):
                if (arg[i] == 'l' or arg[i] == 'r' or arg[i] == 'p'):
                    if (arg[i] not in flags):
                        flags.append(arg[i])
                else:
                    print("Error : flag not recognized. Options are r, l and p.")
                    exit(1)

    cleanArgs = [arg for arg in args if not arg.startswith('-')]

    return flags, cleanArgs


def checkFlags(args, flags):
    recursive = False
    path = "./data/"
    r = int(5)

    for flag in flags:
        if (flag == 'l'):
            if ('r' not in flags):
                print ("Error : l flag will have no effect without r flag.")
                exit(1)
            if (len(args) > 0):
                r = args[0]
                if (r.isnumeric() == False):
                    print("Error : expecting a number for l flag.")
                    exit(1)
                args.pop(0)
            else:
                print("Error : expecting a number for l flag.")
                exit(1)

        if (flag == 'r'):
            recursive = True

        if (flag == 'p'):
            if (len(args) > 0):
                path = args[0]
                args.pop(0)
            else:
                print("Error : path not found for p flag.")
                exit(1)
    if (len(args) != 0):
        print("Error : too much arguments.")
        exit(1)
    return (recursive, path, r)


def parseArgs(args):
    flags = []

    url = getUrl(args)
    if (len(args) > 0):
        flags, args = getFlags(args)
    
    recursive, path, r = checkFlags(args, flags)

    return (flags, url, r, path, recursive)