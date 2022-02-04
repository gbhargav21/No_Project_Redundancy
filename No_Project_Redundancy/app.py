from flask import*
import sqlite3
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)


conn = sqlite3.connect('finaldb',check_same_thread=False)

def dataext():
    l=[]
    cursor = conn.execute("SELECT ID,title,abstract,components,introduction from finaldemo")
    for row in cursor:
        l.append(row)
    conn.close()
    return "Operation Successful.."

def vectorize(Text): return TfidfVectorizer().fit_transform(Text).toarray()
def similarity(doc1, doc2): return cosine_similarity([doc1, doc2])

def major():
    l=[]
    cursor = conn.execute("SELECT ID,title,abstract,components,introduction from finaldemo")
    for row in cursor:
        l.append(row)
    idb=[]
    title=[]
    abstract=[]
    components=[]
    inro=[]
    p=''
    result=[]
    #op=len(idb)
    #op=int(input("Enter index"))
    for i in range(len(l)):
        p=l[i]
        idb.append(p[0])
        title.append(p[1])
        abstract.append(p[2])
        components.append(p[3])
        inro.append(p[4])
        #l=int(input("Enter which index should be  checked against remaining"))
        op=len(idb)
        vectors = vectorize(title)
        vectors1 = vectorize(abstract)
        vectors2 = vectorize(components)
        vectors3 = vectorize(inro)
    for i in range(len(idb)):
        res=''
        if(idb[i]==op):
            p=''
        else:
            opl="Title plag check for"+str(idb[i])+" "+str(op)+"="+str(similarity(vectors[i],vectors[op-1])[0][1]*100)
            res=res+" "+opl
            #print("Title plag check for",idb[i],op,"=",similarity(vectors[i],vectors[op-1])[0][1]*100)
            #print("Abstract plag check for",idb[i],op,"=",similarity(vectors1[i],vectors1[op-1])[0][1]*100)
            opl="Abstract plag check for"+str(idb[i])+" "+str(op)+"="+str(similarity(vectors1[i],vectors1[op-1])[0][1]*100)
            res=res+" "+opl
            #print("Components plag check for",idb[i],op,"=",similarity(vectors2[i],vectors2[op-1])[0][1]*100)
            #print("Introduction plag check for",idb[i],op,"=",similarity(vectors3[i],vectors3[op-1])[0][1]*100)
            #print()
            opl="Components plag check for"+str(idb[i])+" "+str(op)+"="+str(similarity(vectors2[i],vectors2[op-1])[0][1]*100)
            res=res+" "+opl
            opl="Introduction plag check for"+str(idb[i])+" "+str(op)+"="+str(similarity(vectors3[i],vectors3[op-1])[0][1]*100)
            res=res+" "+opl
            result.append(res)
    return result


def database():
    print("Opened database successfully")
    conn.execute('''CREATE TABLE finaldemo
         (ID             INT     NOT NULL,
         title           TEXT    NOT NULL,
         abstract        TEXT    NOT NULL,
         components      TEXT    NOT NULL,
         authors         TEXT    NOT NULL,
         introduction    TEXT   NOT NULL);''')
    print ("Table created successfully")
    conn.close()

def enter_user_data(a,b,c,d,e,f):
    ID=a
    title=b
    abstract=c
    components=d
    authors=e
    introduction=f

    data=(ID,title,abstract,components,authors,introduction)
    query=('''INSERT INTO finaldemo (ID,title,abstract,components,authors,introduction)VALUES (?,?,?,?,?,?)''');
    conn.execute(query,data);
    conn.commit()
    return "Operation Successfull...."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/output",methods=['GET','POST'])
def hel():
  return "Bhargav"





@app.route('/output/',methods=['GET','POST'])
def output():
    if request.method=='POST':
        id1=request.form.get("idiz")#id
        tb=request.form.get("idi")#title
        ab=request.form.get('idii')#abstract
        com=request.form.get("id3")#components
        aut=request.form.get("id4")#authors
        int1=request.form.get("id2")#introduction
        if request.form['button_check']=='check_similarity':
            print(enter_user_data(id1,tb,ab,com,aut,int1))
            gb=major()
            return render_template("output.html",a=tb,b=ab,c=int1,d=com,e=aut,z=id1,zz=gb)
        else:
            return "BHARGAV"


if __name__ == '__main__':
  app.run(debug = True)