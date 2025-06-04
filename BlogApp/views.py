from django.http import JsonResponse,response
from supabase import create_client
from supabase.lib.client_options import ClientOptions
from django.shortcuts import render

SUPABASE_URL = "https://bkufkdfdbwzfgbbqhpjf.supabase.co"  # replace with yours
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJrdWZrZGZkYnd6ZmdiYnFocGpmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg5NjQ4MDAsImV4cCI6MjA2NDU0MDgwMH0.L3NyWrFxR4Xju76fsegEk3nq-eeI_ysb6-nvzCW_HKM"  # replace with your key

supabase = create_client(SUPABASE_URL, SUPABASE_KEY, options=ClientOptions(schema="public"))

def add_blog_post(request):
    if request.method=='POST':
        title=request.POST.get('title')
        content=request.POST.get('content')
        data={
            'title':title,
            'content':content
        }
        try:
            response = supabase.table("blogs").insert(data).execute()
            return JsonResponse({"success": True, "data": response.data})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
        
    return render(request,'blog.html')

def home(request):
        response=supabase.table('blogs').select('title','content').execute()
        data=response.data
        return render(request,'home.html',{'response':data})
    
        

