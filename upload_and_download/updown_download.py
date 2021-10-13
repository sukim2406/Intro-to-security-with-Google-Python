from os import write
from flask import Flask, make_response
import pandas as pd
import numpy as np
import io

app = Flask(__name__)

@app.route("/excel_down", methods=['GET'])
def excel_down():
    data_frame = pd.DataFrame({
        'A': 'fruit drink cookie fruit'.split(),
        'B': 'orange soda pie mango'.split(),
        'C': np.arange(4)})
    
    output = io.BytesIO()
    writer = pd.ExcelWriter(output)
    data_frame.to_excel(writer, 'food')
    writer.save()

    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=download.xlsx'
    response.headers['Content-type'] = "text/csv"
    
    return response

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)

