from flask import Flask,jsonify,json,request,make_response
import jwt
import flask_jwt,requests
import datetime
from functools import wraps

app=Flask(__name__)#define app flask
app.config['SECRET_KEY']='mysecretkey'
#Creante new Annotation ,Apply Token Auth
def token_required(func):
    @wraps(func)
    def decorated(*args,**kwargs):
        #auth = request.headers.get('Authorization'); the orginal encypt Token
        #Bearer affafffffjljfljfljfljfljfljf
        #----------------------------
        #get token from URL
        token=request.args.get('token')#http://172.0.0.1:8000/route?token=sfjslfsfjsjffslfjs
        if(token):
                try:
                    #VERIFY TOKEN
                    data=jwt.decode(token,app.config['SECRET_KEY'])
                except:
                    return jsonify({'message':'Token is invalid!'}),403
                #if pass return function back
                return func(*args, **kwargs)
        else:
            return jsonify({'message':'Token is missing!, LOGIN FIRST!'}),403
    return decorated

#Creante new Annotation ,Apply Basic Auth
def auth_required(func):
    @wraps(func)
    def decorated(*args,**kwargs):
        #auth = request.headers.get('Authorization'); the orginal encypt user name and password
        #Basic asfjjfklajflksa
        auth =request.authorization;
        if(auth):
                if(auth.username=="admin" and auth.password=="1233"):
                    # return function if auth success
                    return func(*args,**kwargs)
                else:
                    resp=make_response('Text PAGE: Invalid User and Password!', 401);
                    resp.headers['WWW-Authenticate']= 'Basic realm="Login is requred!"'
                    return resp
        else:
            return make_response('Text PAGE: Could not verify auth!',401,{'WWW-Authenticate':'Basic Realm="Login is requred!"'})
    return decorated

@app.route("/login",methods=['GET'])
@auth_required
def login():
    # CREATE TOKEN
    auth = request.authorization;
    verification_code=str(auth.username) + str(auth.password);
    my_payload = {"verification": verification_code, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)};
    token = jwt.encode(payload=my_payload, key=app.config['SECRET_KEY'], algorithm='HS256');
    return jsonify({'token': token.decode('UTF-8')}), 200

#create entity/relation tblRoom
tblRoom=[
        {"RoomNo":1,"RoomName":"VIP001","Floor":1,"Type":"VIP"},
        {"RoomNo":2,"RoomName":"VIP002","Floor":1,"Type":"VIP"},
        {"RoomNo":3,"RoomName":"201","Floor":2,"Type":"Delux"}
        ]
@app.route("/",methods=['GET'])
@auth_required
@token_required
def home():
    return json.dumps({"message":"RESTful API is working"});

@app.route("/room/all",methods=['GET'])
@auth_required
@token_required
def all_room():
    return jsonify(tblRoom);

@app.route("/room/CRUD00101R001/<int:roomno>",methods=['GET'])
@auth_required
@token_required
def room_findone(roomno):
    result_list={}
    for room in tblRoom:
        if room["RoomNo"]==roomno:
            result_list.update({"RLST_CD": "000", "RLST_SMS": "Successfully!"})
            result_list.update({"DATA":room});
            return jsonify(result_list);

    result_list.update({"RLST_CD": "888", "RLST_SMS": "Result not found!"})
    result_list.update({"DATA": {}});
    return jsonify(result_list);

@app.route("/room/CRUD00101R002/<string:type>",methods=['GET'])
@auth_required
@token_required
def room_findtype(type):
    result_list = {}
    result=[]
    for room in tblRoom:
        if room["Type"] == type:
            result.append(room)

    if(len(result)>0):
        result_list.update({"RLST_CD": "000", "RLST_SMS": "Successfully!"})
        result_list.update({"DATA": result});
    else:
        result_list.update({"RLST_CD": "888", "RLST_SMS": "Result not found!"})
        result_list.update({"DATA": result});

    return jsonify(result_list);

@app.route("/room/CRUD00101C001",methods=['POST'])
@auth_required
@token_required
def room_addone():
    result_list = {}
    try:
        #===1-Data Validation---------
        if(len(request.json)!=4):
            result_list.update({"RLST_CD": "701", "RLST_SMS": "Invalid Business Data!"})
            return jsonify(result_list);
        #ROOM_NO
        if ("ROOM_NO" not in request.json):
            result_list.update({"RLST_CD": "702", "RLST_SMS": "Not Exist ROOM_NO!"})
            return jsonify(result_list);
        #ROOM_NAME
        if ("ROOM_NAME" not in request.json):
            result_list.update({"RLST_CD": "703", "RLST_SMS": "Not Exist ROOM_NAME!"})
            return jsonify(result_list);
        #TYPE
        if ("TYPE" not in request.json):
            result_list.update({"RLST_CD": "704", "RLST_SMS": "Not Exist TYPE!"})
            return jsonify(result_list);
        #FLOOR
        if ("FLOOR" not in request.json):
            result_list.update({"RLST_CD": "705", "RLST_SMS": "Not Exist FLOOR!"})
            return jsonify(result_list);
        #===1-End Data Validation
        no = request.json['ROOM_NO']
        name = request.json['ROOM_NAME']
        floor = request.json['FLOOR']
        type = request.json['TYPE']
        record={"RoomNo":int(no),"RoomName":name,"Floor":int(floor),"Type":type}
        tblRoom.append(record)

        result_list.update({"RLST_CD": "000", "RLST_SMS": "Successfully!"})
        result_list.update({"DATA": tblRoom})
        return jsonify(result_list);
    except Exception as err:
        print("=============","CRUD00101C001","=============")
        print(err)
        print("=============", "CRUD00101C001", "=============")
        result_list.update({"RLST_CD": "999", "RLST_SMS": "Unhandle Error!"})
        return jsonify(result_list);

@app.route("/room/CRUD00101U001/<int:roomno>",methods=['PUT'])
@auth_required
@token_required
def room_editone(roomno):
    result_list = {}
    try:
        #===1-Data Validation---------
        if(len(request.json)!=3):
            result_list.update({"RLST_CD": "701", "RLST_SMS": "Invalid Business Data!"})
            return jsonify(result_list);
        #ROOM_NAME
        if ("ROOM_NAME" not in request.json):
            result_list.update({"RLST_CD": "703", "RLST_SMS": "Not Exist ROOM_NAME!"})
            return jsonify(result_list);
        #TYPE
        if ("TYPE" not in request.json):
            result_list.update({"RLST_CD": "704", "RLST_SMS": "Not Exist TYPE!"})
            return jsonify(result_list);
        #FLOOR
        if ("FLOOR" not in request.json):
            result_list.update({"RLST_CD": "705", "RLST_SMS": "Not Exist FLOOR!"})
            return jsonify(result_list);
        #===1-End Data Validation

        name = request.json['ROOM_NAME']
        floor = request.json['FLOOR']
        type = request.json['TYPE']

        for room in tblRoom:
            if room["RoomNo"] == roomno:
                room["RoomName"]=name
                room["Type"] = type
                room["Floor"] = floor
                result_list.update({"RLST_CD": "000", "RLST_SMS": "Successfully!"})
                result_list.update({"DATA": tblRoom});
                return jsonify(result_list);

        result_list.update({"RLST_CD": "888", "RLST_SMS": "Update Not Found!"})
        result_list.update({"DATA": tblRoom})
        return jsonify(result_list);
    except Exception as err:
        print("=============","CRUD00101U001","=============")
        print(err)
        print("=============", "CRUD00101U001", "=============")
        result_list.update({"RLST_CD": "999", "RLST_SMS": "Unhandle Error!"})
        return jsonify(result_list);

@app.route("/room/CRUD00101D001",methods=['DELETE'])
@auth_required
@token_required
def room_deleteone():
    result_list = {}
    try:
        #===1-Data Validation---------
        if(len(request.json)!=1):
            result_list.update({"RLST_CD": "701", "RLST_SMS": "Invalid Business Data!"})
            return jsonify(result_list);
        #ROOM_NO
        if ("ROOM_NO" not in request.json):
            result_list.update({"RLST_CD": "702", "RLST_SMS": "Not Exist ROOM_NO!"})
            return jsonify(result_list);
        #===1-End Data Validation

        no = int(request.json['ROOM_NO'])

        for room in tblRoom:
            if room["RoomNo"] == no:
                tblRoom.remove(room)
                result_list.update({"RLST_CD": "000", "RLST_SMS": "Successfully!"})
                result_list.update({"DATA": tblRoom});
                return jsonify(result_list);

        result_list.update({"RLST_CD": "888", "RLST_SMS": "Remove Not Found!"})
        result_list.update({"DATA": tblRoom})
        return jsonify(result_list);
    except Exception as err:
        print("=============","CRUD00101D001","=============")
        print(err)
        print("=============", "CRUD00101D001", "=============")
        result_list.update({"RLST_CD": "999", "RLST_SMS": "Unhandle Error!"})
        return jsonify(result_list);

@app.route("/room/CRUD00101C002",methods=['POST'])
@auth_required
@token_required
def room_addmany():
    result_list = {}
    try:
        #===1-Data Validation---------
        if(len(request.json)!=1):
            result_list.update({"RLST_CD": "701", "RLST_SMS": "Invalid Business Data!"})
            return jsonify(result_list);

        #RECORDS
        if ("RECORDS" not in request.json):
            result_list.update({"RLST_CD": "702", "RLST_SMS": "Not Exist RECORDS!"})
            return jsonify(result_list);

        RECORDS = list(request.json['RECORDS'])

        for rec in RECORDS:
            #ROOM_NO
            if ("ROOM_NO" not in rec):
                result_list.update({"RLST_CD": "703", "RLST_SMS": "Not Exist ROOM_NO!"})
                return jsonify(result_list);
            #ROOM_NAME
            if ("ROOM_NAME" not in rec):
                result_list.update({"RLST_CD": "704", "RLST_SMS": "Not Exist ROOM_NAME!"})
                return jsonify(result_list);
            #TYPE
            if ("TYPE" not in rec):
                result_list.update({"RLST_CD": "705", "RLST_SMS": "Not Exist TYPE!"})
                return jsonify(result_list);
            #FLOOR
            if ("FLOOR" not in rec):
                result_list.update({"RLST_CD": "706", "RLST_SMS": "Not Exist FLOOR!"})
                return jsonify(result_list);
        #===1-End Data Validation
        for rec in RECORDS:
            no = rec['ROOM_NO']
            name =rec['ROOM_NAME']
            floor =rec['FLOOR']
            type =rec['TYPE']
            row={"RoomNo":int(no),"RoomName":name,"Floor":int(floor),"Type":type}
            tblRoom.append(row)

        result_list.update({"RLST_CD": "000", "RLST_SMS": "Successfully!"})
        result_list.update({"DATA": tblRoom})
        return jsonify(result_list);
    except Exception as err:
        print("=============","CRUD00101C002","=============")
        print(err)
        print("=============", "CRUD00101C002", "=============")
        result_list.update({"RLST_CD": "999", "RLST_SMS": "Unhandle Error!"})
        return jsonify(result_list);

#start Flask app runing
if __name__=="__main__":
    app.run(debug=True,port=8000);