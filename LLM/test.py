import turtle


screen = turtle.Screen()
screen.title("Robot Face")
screen.bgcolor("black")
screen.setup(width=600, height=600)

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)
pen.pensize(3)


def draw_circle(x, y, radius, color):
    pen.penup()
    pen.goto(x, y - radius)
    pen.pendown()
    pen.fillcolor(color)
    pen.begin_fill()
    pen.circle(radius)
    pen.end_fill()


def draw_head():
    pen.penup()
    pen.goto(-150, 150)
    pen.pendown()
    pen.color("white")
    pen.pensize(10)
    pen.begin_fill()
    pen.fillcolor("#202020")
    pen.setheading(0)
    for _ in range(2):
        pen.forward(300)
        pen.circle(-50, 90)
        pen.forward(300)
        pen.circle(-50, 90)
    pen.end_fill()


draw_head()


draw_circle(-70, 80, 50, "white")      # tròng trắng
draw_circle(-70, 80, 30, "#00aaff")    # mống mắt
draw_circle(-70, 90, 10, "white")      # highlight


draw_circle(70, 80, 50, "white")
draw_circle(70, 80, 30, "#00aaff")
draw_circle(70, 90, 10, "white")


pen.penup()
pen.goto(-50, -20)
pen.pendown()
pen.color("white")
pen.pensize(5)
pen.setheading(-60)
pen.circle(60, 120)  

turtle.done()