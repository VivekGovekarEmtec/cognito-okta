
from typing import Dict, List
from io import BytesIO
import xlsxwriter


def convert_to_excel(data: List[Dict[str, any]], headers: List[str]):
    try:
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        # Write headers to the Excel sheet
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)

        if data:
            # Write data to the Excel sheet if available
            for row, item in enumerate(data, start=1):
                for col, value in enumerate(item.values()):
                    worksheet.write(row, col, value)

        workbook.close()
        output.seek(0)

        return output
    except Exception as e:
        print(f"An error occurred during Excel conversion: {e}")
        return None
