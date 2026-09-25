# Programming test: 'O mare, 'o sole, 'o robot

Ciro Musk is a Neapolitan startupper on a mission: automating the servers of every pizzeria in Naples. The first customer is a pizzeria run by maestro Gennaro, an old pizzaiolo who has never touched a computer and has no intention of starting now. Gennaro runs the pizzeria the way he always has: with his Neapolitan heart. "AGI may have arrived in Naples," he says, "but I have never seen a robot eat a pizza."

Ciro Musk's plan is to put a terminal next to the oven, and the terminal needs a program that understands Gennaro. Write that program.

Your program must read Gennaro's commands from standard input, one per line, and must answer each command with exactly one line on standard output. Gennaro is open minded, so you can use the programming language you prefer.

Test cases are in `test-cases/` (inputs, `<id>.in`), their expected outputs in `solutions/` (`<id>.out`). See below how to run and check them.

## Gennaro shouts over the oven

- Names of ingredients and pizzas are single words. Quantities are positive integers.
- An invalid line (unknown command, wrong number of arguments, bad quantity) prints `ERROR invalid command`. The program never crashes.
- Empty lines print nothing.
- A command that prints an error changes nothing. If more errors apply, print the first in this order: invalid command, unknown pizza, not enough ingredient.

## The pantry

- `RESTOCK <ingredient> <qty>` adds units. Prints `OK`.
- `TRASH <ingredient> <qty>` removes units. Prints `OK`, or `ERROR not enough <ingredient>`.
- `STOCK <ingredient>` prints the units available, `0` for an ingredient never seen.

## The pizzeria

- `RECIPE <pizza> <ingredient> ...` defines or replaces a recipe with at least one ingredient. Prints `OK`.
- `ORDER <pizza>` uses one unit of each ingredient in the recipe; an ingredient listed twice is used twice. Prints `OK`, `ERROR unknown pizza`, or `ERROR not enough <ingredient>` for the first short ingredient in recipe order.

## The register

- `SALES` prints `<pizza> <count>` pairs on one line for every pizza sold, by count descending, then by name. Prints `none` if nothing was sold.

## Gennaro plans ahead

- `CAN <pizza>` prints how many of that pizza can be baked with the pantry as it is now, and changes nothing. Prints `ERROR unknown pizza` if the pizza has no recipe.

## Output

- ASCII only. Numbers without sign or leading zeros.
- Blank lines, spaces at the ends of a line and repeated spaces are ignored. Everything else must match exactly.
- Nothing else on standard output: no prompts, no debug messages. Standard error is ignored.

# Running

Your program must read the commands from standard input and must write the answers to standard output. It must not open files itself: you feed it a `.in` file and save what it prints with shell redirection, next to the input.

```
./pizzeria < test-cases/example.in > test-cases/example.out
python3 pizzeria.py < test-cases/example.in > test-cases/example.out
java Pizzeria < test-cases/example.in > test-cases/example.out
```

Each `solutions/<id>.out` is exactly what a correct program prints when run this way on `test-cases/<id>.in`.

## Checking your output

Check the format of your output:

```
python3 lint.py test-cases/example.out
```

It prints `Y`, or `N` and the first problem found. `Y` does not mean your output is correct.

Compare your output with the expected one:

```
python3 check.py test-cases/example.out solutions/example.out
```

It prints `PASS`, or `FAIL` and the first wrong answer: `answer 11` is the answer to the 11th command.

The tools need Python 3.10 or newer; you do not need to read them.

## Writing your own tests

`reference.py` is a correct solution. Use it to generate the expected output for an input you wrote yourself, then check your program against it:

```
python3 reference.py < test-cases/mytest.in > solutions/mytest.out
./pizzeria < test-cases/mytest.in > test-cases/mytest.out
python3 check.py test-cases/mytest.out solutions/mytest.out
```

# How will this be checked?

An LLM will pick your solution, run it on every test case, then lint and check each output. Here `./solution` stands for however your program is run:

```
for t in test-cases/*.in; do
  id=$(basename "$t" .in)
  ./solution < test-cases/$id.in > test-cases/$id.out
  python3 lint.py test-cases/$id.out
  python3 check.py test-cases/$id.out solutions/$id.out
done
```

