#Import Library
import json
import os
from flask import Flask
from flask import request
from flask import make_response
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("thaistockadvisor-firebase-adminsdk-3ud1m-9433f3b682.json")
firebase_admin.initialize_app(cred)

# Flask
app = Flask(__name__)
@app.route('/', methods=['POST']) 

def MainFunction():

    #รับ intent จาก Dailogflow
    question_from_dailogflow_raw = request.get_json(silent=True, force=True)
    print('question_from_dailogflow_raw: ', question_from_dailogflow_raw)

    #เรียกใช้ฟังก์ชัน generate_answer เพื่อแยกส่วนของคำถาม
    answer_from_bot = generating_answer(question_from_dailogflow_raw)
    print('answer_from_bot: ', answer_from_bot)
    
    #ตอบกลับไปที่ Dailogflow
    r = make_response(answer_from_bot)
    r.headers['Content-Type'] = 'application/json' #การตั้งค่าประเภทของข้อมูลที่จะตอบกลับไป

    return r

def generating_answer(question_from_dailogflow_dict):

    #Print intent ที่รับมาจาก Dailogflow
    print('intent: ', json.dumps(question_from_dailogflow_dict, indent=4 ,ensure_ascii=False))

    #เก็บค่า ชื่อของ intent ที่รับมาจาก Dailogflow
    intent_group_question_str = question_from_dailogflow_dict["queryResult"]["intent"]["displayName"]
    print('intent_group_question_str: ', intent_group_question_str)

    #ลูปตัวเลือกของฟังก์ชั่นสำหรับตอบคำถามกลับ
    if intent_group_question_str == 'แนะนำหุ้น':
        answer_str = stock_recommentation()
    elif intent_group_question_str == 'ไม่แนะนำหุ้น': 
        answer_str = stock_not_recommentation()
    else: answer_str = "ฉันไม่เข้าใจ คุณต้องการอะไร"

    #สร้างการแสดงของ dict 
    answer_from_bot = {"fulfillmentText": answer_str}
    
    #แปลงจาก dict ให้เป็น JSON
    answer_from_bot = json.dumps(answer_from_bot, indent=4) 
    
    return answer_from_bot

def stock_recommentation(): #ฟังก์ชั่นสำหรับแนะนำหุ้น
    database_ref = firestore.client().document('stock/stock_pos')
    database_dict = database_ref.get().to_dict()
    database_list = list(database_dict.values())
    stock_pos = list_to_string(database_list)
    print('suggest stock: ', stock_pos)

    suggest = 'แนะนำ'
    answer_function = suggest + ' ' + stock_pos
    return answer_function

def stock_not_recommentation(): #ฟังก์ชั่นสำหรับไม่แนะนำ
    database_ref = firestore.client().document('stock/stock_neg')
    database_dict = database_ref.get().to_dict()
    database_list = list(database_dict.values())
    suggest = 'ไม่แนะนำ'
    stock_neg = list_to_string(database_list)

    answer_function = suggest + ' ' + stock_neg
    return answer_function

def list_to_string(stock_list):
    # initialize an empty string
    stocks = ""
    # traverse in the string
    for stock in stock_list:
        stocks += stock + ' '
    return stocks

#Flask
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)
