# Function to calculate pergola components based on dimensions
def calculate_cut_sheet(dimensions):
    cut_sheet_data = []
    
    for width, length in dimensions:
        height = 108  # Default height = 9ft (108 inches)

        cut_sheet_data.append("Parts | Length | Quantity")
        cut_sheet_data.append(f"Beam | {width}\" | 2")
        cut_sheet_data.append(f" | {length}\" | 2")
        cut_sheet_data.append(f"Post Height | {height - 10}\" | 4")
        cut_sheet_data.append(f"Gutters Width | {width - 5}\" | 2")
        cut_sheet_data.append(f"Gutters Length | {length - 5}\" | 2")
        cut_sheet_data.append("")  # Empty row for spacing

    return "\n".join(cut_sheet_data) if cut_sheet_data else "No dimensions found."

