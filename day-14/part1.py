scores = '37'
first_recipe = 0
second_recipe = 1
recipes = 540561

while len(scores) <= (recipes+10):
    first_score = int(scores[first_recipe])
    second_score = int(scores[second_recipe])

    scores += str(first_score + second_score)

    first_recipe = (first_recipe + first_score + 1) % len(scores)
    second_recipe = (second_recipe + second_score + 1) % len(scores)

print(scores[recipes:recipes+10])
