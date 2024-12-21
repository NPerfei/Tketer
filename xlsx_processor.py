import database_manager as dbm
from openpyxl import workbook as wb
from openpyxl.styles import Font, Alignment

def create_excel_sheet(database: dbm.DatabaseManager, filter: str, filepath: str):
    try:
        all_data = database.get_data(filter)
        converted_data =[]
        count = 1
        
        for data in all_data:
            converted_data.append([count, data[1], data[2], data[3].strftime("%m/%d/%Y"), f"{data[0]:06d}"])
            count += 1
        

        work_book = wb.Workbook()
        current_work_book = work_book.active
        current_work_book.title = "Tickets"

        column_lengths = [5, 35, 15, 15, 10]
        columns = ['A', 'B', 'C', 'D', 'E']

        for i in range(len(columns)):
            current_work_book.column_dimensions[columns[i]].width = column_lengths[i]

        column_headers = ["No.", "Name", "Course & Section", "Date", "Ticket No."]
        current_work_book.append(column_headers)

        for heading in current_work_book[1]:
            heading.font = Font(bold=True)
            heading.alignment = Alignment(horizontal="center")

        for row in converted_data:
            current_work_book.append(row)

        work_book.save(filepath)
    except Exception as e:
        print("An error occured while obtaining data:", e)
        raise e
