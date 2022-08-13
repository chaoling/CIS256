def caesarShift(txt: str, shift: int) -> str:
    pass


if __name__ == "__main__":
    txt = input()
    shift = int(input())
    print(caesarShift(txt, shift))

    #assert caesarShift('example', 1) == 'fybnqmf', 'failed test case 1'
    #assert caesarShift('example', -1) == 'dwzlokd', 'failed test case 2'
    #assert caesarShift('python', 2) == 'ravjqp', "failed test case 3"
    #assert caesarShift('pecan', 4) == 'tiger', "failed test case 4"
