class Item_Formatter:
    def __init__(self, filepath):
        with open(filepath, 'r') as file:
            self.data = file.readlines()

    def format(self, item_name, tier):
        """
        Converts item name to albion format metadata. Plane of the specified tier or the highest tier if the specified one is not found.
        """

        max_tier = 0
        best_item = None
        # Special cases
        if item_name == "martlock":
            return "T8_CAPEITEM_FW_MARTLOCK"
        elif item_name == "lym":
            return "T8_CAPEITEM_FW_LYMHURST"
        elif item_name == "tortilla":
            return "T7_MEAL_OMELETTE"
        elif item_name == "guiso":
            return "T8_MEAL_STEW"
        elif item_name == "guiso anguila":
            return "T8_MEAL_STEW_FISH"
        # New weapons
        elif "Rootbound" in item_name:
            return "Elder%27s%20Rootbound%20Staff"
        elif "Earthrune" in item_name:
            return "Elder%27s%20Earthrune%20Staff"
        elif "Astral" in item_name:
            return "Elder%27s%20Astral%20Staff"
        elif "Rift" in item_name:
            return "Elder%27s%20Rift%20Glaive"
        elif "Lightcaller" in item_name:
            return "Elder%27s%20Lightcaller"

        # Abre el archivo y lee las líneas
        for line in self.data:
            if item_name in line:
                # Ignores id 
                id = line.split(':')[1].strip()
                
                # Ignores enchantment level
                id = id.split('@')[0]
                
                # Get the tier of the item
                try:
                    current_tier = int(id.split('_')[0][1])
                except ValueError:
                    continue  
                
                # Return if find the exact tier
                if current_tier == tier:
                    return id
                
                # Update the best tier found so far
                if current_tier > max_tier:
                    max_tier = current_tier
                    best_item = id
    
        # Return the best item found if the exact tier is not found
        if best_item == '':
            return "None"
        return best_item
    
#Samples
# file_path = 'items.txt'
# formatter = Item_Formatter(file_path)
# formatted = formatter.format('Rootbound Staff', 4)
# print(formatted)
