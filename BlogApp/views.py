from django.http import JsonResponse,response
from supabase import create_client
from supabase.lib.client_options import ClientOptions
from django.shortcuts import render

SUPABASE_URL = "https://bkufkdfdbwzfgbbqhpjf.supabase.co"  # replace with yours
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJrdWZrZGZkYnd6ZmdiYnFocGpmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg5NjQ4MDAsImV4cCI6MjA2NDU0MDgwMH0.L3NyWrFxR4Xju76fsegEk3nq-eeI_ysb6-nvzCW_HKM"  # replace with your key

supabase = create_client(SUPABASE_URL, SUPABASE_KEY, options=ClientOptions(schema="public"))
supabase_auth = create_client(SUPABASE_URL, SUPABASE_KEY, options=ClientOptions(schema="auth"))

def add_blog_post(request):
    if request.method=='POST':
        userid=request.session.get('userid')
        title=request.POST.get('title')
        content=request.POST.get('content')

        user=supabase.auth.get_user()
        username=user.user.user_metadata.get('display_name')
        request.session['username']=username

        username=request.session.get('username')

        data={
            'title':title,
            'content':content,
            'user_id':userid,
            'username':username
        }
        try:
            response = supabase.table("blogs").insert(data).execute()
            return JsonResponse({"success": True, "data": response.data})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
        
    return render(request,'blog.html')

# def home(request):
#         response=supabase.table('blogs').select('title','content','created_at').execute()
#         data=response.data
#         return render(request,'home.html',{'response':data})

def signup(request):
     if request.method=='POST':
          email=request.POST.get('email')
          password=request.POST.get('password')
          username=request.POST.get('username')
          response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

          user = response.user
          user_id = user.id

          supabase.auth.update_user({
            "data": {
                "display_name": username
            }
        })
          return render(request,'signin.html')
     
     return render(request,'signup.html')

def signin(request):
     if request.method=='POST':
          email=request.POST.get('email')
          password=request.POST.get('password')
          response=supabase.auth.sign_in_with_password({'email':email,'password':password})
          request.session['userid']=response.user.id
          response=supabase.table('blogs').select('title','content','created_at','username').execute()
          data=response.data
          
          return render(request,'home.html',{'response':data})
     return render(request,'signin.html')
          
          
    
        

