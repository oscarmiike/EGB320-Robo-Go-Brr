import pandas as pd
import numpy as np

def process_order_file(file_name):
    """
    Process the order CSV file, optimize the order based on row and shelf logic,
    map the item names to corresponding numbers, and return six order lists.

    Parameters:
    - file_name (str): The path to the CSV file to process.

    Returns:
    - List of six orders, where each order is a list containing [Item Number, Shelf, Height, Bay, Mapped Item Number, Row]
    """

    # Step 1: Load the CSV into a DataFrame
    df = pd.read_csv(file_name, encoding='utf-8-sig')

    # Step 2: Calculate the row based on 'Shelf'
    df['Row'] = df['Shelf'] // 2

    # Step 3: Map the item names to numbers, with a space in front of 'Cube'
    item_name_mapping = {
        ' Cube': 0,            # Space added in front of 'Cube'
        'Weetbots': 1,
        'Soccer Ball': 2,      # Assuming "Ball" refers to a soccer ball
        'Bottle': 3,
        'Bowl': 4,
        'Cup': 5               # Assuming "Mug" refers to "Cup"
    }

    # Apply the mapping to the 'Item Name' column
    df['Item Number Mapped'] = df['Item Name'].map(item_name_mapping)

    # Step 4: Optimize the order based on the custom logic:
    # - Pick 1 item from Row 2 first (closest to the start)
    # - Then pick all items from Row 0 (closest to drop-off)
    # - Then pick all items from Row 1
    # - Finally, finish remaining items in Row 2

    # Step 4.1: Pick the closest item from Row 2 (only one item initially)
    first_item_row_2 = df[df['Row'] == 2].head(1)

    # Step 4.2: Finish all the items in Row 0
    remaining_row_0 = df[df['Row'] == 0]

    # Step 4.3: Finish all the items in Row 1
    remaining_row_1 = df[df['Row'] == 1]

    # Step 4.4: Finish any remaining items in Row 2 (excluding the one picked first)
    remaining_row_2 = df[(df['Row'] == 2) & (df.index != first_item_row_2.index[0])]

    # Step 4.5: Concatenate the dataframes in the desired order
    final_order_df = pd.concat([first_item_row_2, remaining_row_0, remaining_row_1, remaining_row_2])

    # Reset index for cleaner output
    final_order_df = final_order_df.reset_index(drop=True)

    # Step 5: Create a list to store all the orders as individual lists
    orders = []

    # Step 6: Iterate over each row and append the values to the list
    for index, row in final_order_df.iterrows():
        # Create a list for each order with the desired columns in specific positions
        order = [
            row['Item Number'],       # order[0]: Item Number
            row['Shelf'],             # order[1]: Shelf
            row['Height'],            # order[2]: Height
            row['Bay'],               # order[3]: Bay
            row['Item Number Mapped'],# order[4]: Mapped Item Number
            row['Row']                # order[5]: Row (calculated based on shelf)
        ]
        # Append the order list to the orders list
        orders.append(order)

    # Step 7: Return the six order lists (assuming the file contains at least 6 orders)
    return orders[:6]

# # Example usage:
# file_name = "D:\QUT\SEM2 2024\EGB320\EGB320_COPPELIA_FILES_V1.4.3\EGB320_COPPELIA_FILES_V1.4.3\COPPELIA_PythonCode\Order_1.csv"  # Replace with your file path
# order_lists = process_order_file(file_name)

# # Print the six orders
# # for i, order in enumerate(order_lists, 1):
# #     print(f"Order {i}: {order}")
# print(order_lists[0])
# print(order_lists[0][5])
