import sys
from collections import Counter
from typing import NamedTuple


class State(NamedTuple):
    pantry: dict[str, int]
    recipes: dict[str, list[str]]
    sales: dict[str, int]


def positive(word: str) -> bool:
    return word.isascii() and word.isdigit() and int(word) > 0


def restock(s: State, item: str, qty: int) -> tuple[str, State]:
    return "OK", s._replace(pantry={**s.pantry, item: s.pantry.get(item, 0) + qty})


def trash(s: State, item: str, qty: int) -> tuple[str, State]:
    if s.pantry.get(item, 0) < qty:
        return f"ERROR not enough {item}", s
    return restock(s, item, -qty)


def order(s: State, pizza: str) -> tuple[str, State]:
    if pizza not in s.recipes:
        return "ERROR unknown pizza", s
    need = Counter(s.recipes[pizza])
    short = [item for item, n in need.items() if s.pantry.get(item, 0) < n]
    if short:
        return f"ERROR not enough {short[0]}", s
    used = {item: s.pantry[item] - n for item, n in need.items()}
    sales = {**s.sales, pizza: s.sales.get(pizza, 0) + 1}
    return "OK", s._replace(pantry={**s.pantry, **used}, sales=sales)


def report(sales: dict[str, int]) -> str:
    ranked = sorted(sales.items(), key=lambda pair: (-pair[1], pair[0]))
    return " ".join(f"{pizza} {n}" for pizza, n in ranked) or "none"


def can(s: State, pizza: str) -> str:
    if pizza not in s.recipes:
        return "ERROR unknown pizza"
    need = Counter(s.recipes[pizza])
    return str(min(s.pantry.get(item, 0) // n for item, n in need.items()))


def step(words: list[str], s: State) -> tuple[str, State]:
    match words:
        case ["RESTOCK", item, qty] if positive(qty):
            return restock(s, item, int(qty))
        case ["TRASH", item, qty] if positive(qty):
            return trash(s, item, int(qty))
        case ["STOCK", item]:
            return str(s.pantry.get(item, 0)), s
        case ["RECIPE", pizza, *ingredients] if ingredients:
            return "OK", s._replace(recipes={**s.recipes, pizza: ingredients})
        case ["ORDER", pizza]:
            return order(s, pizza)
        case ["SALES"]:
            return report(s.sales), s
        case ["CAN", pizza]:
            return can(s, pizza), s
        case _:
            return "ERROR invalid command", s


def main() -> None:
    state = State({}, {}, {})
    for line in sys.stdin:
        words = line.split()
        if words:
            answer, state = step(words, state)
            print(answer)


if __name__ == "__main__":
    main()
