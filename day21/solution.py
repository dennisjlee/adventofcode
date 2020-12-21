import functools
import itertools
import re
import sys

INGREDIENT_PARSER = re.compile(r'([\w ]+)(?:\(contains (.*)\))?')


class IngredientList:
    def __init__(self, line):
        match = INGREDIENT_PARSER.match(line.strip())
        self.ingredients = set(match.group(1).strip().split(' '))
        self.allergens = set(match.group(2).split(', ')) if match.group(2) else set()

    def __repr__(self):
        return f'IngredientList(ingredients={repr(self.ingredients)}, allergens={repr(self.allergens)}'


def main():
    with open(sys.argv[1]) as f:
        ingredient_lists = [IngredientList(line) for line in f.readlines()]

    # part1
    possible_ingredients = {}
    for il in ingredient_lists:
        for allergen in il.allergens:
            if allergen in possible_ingredients:
                possible_ingredients[allergen] &= il.ingredients
            else:
                possible_ingredients[allergen] = il.ingredients.copy()

    all_ingredients = functools.reduce(lambda ing, il2: ing | il2.ingredients, ingredient_lists, set())
    possible_allergen_ingredients = set(itertools.chain(*possible_ingredients.values()))
    non_allergen_ingredients = all_ingredients - possible_allergen_ingredients
    non_allergen_appearances = 0
    for il in ingredient_lists:
        for ingredient in il.ingredients:
            if ingredient in non_allergen_ingredients:
                non_allergen_appearances += 1
    print(non_allergen_appearances)

    # part2
    final_allergen_map = {}
    while possible_ingredients:
        allergen, ingredients = next(item for item in possible_ingredients.items() if len(item[1]) == 1)
        allergen_ingredient = ingredients.pop()
        final_allergen_map[allergen] = allergen_ingredient
        del possible_ingredients[allergen]
        for ingredients in possible_ingredients.values():
            ingredients.discard(allergen_ingredient)

    print(','.join(ingredient for allergen, ingredient in sorted(final_allergen_map.items())))




if __name__ == '__main__':
    main()
