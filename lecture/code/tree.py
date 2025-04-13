import turtle

def tree(branchLen, t, level):
    if branchLen > 10: #base case
        t.width(max(1,15-level*3))
        t.forward(branchLen)
        t.right(20)
        tree(branchLen-15, t, level + 1)  # recurse next branch 15 shorter
        t.left(40)
        tree(branchLen-15, t, level + 1)  # recurse next branch 15 shorter
        t.right(20) # return to start direction
        t.backward(branchLen)  # back down branch same to start pos
    else:
        return

def main():
    t = turtle.Turtle()
    myWin = turtle.Screen()

    myWin.setup(width=600, height=600)  # line to make smaller window
    t.speed(1)  # max speed on drawing

    t.left(90)  # these line position turtle in window
    t.up()      # and point turtle 'up'
    t.backward(100)
    t.down()    # now at base of tree, lower pen
    t.color("green")  # set color of tree start
    t.width(15)
    tree(105, t, 1)  # draw tree starting at 105 length branches
    myWin.exitonclick()

main()
