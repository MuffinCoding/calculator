# This is a simple calculator

This calculator lets you do calculations using the [Shunting Yard algorithm](https://en.wikipedia.org/wiki/Shunting_yard_algorithm) to produce [Reverse Polish Motation](https://en.wikipedia.org/wiki/Reverse_Polish_notation) output used to calculate the output.

The calculator has some fun additions too, such as remembering results like so:

```
calc 2000 > a = 1 + 2
3
calc 2000 > a
3
```

You can also define functions:

```
calc 2000 > a :DEFINE b + c
0
```

And run them:

```
calc 2000 > a :RUN 1 2
3
```

You can save the result of a function like so:

```
calc 2000 > res = a :RUN 1 2
3
calc 2000 > res
3
```

If you want to remove a variable or undefine a function do as follows:

```
calc 2000 > :DEL a
0
```

In order to view the memory type `:MEM`


The calculator is simple and messy as I did not use any tutorial, just the two wikipedia pages that explain the algorithm and my brain :)