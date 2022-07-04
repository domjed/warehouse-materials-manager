def calculateSummary(materials):
    summary = dict()

    selectedPurchasesList = list(
        map(lambda material: material.weight if material.weight > 0 else 0, materials))
    summary["selectedPurchasedMaterials"] = round(
        sum(selectedPurchasesList), 3)

    selectedSellsList = list(
        map(lambda material: material.weight if material.weight < 0 else 0, materials))
    summary["selectedSoldMaterials"] = round(sum(selectedSellsList), 3)

    totalBalance = summary["selectedPurchasedMaterials"] + \
        summary["selectedSoldMaterials"]
    summary["totalBalance"] = round(totalBalance, 3)

    return (summary)
