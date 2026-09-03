import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

load_dotenv()
app=Flask(__name__)

api_key=os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set.")

client=genai.Client(api_key=api_key)
MODEL="gemini-3.1-flash"

SYSTEM_PROMPT="""
You are VehicleCare AI, a vehicle maintenance and troubleshooting assistant.
Help with cars and bikes: starting problems, battery, tyres, engine oil,
service, fuel efficiency, dashboard warnings and basic maintenance.
Give simple, practical and safe guidance. Ask for vehicle model/year and
symptoms when useful. Never encourage dangerous repairs or driving an unsafe
vehicle. For serious brake, steering, fuel leak, smoke, overheating or
electrical problems, advise stopping safely and contacting a qualified mechanic.
If the user writes Tamil or Thanglish, answer in Tamil/Thanglish.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat",methods=["POST"])
def chat():
    data=request.get_json(silent=True) or {}
    user_message=(data.get("message") or "").strip()
    if not user_message:
        return jsonify({"reply":"Please enter a vehicle-related question."}),400
    try:
        response=client.models.generate_content(
            model=MODEL,
            contents=SYSTEM_PROMPT+"\n\nUser question:\n"+user_message
        )
        reply=getattr(response,"text",None) or "Sorry, I couldn't generate a response."
        return jsonify({"reply":reply})
    except Exception as e:
        print("Gemini API Error:",str(e))
        return jsonify({"reply":"Sorry, the AI service is temporarily unavailable. Please try again."}),500

if __name__=="__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port,debug=False)
