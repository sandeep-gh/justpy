# Justpy Tutorial demo static_test from docs/tutorial/static.md
import justpy as jp

def static_test():
    wp = jp.WebPage()
    jp.Img(src='/static/static/papillon.jpg', a=wp, classes='m-2 p-2')
    return wp

# initialize the demo
from examples.basedemo import Demo
Demo(static_test)
