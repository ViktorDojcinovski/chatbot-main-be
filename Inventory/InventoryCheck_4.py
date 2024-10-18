import os
import pandas as pd
from fuzzywuzzy import process, fuzz
import re
# from fpdf import FPDF

script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct relative paths
inventory_path = os.path.join(script_dir, "TireInventoryFinal.xlsx")
mapping_path = os.path.join(script_dir, "MappingTable.xlsx")
get_size_path = os.path.join(script_dir, "Get_Size.xlsx")

# Load the data frames
inventory_df = pd.read_excel(inventory_path)
mapping_df = pd.read_excel(mapping_path)
Get_Size_df = pd.read_excel(get_size_path)

def fuzzy_match(query, choices):
    best_match = process.extractOne(query.lower(), choices, scorer=fuzz.WRatio)
    if best_match and best_match[1] >= 80:
        return best_match
    return None

def strip_non_numeric(input_string):
    return re.sub(r'\D', '', input_string)

def check_stock_bts(V_type, tire_type, size, stock):
    matched_V_car = fuzzy_match(V_type, mapping_df['Car'].unique())
    matched_V_van = fuzzy_match(V_type, mapping_df['Van'].unique())
    matched_V_truck = fuzzy_match(V_type, mapping_df['Truck'].unique())

    if matched_V_car and (matched_V_van is None or matched_V_car[1] >= matched_V_van[1]) and (matched_V_truck is None or matched_V_car[1] >= matched_V_truck[1]):
        matched_V = "car"
    elif matched_V_van and (matched_V_car is None or matched_V_van[1] >= matched_V_car[1]) and (matched_V_truck is None or matched_V_van[1] >= matched_V_truck[1]):
        matched_V = "van"
    elif matched_V_truck and (matched_V_car is None or matched_V_truck[1] >= matched_V_car[1]) and (matched_V_van is None or matched_V_truck[1] >= matched_V_van[1]):
        matched_V = "truck"
    else:
        matched_V = None

    matched_type_S = fuzzy_match(tire_type, mapping_df['Summer'].unique())
    matched_type_W = fuzzy_match(tire_type, mapping_df['Winter'].unique())
    matched_type_AS = fuzzy_match(tire_type, mapping_df['All-Season'].unique())

    if matched_type_S and (matched_type_W is None or matched_type_S[1] >= matched_type_W[1]) and (matched_type_AS is None or matched_type_S[1] >= matched_type_AS[1]):
        matched_type = "Summer"
    elif matched_type_W and (matched_type_S is None or matched_type_W[1] >= matched_type_S[1]) and (matched_type_AS is None or matched_type_W[1] >= matched_type_AS[1]):
        matched_type = "Winter"
    elif matched_type_AS and (matched_type_S is None or matched_type_AS[1] >= matched_type_S[1]) and (matched_type_W is None or matched_type_AS[1] >= matched_type_W[1]):
        matched_type = "All-Season"
    else:
        matched_type = None

    size_striped = str(strip_non_numeric(size))

    stock = int(stock)

    if matched_V and matched_type and size_striped:
        inventory_df['vehicle type'] = inventory_df['vehicle type'].astype(str).str.lower().str.strip()
        inventory_df['Season'] = inventory_df['Season'].astype(str).str.lower().str.strip()
        inventory_df['Sizes'] = inventory_df['Sizes'].astype(str).str.strip()

        filtered_data = inventory_df[
            (inventory_df['vehicle type'] == matched_V.lower()) & 
            (inventory_df['Season'] == matched_type.lower()) &
            (inventory_df['Sizes'] == size_striped) &
            (inventory_df['stock'] >= stock) &
            (inventory_df['stock'] >= 1)
        ]
        # DEBUGGING
        # print(filtered_data)

        # pdf = PDF()
        # pdf.add_page()

        # pdf.chapter_title('Ponuda')
        # pdf.add_dataframe(filtered_data)

        # pdf_output = 'C:\\Users\\Damjan Janakievski\\RASA ENV\\ChatbotV3\\Inventory\\output.pdf'
        # pdf.output(pdf_output)
            # DEBUGGING
    
        print(filtered_data)
        if not filtered_data.empty:
            return filtered_data
        elif stock <= 0:
            return "Please insert a quantity greater than 0. For example (1,4,5)"
        else:
            return f"No tires in stock from type:{matched_V},{matched_type},{size_striped},{stock}"
    
        
        
# class PDF(FPDF):
#     def header(self):
#         self.set_font('Arial', 'B', 12)
#         self.cell(0, 10, 'Title of the PDF', 0, 1, 'C')

#     def footer(self):
#         self.set_y(-15)
#         self.set_font('Arial', 'I', 8)
#         self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

#     def chapter_title(self, title):
#         self.set_font('Arial', 'B', 12)
#         self.cell(0, 10, title, 0, 1, 'L')
#         self.ln(10)

#     def chapter_body(self, body):
#         self.set_font('Arial', '', 12)
#         self.multi_cell(0, 10, body)
#         self.ln()

#     def add_dataframe(self, df):
#         self.set_font('Arial', 'B', 12)
#         for col in df.columns:
#             self.cell(40, 10, col, 1)
#         self.ln()

#         self.set_font('Arial', '', 12)
#         for i in range(len(df)):
#             for col in df.columns:
#                 self.cell(40, 10, str(df[col].iloc[i]), 1)
#             self.ln()




def check_vehicle_type(V_type):
    matched_V_car = fuzzy_match(V_type, mapping_df['Car'].unique())
    matched_V_van = fuzzy_match(V_type, mapping_df['Van'].unique())
    matched_V_truck = fuzzy_match(V_type, mapping_df['Truck'].unique())

    if matched_V_car and (matched_V_van is None or matched_V_car[1] >= matched_V_van[1]) and (matched_V_truck is None or matched_V_car[1] >= matched_V_truck[1]):
        matched_V = "car"
    elif matched_V_van and (matched_V_car is None or matched_V_van[1] >= matched_V_car[1]) and (matched_V_truck is None or matched_V_van[1] >= matched_V_truck[1]):
        matched_V = "van"
    elif matched_V_truck and (matched_V_car is None or matched_V_truck[1] >= matched_V_car[1]) and (matched_V_van is None or matched_V_truck[1] >= matched_V_van[1]):
        matched_V = "truck"
    else:
        matched_V = None

    return matched_V


def check_tire_type(tire_type):
    matched_type_S = fuzzy_match(tire_type, mapping_df['Summer'].unique())
    matched_type_W = fuzzy_match(tire_type, mapping_df['Winter'].unique())
    matched_type_AS = fuzzy_match(tire_type, mapping_df['All-Season'].unique())

    if matched_type_S and (matched_type_W is None or matched_type_S[1] >= matched_type_W[1]) and (matched_type_AS is None or matched_type_S[1] >= matched_type_AS[1]):
        matched_type = "summer season"
    elif matched_type_W and (matched_type_S is None or matched_type_W[1] >= matched_type_S[1]) and (matched_type_AS is None or matched_type_W[1] >= matched_type_AS[1]):
        matched_type = "winter season"
    elif matched_type_AS and (matched_type_S is None or matched_type_AS[1] >= matched_type_S[1]) and (matched_type_W is None or matched_type_AS[1] >= matched_type_W[1]):
        matched_type = "all season"
    else:
        matched_type = None
    return matched_type

def check_tire_size(size):
    size_striped = strip_non_numeric(size)

    return size_striped


def get_tire_size(model,maker,year):
    filtered_data = Get_Size_df[
            (Get_Size_df['Car Maker'] == maker) & 
            (Get_Size_df['Car Model'] == model) &
            (Get_Size_df['Year'] == int(year))
        ]
    try:
        first_item_str = str(filtered_data['Wheel Size'].iloc[0])
    except IndexError:
        print(filtered_data)
    print(first_item_str)
    return first_item_str


# if __name__ == "__main__":
#     print(get_tire_size("Corolla","Toyota",2020))