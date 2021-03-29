from . import get_foods

for food in get_foods():
    print(food["ds"])
    print(food["url"])
    print("==== 아침 =====")
    print(food["breakfast"])
    print("==== 점심 =====")
    print(food["lunch"])
    print("==== 저녁 =====")
    print(food["dinner"])
    print("\n\n\n")
