import pandas as pd
import Item_Formatter as IF

# Open the Excel file and read it into a DataFrame
df = pd.read_excel('COMPO.xlsx')

# Open a csv file where the data will be written
with open('COMPO.csv', 'w') as file:
    # Write the header
    file.write('id,group,weapon,off hand,helmet,armor,boots,cape,food\n')
    
    # Open formatter
    formatter = IF.Item_Formatter('items.txt')

    # Iterate over the rows of the DataFrame
    groups_max = [8, 7]
    current_group = 0
    group_count = 0
    for index, row in df.iterrows():
        # Write the item name and tier to the csv file
        weapon_row = row['ARMA'].split('/')
        weapon = formatter.format(weapon_row[0], 8)
        off_hand = ''
        if len(weapon_row) > 1:
            off_hand = formatter.format(weapon_row[1], 8)
        helmet = formatter.format(row['CASCO'], 8)
        armor = formatter.format(row['PECHO'], 8)
        boots = formatter.format(row['BOTAS'], 8)
        cape = formatter.format(row['CAPA'], 8)
        food = formatter.format(row['COMIDA'], 8)
        potion = formatter.format(row['POCION'], 8)
        file.write(f"{index},{current_group},{weapon},{off_hand},{helmet},{armor},{boots},{cape},{food}\n")
        if current_group < len(groups_max):
            group_count += 1
            if group_count == groups_max[current_group]:
                current_group += 1
                group_count = 0

    