from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from django.middleware import csrf
import mysql.connector
import json

config = {
        'user': 'root',
        'password': 'root',
        'host': 'localhost',
        'database': 'bugtracking',
    }



def index(request): 
    return render(request,'index.html')

def bug_info(request):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    ID=int(request.POST.get('req_ID'))
    if ID is None:
        ID = request.session['bug_id'] = request.session.get('req_ID')
    print('ID for bug_info ',ID)
    query=f"select bug_id,bug_name,description,status,workflow,severity,steps from bugdata where id={ID}"
    cursor.execute(query)
    rows=cursor.fetchall()
    print(rows)
    cursor.close()
    conn.close()
    context={'rows':rows}
    return render(request,'bugpage.html',context)

def customer_login(request):
     context = {'show_inv_alert':'False','ul': 'c','showreg':'True'}
     return render(request,'login.html',context)
def tester_login(request):
     context = {'ul': 't','showreg':'True'}
     return render(request,'login.html',context)
def project_manager_login(request):
     context = {'ul': 'p','showreg':'False'}
     return render(request,'login.html',context)
def bug_comments(request):
    id=request.POST.get('bug_id')
    if id is None:
        id = request.session.get('bug_id')
    if id is None:
        # Handle the case when bug_id is not found
        # For example, redirect the user to an error page or display a message
        return HttpResponse("Bug ID not found")
    st=f"bug id {id}'s bug comments page"
    print(st)
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    query=f"select description,bug_id,status,id from bugdata where bug_id={id}"
    cursor.execute(query)
    bug_data=cursor.fetchall()
    print(bug_data)
    desc=bug_data[0][0]
    bugid= bug_data[0][1]
    status=bug_data[0][2]
    req_id=bug_data[0][3]
    query = f"SELECT status_updation, comment, commented_at FROM bug_comments WHERE bug_id = {id} ORDER BY commented_at DESC"
    cursor.execute(query)
    comments=cursor.fetchall()
    print(comments)
    query=f"select status from requests where req_ID={req_id}"
    cursor.execute(query)
    rows=cursor.fetchall()
    request_status= rows[0][0]


    context={'info':st,'id':id,'desc':desc,'bugid':bugid,'status':status,'comments':comments,'request_status':request_status}
    return render(request,'bugcomments1.html',context)

def bug_testst_cmt(request):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    bugid=request.POST.get('bugid')
    id=bugid
    request.session['bug_id'] = id
    status=request.POST.get('statusSelect')
    comment=request.POST.get('comment-box')
    prevstatus=request.POST.get('prevstatus')
    query=f"update bugdata set status='{status}' where bug_id={bugid}"
    cursor.execute(query)
    conn.commit()
    st='Tester SET '+prevstatus+' -> '+status
    print(st)
    query=f'''insert into bug_comments(bug_id,status_updation,comment,commented_at) values({bugid},'{st}',"{comment}",CURRENT_TIMESTAMP)'''
    cursor.execute(query)
    conn.commit()
    return redirect('bug_comments_tester')

def bug_st_cmt(request):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    bugid=request.POST.get('bugid')
    id=bugid
    request.session['bug_id'] = id
    status=request.POST.get('statusSelect')
    comment=request.POST.get('comment-box')
    prevstatus=request.POST.get('prevstatus')
    query=f"update bugdata set status='{status}' where bug_id={bugid}"
    cursor.execute(query)
    conn.commit()
    st='Customer SET '+prevstatus+' -> '+status
    print(st)
    query=f'''insert into bug_comments(bug_id,status_updation,comment,commented_at) values({bugid},'{st}',"{comment}",CURRENT_TIMESTAMP)'''
    cursor.execute(query)
    conn.commit()
    return redirect('bug_comments')

def clog(request):
     em=request.POST.get('em')
     pw=request.POST.get('pw')
     conn = mysql.connector.connect(**config)
     cursor = conn.cursor()
     res=''
     context={'show_inv_alert':'True','ul': 'c','showreg':'True','alert_message':'Invalid Credentials'}
     try:
         query=f"select email,id from customers where email='{em}' and pass='{pw}'"
         cursor.execute(query)
         rows=cursor.fetchall()
         cursor.close()
         conn.close()
         id=rows[0][1]
         request.session['ID'] = id
         if(rows[0][0] == em):
             
             res= 'login success'
             return redirect('user_home')
         else:
             res= 'Invalid Credentials'
             return render(request,'login.html',context)
     except Exception as e:
         res= 'Invalid Credentials'
         return render(request,'login.html',context)


def tlog(request):
    em=request.POST.get('em')
    pw=request.POST.get('pw')
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    res=''
    context={'show_inv_alert':'True','ul': 't','showreg':'True','alert_message':'Invalid Credentials'}
    try:
        query = f"SELECT email,id FROM testers WHERE email='{em}' AND pass='{pw}'"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if rows:  # Check if rows is not None
            id = rows[0][1]  # This should be corrected to rows[0] if email is the first column
            request.session['tester_ID'] = id
            res = 'login success'
            return redirect('newTester')
        else:
            res = 'Invalid Credentials'
            context['alert'] = 'Invalid email or password'  # Add alert message to the context
            context['pwalert'] = ''  # Add empty pwalert to avoid rendering issues
            return render(request, 'login.html', context)
    except Exception as e:
        res = 'Invalid Credentials'
        context['alert'] = 'Invalid email or password'  # Add alert message to the context
        context['pwalert'] = ''  # Add empty pwalert to avoid rendering issues
        return render(request, 'login.html', context)




def plog(request):
    em = request.POST.get('em')
    pw = request.POST.get('pw')
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    res = ''
    context = {'show_inv_alert': 'True', 'ul': 'p', 'showreg': 'True', 'alert_message': 'Invalid Credentials'}
    
    try:
        query = "SELECT email FROM project_manager WHERE email = %s AND password = %s"
        cursor.execute(query, (em, pw))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if row and row[0] == em:
            res = 'login success'
            return redirect('manager_home')
        else:
            res = 'Invalid Credentials'
            return render(request, 'login.html', context)
    except Exception as e:
        res = 'Invalid Credentials'
        return render(request, 'login.html', context)
     

def creg(request):
    if request.method == 'POST':
        em = request.POST.get('em')
        pw = request.POST.get('pw')
        fname = request.POST.get('fname')
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            query = f"insert into customers(email,pass,fname) values('{em}','{pw}','{fname}')"
            cursor.execute(query)
            conn.commit()
            conn.close()
            cursor.close()
            context = {'show_inv_alert': 'True', 'ul': 'c', 'showreg': 'False', 'alert_message': 'Please login with your newly registered account!'}
            return render(request, 'login.html', context)
        except Exception as e:
            context = {'show_inv_alert': 'True', 'ul': 'c', 'showreg': 'False', 'alert_message': 'Error from exception'}
            return render(request, 'login.html',context, {'error_message': str(e)})
    else:
        context = {'show_inv_alert': 'True', 'ul': 'c', 'showreg': 'False', 'alert_message': 'Post method error'}
        return render(request, 'login.html', {'error_message': 'Form submission method must be POST.'})


def treg(request):
    if request.method == 'POST':
        em = request.POST.get('em')
        pw = request.POST.get('pw')
        fname = request.POST.get('fname')
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            query = f"insert into testers(email,pass,fname,isavailable) values('{em}','{pw}','{fname}',1)"
            cursor.execute(query)
            conn.commit()
            conn.close()
            cursor.close()
            context = {'show_inv_alert': 'True', 'ul': 't', 'showreg': 'False', 'alert_message': 'Please login with your newly registered account!'}
            return render(request, 'login.html', context)
        except Exception as e:
            context = {'show_inv_alert': 'True', 'ul': 't', 'showreg': 'False', 'alert_message': 'Error from exception'}
            return render(request, 'login.html',context, {'error_message': str(e)})
    else:
        context = {'show_inv_alert': 'True', 'ul': 't', 'showreg': 'False', 'alert_message': 'Post method error'}
        return render(request, 'login.html', {'error_message': 'Form submission method must be POST.'})




def user(request):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bugdata")
        data = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Error:", err)
        data = []  # Empty list in case of error
    finally:
        cursor.close()
        conn.close()

    return JsonResponse({'data': data})




def submit_url(request):    
    try:
        url = request.POST.get('urlInput')
        username = request.POST.get('usernameInput')
        password = request.POST.get('passwordInput')
        print(url,username,password)
        ID = request.session.get('ID')
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute(f"select fname from customers where id={ID}")
        row=cursor.fetchall()
        fname=row[0][0]
        print("Name : ",fname)
        if (url != '' or username!= ''or password!=''): 
            cursor.execute(f"INSERT INTO requests(url,username,password,ID,status,assignedto,requested_at,fname) VALUES('{url}','{username}','{password}',{ID},'Under Review',-1,CURRENT_TIMESTAMP,'{fname}')")
            connection.commit()
            context={'show_alert':True,'alert_message':'Request added!'}
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
            cursor.close()
            connection.close()

    
    return redirect('user_home')



def user_home(request):
     conn = mysql.connector.connect(**config)
     cursor = conn.cursor()
     ID = request.session.get('ID')
     query=f"select *from requests where ID={ID} and status != 'Testing Completed'"
     cursor.execute(query)
     rows=cursor.fetchall()
     if rows:
         query=f"select url,requested_at,status,CAST(req_ID AS CHAR) from requests where ID={ID} and status !='Testing Completed'"
         cursor.execute(query)
         rows=cursor.fetchall()
         print(rows)
         query=f"select url,requested_at,status,CAST(req_ID AS CHAR) from requests where ID={ID} and status='Testing Completed'"
         cursor.execute(query)
         prev_reqrows=cursor.fetchall()
         print(prev_reqrows)
         if prev_reqrows:
            context={'show_newrequests':'False','rows':rows,'ID':ID,'show_prevrequests':'True','prev_reqrows':prev_reqrows}
         else:
            context={'show_newrequests':'False','rows':rows,'ID':ID,'show_prevrequests':'False'}
        
     else:
         query=f"select url,requested_at,status,CAST(req_ID AS CHAR) from requests where ID={ID} and status='Testing Completed'"
         cursor.execute(query)
         prev_reqrows=cursor.fetchall()
         print(prev_reqrows)
         if prev_reqrows:
            context={'show_newrequests':'True','rows':rows,'ID':ID,'show_prevrequests':'True','prev_reqrows':prev_reqrows}
         else:
            context={'show_newrequests':'True','rows':rows,'ID':ID,'show_prevrequests':'False'}
     return render(request,'user_page1.html',context)


def testing_requests(request):
    # Sample data for demonstration purposes
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Fetch data from the database for the first query
    query = "SELECT CAST(req_ID AS CHAR), requested_at, url, fname, status FROM requests where assignedto = -1 and status != 'Testing Completed'"
    cursor.execute(query)
    rows = cursor.fetchall()







    # Close cursor and connection
    cursor.close()
    conn.close()

    context = {
        'rows': rows,
    }

    # Render the template with context data
    return render(request, 'testing_requests.html', context)

def reqstatusupdatefunc(request):
    id=int(request.POST.get('req_ID'))
    status=request.POST.get('statusSelect')
    print(f"from reqstatus function id ={id},status={status}")
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    query=f"update requests set status='{status}' where req_id={id}"
    cursor.execute(query)
    conn.commit()
    request.session['alert'] = f'req_id {id} status updated to {status}'
    if(status=='Testing Completed'):
        query=f"select assignedto from requests where req_id={id}"
        cursor.execute(query)
        row=cursor.fetchall()
        tester_id = row[0][0]
        query=f"update testers set isavailable=1 where id={tester_id}"
        cursor.execute(query)
        conn.commit()
    # Render the template with context data
    return redirect(assigned_requests)
       

def assign_tester(request, request_id):
    if request.method == 'POST':

        return redirect('testing_requests')

def assigned_requests(request):
    # Sample data for demonstration purposes
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Fetch data from the database for the first query
    query = "SELECT CAST(req_ID AS CHAR), requested_at, url, fname, status,assignedto,test_status,tester_comment FROM requests where status != 'Under Review'"
    cursor.execute(query)
    rows = cursor.fetchall()

    alert=request.session.get('alert')
    if(alert):
        context={'show_alert1':alert,'rows':rows}
        request.session['alert'] = ''
    else:
        context = {'rows': rows}

    # Render the template with context data
    return render(request, 'assigned_requests.html', context)

    
def avail_testers(request):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    data = json.loads(request.body)
    id = data.get('id')
    # Fetch testers data for the second query
    query_testers = "SELECT id, fname, email FROM testers WHERE isavailable = 1"
    cursor.execute(query_testers)
    testers = cursor.fetchall()

    # Close cursor and connection
    cursor.close()
    conn.close()

    testers_table = '<table>'  # Start the table outside the loop
    for tester in testers:
        testers_table += f'<tr><td>{tester[0]}</td><td>{tester[1]}</td><td>{tester[2]}</td><td>'
        # Generate CSRF token for each form
        csrf_token = csrf.get_token(request)
        # Add the form with the CSRF token inside the loop
        testers_table += f'<form action="/assigntotester/" method="post">'
        testers_table += f'<input type="hidden" name="req_ID" value="{id}">'
        testers_table += f'<input type="hidden" name="tester_ID" value="{tester[0]}">'
        testers_table += f'<input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">'
        testers_table += '<button type="submit">Assign</button></form></td></tr>'
    testers_table += '</table>'  # Close the table after the loop
    return HttpResponse(testers_table)

def assigntotester(request):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        tester_ID=request.POST.get('tester_ID')
        req_ID=request.POST.get('req_ID')
        query=f"update testers set isavailable=0 where id={tester_ID}"
        cursor.execute(query)
        conn.commit()
        query=f"update requests set assignedto={tester_ID},status='Request Accepted' where req_ID={req_ID}"
        cursor.execute(query)
        conn.commit()
        res=f"request ID {req_ID} assigned to tester {tester_ID}"
        query = "SELECT CAST(req_ID AS CHAR), requested_at, url, fname, status FROM requests where status != 'Under Review'"
        cursor.execute(query)
        rows = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        conn.close()

        context={'show_alert':'True','res':res,'rows':rows}
    except Exception as e:
        context={'show_alert':'True','res':e}
    return render(request,'assigned_requests.html',context)


def newTester(request):
    id = int(request.session.get('tester_ID'))
    print('ID ',id)

    rows=[]
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute(f"SELECT url, username,password,CAST(req_ID as CHAR),assignedto,status,fname FROM requests where assignedto = {id} and status != 'Testing Completed' ")
        data = cursor.fetchall()
        cursor.execute(f"SELECT url, username,password,CAST(req_ID as CHAR),assignedto,status,fname FROM requests where assignedto = {id} and status = 'Testing Completed' ")
        rows = cursor.fetchall()
        print(data)
        print(rows)
        req_ID=int(data[0][3])
        cursor.execute(f"select test_status,tester_comment from requests where req_ID={req_ID}")
        row=cursor.fetchall()
        req_status=row[0][0]
        req_status_desc=row[0][1]
        if req_status is None:
            req_status == ''
        if req_status_desc is None:
            req_status_desc==''
    except mysql.connector.Error as err:
        print("Error:", err)
        err+='id is'+id
        return HttpResponse(err)
    finally:
            cursor.close() 
            connection.close()
    return render(request,'newTester.html',{'data':data,'rows':rows,'req_status':req_status,'req_status_desc':req_status_desc})

def bugraise(request):
    print("from bugraise")
    try:
        if request.method=="POST":
            print("inside the bug input ")
            req_ID = int(request.POST.get('req_ID'))
            print(req_ID)
            bugname = request.POST.get('bugName')
            summary = request.POST.get('summary')
            workflow = request.POST.get('workflow')
            severity = request.POST.get('severity')
            steps = request.POST.get('steps')
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()
            cursor.execute("SELECT url, username,password,CAST(req_ID as CHAR) FROM requests")
            data = cursor.fetchall()
            cursor.execute(f"INSERT INTO bugdata (bug_name, description, status,id,workflow, severity, steps) VALUES ('{bugname}', '{summary}', 'Under Triage', '{req_ID}','{workflow}', '{severity}', '{steps}')")
            connection.commit()
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    return redirect(newTester)
def bugs(request):
    try:
        req_id = request.POST.get('req_ID')
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute(f"SELECT status,bug_name,description,workflow,severity,steps,bug_id FROM bugdata where id = {req_id}")
        data = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Error:", err)
        return HttpResponse(err)
    finally:
            cursor.close()
            connection.close()
    return render(request,'bugs.html',{'data':data})


def manager_comment(request):
    try:
        if request.method=="POST":
            print("inside the bgcdgug")
            id = int(request.POST.get('req_ID'))
            test_status = request.POST.get('test_status')
            tester_comment = request.POST.get('comment')
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()
            cursor.execute(f"UPDATE requests SET test_status = '{test_status}', tester_comment = '{tester_comment}' WHERE req_ID = {id}")
            connection.commit()
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    return redirect(newTester)
     

def bug_comments_tester(request):
    id=request.POST.get('bug_id')
    if id is None:
        id = request.session.get('bug_id')
    if id is None:
        return HttpResponse("Bug ID not found")
    st=f"bug id {id}'s bug comments page"
    print(st)
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    query=f"select description,bug_id,status,id from bugdata where bug_id={id}"
    cursor.execute(query)
    bug_data=cursor.fetchall()
    print(bug_data)
    desc=bug_data[0][0]
    bugid= bug_data[0][1]
    status=bug_data[0][2]
    req_id=bug_data[0][3]
    query = f"SELECT status_updation, comment, commented_at FROM bug_comments WHERE bug_id = {id} ORDER BY commented_at DESC"
    cursor.execute(query)
    comments=cursor.fetchall()
    print(comments)
    query=f"select status from requests where req_ID={req_id}"
    cursor.execute(query)
    rows=cursor.fetchall()
    request_status= rows[0][0]

    context={'info':st,'id':id,'desc':desc,'bugid':bugid,'status':status,'comments':comments,'request_status':request_status}
    return render(request,'bugcommentstester.html',context)

def manager_home(request):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute(f"SELECT id , fname , email FROM customers")
        data = cursor.fetchall()
        print(data)
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
            cursor.close()
            connection.close()
    return render(request,'manager_home.html',{'data':data})

def assigned_requests_customer(request):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    custid=int(request.POST.get('custID'))
    # Fetch data from the database for the first query
    query = f"SELECT CAST(req_ID AS CHAR), requested_at, url, fname, status,assignedto,test_status,tester_comment FROM requests where status != 'Under Review' and ID={custid}"
    cursor.execute(query)
    rows = cursor.fetchall()

    alert=request.session.get('alert')
    if(alert):
        context={'show_alert1':alert,'rows':rows}
        request.session['alert'] = ''
    else:
        context = {'rows': rows,'ID':custid}

    # Render the template with context data
    return render(request, 'assigned_requests_customer.html', context)

def customer_requests(request):
    custid = int(request.POST.get('custID'))
    print(custid)
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Fetch data from the database for the first query
    query = f"SELECT CAST(req_ID AS CHAR), requested_at, url, fname, status FROM requests where assignedto = -1 and status != 'Testing Completed' and ID = {custid} "
    cursor.execute(query)
    rows = cursor.fetchall()







    # Close cursor and connection
    cursor.close()
    conn.close()

    context = {
        'rows': rows,
        'ID':custid
    }

    # Render the template with context data
    return render(request, 'customer_requests.html', context)




     
    