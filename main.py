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

    # Loop through items
    while True:
        line = ""
        # Jump to next item
        while ("<!-- Product Line -->" not in line):
            line = file.readline()
            # Break if end of receipt
            if ("<!-- Bottom Spacer -->" in line): 
                file.close()
                return items

        # Skip to & extract item quantity
        skipTags(file, 3)
        itemQuantity = extractQuantity(file)

        # Skip to & extract item name
        skipTags(file, 4)
        itemName = extractText(file)

        # Truncate long item names
        if len(itemName) > 60:
            itemName = itemName[:60] + "..."

        # Skip to & extract item price
        skipTags(file, 4)
        itemPrice = extractPrice(file)

        items.append((itemName, itemQuantity, itemPrice))

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
def extractQuantity(file) -> int:
    # Extract number as string
    num = extractText(file)

    # Convert to integer
    return int(num.replace("x", ""))

# Extracts text up until the start of the next tag, then strips and formats as price
def extractPrice(file) -> int:
    # Extract price as string
    price = extractText(file)

    # Convert to price in pence
    return int(price.replace("Â£", "").replace(".", ""))

if __name__ == "__main__":
    main()