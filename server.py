import os
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses  import HTMLResponse, JSONResponse
from fastapi.templating  import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Import existing backend modules
from src.pdf_extractor import extract_text_from_pdf
from src.preprocessing  import tokenize_sentences, preprocess_sentence, download_nltk_data
from src.summarizer import score_sentences, generate_summary
from src.other  import compute_statistics

# Ensure NLTK datasets are downloaded
download_nltk_data()


app = FastAPI(title="AI PDF Summarizer Backend")

# setup templates
templates = Jinja2Templates(directory="frontend")



#make sure we have a static folder even if empty
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_landing_page(request: Request):
    """Serves the main workspace page (workspace.html)."""
    return templates.TemplateResponse("workspace.html", {"request": request})


@app.post("/api/summarize")
async def api_summarize(file: UploadFile = File(...), summary_length: str = Form("medium")):
    """
    API endpoint to process an uploaded PDF and return the summary.
    summary_length should be one of: 'short', 'medium', 'long'
    """
    try:
        # read file bytes
        file_bytes = await file.read()
        
        # extract text
        extracted_text, num_pages = extract_text_from_pdf(file_bytes)
        
        if not extracted_text.strip():
            return JSONResponse(
                status_code=400, 
                content={"error": "Could not extract text from PDF. It might be scanned or corrupted."}
            )
        
            
        #tokenize and filter sentences
        raw_sentences = tokenize_sentences(extracted_text)
        original_sentences = [s for s in raw_sentences if len(s.split()) > 3]
        
        if len(original_sentences) < 2:
            return JSONResponse(
                status_code=400, 
                content={"error": "The document is too short to summarize (fewer than 2 sentences)."}
            )

            
        #preprocess sentences
        preprocessed_sentences = [preprocess_sentence(s) for s in original_sentences]
        
        # score sentences
        scored_sentences = score_sentences(original_sentences, preprocessed_sentences)
        
        # Map summary length to ratio
        ratio_map = {
            "short": 0.3,
            "medium": 0.4,
            "long": 0.6,
        }
        ratio = ratio_map.get(summary_length.lower(), 0.4)


        
        # generate summary
        summary_text, top_sentences = generate_summary(original_sentences, scored_sentences, ratio=ratio)
        
        # statistics
        stats = compute_statistics(
            extracted_text, 
            summary_text, 
            num_pages
        )


        
        # format the summary text
        html_summary = summary_text.replace("\n", "<br>").replace("**Key Highlights:**", "<strong>Key Highlights:</strong>")
        
        return {
            "success": True,
            "summary": html_summary,
            "stats": stats,
            "extracted_text": extracted_text
        }
    
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred during summarization: {str(e)}"}
        )




if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
