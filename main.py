from ui import Application

def main():
    app = Application(extractItems, calculateCosts)
    app.exec()

# Based on user selections, divides the cost of each item up between the contributors
def calculateCosts(items, app):
    costs = [0] * 4
    contribs = [False] * 4
    uiItemListLayout = app.itemList.layout()

    for i in range(len(items)):
        uiItemBox = uiItemListLayout.itemAt(i).widget()
        contribs[0] = uiItemBox.checkBox1.isChecked()
        contribs[1] = uiItemBox.checkBox2.isChecked()
        contribs[2] = uiItemBox.checkBox3.isChecked()
        contribs[3] = uiItemBox.checkBox4.isChecked()
        
        price = items[i][2]
        divisor = contribs.count(True)

        if divisor == 0: continue

        for i in range(len(costs)):
            if contribs[i]:
                costs[i] += price / divisor

    costStrings = [""] * 4
    for i in range(len(costs)):
        costStrings[i] = "£" + "{:,.2f}".format(round(costs[i]) / 100)

    app.cost1.setText(costStrings[0])
    app.cost2.setText(costStrings[1])
    app.cost3.setText(costStrings[2])
    app.cost4.setText(costStrings[3])

# Extracts item names, quantities and costs from a given .eml file into an array of tuples
def extractItems(filepath) -> list[tuple[str, int, int]]:
    # Open file
    file = open(filepath, "r")

    items = []

    line = ""

    # Jump to start of xml portion
    while "!DOCTYPE" not in line:
        line = file.readline()

    # Order changes loop
    while True:
        # Jump to next order change or start of receipt
        while ("We Sent" not in line) and ("Your Order" not in line):
            line = file.readline()

        # If reached start of receipt, exit loop
        if "Your Order" in line: break

        # Skip to & extract item name
        skipTags(file, 2)
        itemName = extractText(file)

        # Get quantity from item name
        itemQuantity = int(itemName[0])
        itemName = itemName[4:]

        if len(itemName) > 60:
            itemName = itemName[:60] + "..."

        # Skip to & extract item price
        line = file.readline()
        skipTags(file, 1)
        itemPrice = extractPrice(file)

        items.append((itemName, itemQuantity, itemPrice))

    # Jump to end of receipt header
    while "price" not in line.lower():
        line = file.readline()

    # Jump to start of items
    skipTags(file, 1)

    # Receipt loop
    while True:
        # Skip to and extract item name
        skipTags(file, 2)
        itemName = extractText(file)

        # If we reach the end of the receipt, stop
        if itemName == "": break

        if len(itemName) > 60:
            itemName = itemName[:60] + "..."

        # Skip to and extract item quantity
        skipTags(file, 2)
        itemQuantity = extractNum(file)
        
        # Skip to and extract item quantity
        skipTags(file, 2)
        itemPrice = extractPrice(file)

        items.append((itemName, itemQuantity, itemPrice))

        skipTags(file, 2)

    file.close()

    return items

# Moves file pointer to the end of the next n tags
def skipTags(file, n) -> None:
    # Find end of next n tags
    tagCount = 0
    while tagCount < n:
        if file.read(1) == ">":
            tagCount += 1

# Extracts text up until the start of the next tag, then strips and formats
def extractText(file) -> str:
    # Extract item name up until start of next tag
    text = ""
    char = ""
    while char != "<":
        text += char
        char = file.read(1)

    # Strip junk in item name
    return text.replace("&amp;", "&").lstrip().rstrip()

# Extracts text up until the start of the next tag, then strips and formats as price
def extractNum(file) -> int:
    # Extract number as string
    num = extractText(file)

    # Convert to integer
    return int(num)

# Extracts text up until the start of the next tag, then strips and formats as price
def extractPrice(file) -> int:
    # Extract price as string
    price = extractText(file)

    # Convert to price in pence
    return int(price.replace("Â£", "").replace(".", ""))

if __name__ == "__main__":
    main()