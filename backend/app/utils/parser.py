import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def detect_document_type(text: str) -> str:
    prompt = f"""Analyze this extracted text and classify the document type.

Rules:
- If it mentions bank, transaction, transfer, IBFT, account number → BANK_SLIP
- If it mentions invoice number, vendor, bill to, GST, due date → INVOICE  
- If it mentions identity card, CNIC, NIC, national identity → ID_CARD
- If it mentions store, items purchased, POS receipt → RECEIPT
- Otherwise → UNKNOWN

Return ONLY one word: BANK_SLIP, INVOICE, ID_CARD, RECEIPT, or UNKNOWN

Text:
{text[:500]}

Document type:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10,
        temperature=0
    )
    result = response.choices[0].message.content.strip().upper()
    valid = ["BANK_SLIP", "INVOICE", "ID_CARD", "RECEIPT", "UNKNOWN"]
    for v in valid:
        if v in result:
            return v
    return "UNKNOWN"


def parse_document(text: str, doc_type: str) -> dict:
    prompts = {
        "BANK_SLIP": """Extract these fields from the bank slip text and return as JSON:
{
  "transaction_id": "",
  "date": "",
  "time": "",
  "sender_name": "",
  "receiver_name": "",
  "bank_name": "",
  "amount": "",
  "currency": "",
  "transaction_type": "",
  "reference_number": "",
  "status": ""
}""",
        "INVOICE": """Extract these fields from the invoice text and return as JSON:
{
  "invoice_number": "",
  "vendor_name": "",
  "bill_to": "",
  "date": "",
  "due_date": "",
  "subtotal": "",
  "tax": "",
  "total_amount": "",
  "currency": "",
  "line_items": []
}""",
        "ID_CARD": """Extract these fields from the ID card text and return as JSON:
{
  "full_name": "",
  "father_name": "",
  "date_of_birth": "",
  "id_number": "",
  "issue_date": "",
  "expiry_date": "",
  "gender": "",
  "address": ""
}""",
        "RECEIPT": """Extract these fields from the receipt text and return as JSON:
{
  "store_name": "",
  "date": "",
  "time": "",
  "items": [],
  "subtotal": "",
  "tax": "",
  "total": "",
  "payment_method": ""
}"""
    }

    prompt = f"""{prompts.get(doc_type, '{"extracted_text": ""}')}

IMPORTANT: Return ONLY the JSON object. No explanation, no markdown, no code blocks. Just raw JSON.

Document text:
{text}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    # Find JSON object in response
    start = raw.find("{")
    end = raw.rfind("}") + 1
    if start != -1 and end != 0:
        raw = raw[start:end]

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw_response": raw}