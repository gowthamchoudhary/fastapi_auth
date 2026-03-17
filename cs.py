def cost_product(product, price):
    product = product.replace('"', '').replace("'", '')

    if product.isdigit() and len(product) == 5:
        try:
            price = float(price)
            print(product, "costs Rs.", price)
        except:
            print("Invalid Input")
    else:
        print("Invalid Input")


# read all input at once
data = input().split()

# process in pairs
for i in range(0, len(data), 2):
    if i + 1 < len(data):
        cost_product(data[i], data[i+1])