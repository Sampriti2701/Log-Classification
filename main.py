import os
import pandas as pd
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
from classify import classify  # Ensure classify.py exists and works correctly

app = FastAPI()

# Ensure the output directory exists
OUTPUT_DIR = "resources"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/classify/")
async def classify_logs(file: UploadFile):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV.")

    try:
        # Read the uploaded CSV
        df = pd.read_csv(file.file)
        file.file.close()  # Close file after reading to prevent resource leaks

        # Validate required columns
        required_columns = {"source", "log_message"}
        if not required_columns.issubset(df.columns):
            raise HTTPException(status_code=400, detail="CSV must contain 'source' and 'log_message' columns.")

        # Perform classification
        df["target_label"] = classify(list(zip(df["source"], df["log_message"])))

        # Save the modified file
        output_file = os.path.join(OUTPUT_DIR, "output.csv")
        df.to_csv(output_file, index=False)

        print(f"File saved successfully: {output_file}")
        return FileResponse(output_file, media_type='text/csv', filename="classified_output.csv")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")