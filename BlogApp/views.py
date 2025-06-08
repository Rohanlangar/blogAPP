from django.http import JsonResponse,response
from supabase import create_client
from supabase.lib.client_options import ClientOptions
from django.shortcuts import render,redirect

SUPABASE_URL = "https://bkufkdfdbwzfgbbqhpjf.supabase.co"  # replace with yours
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJrdWZrZGZkYnd6ZmdiYnFocGpmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg5NjQ4MDAsImV4cCI6MjA2NDU0MDgwMH0.L3NyWrFxR4Xju76fsegEk3nq-eeI_ysb6-nvzCW_HKM"  # replace with your key

supabase = create_client(SUPABASE_URL, SUPABASE_KEY, options=ClientOptions(schema="public"))
supabase_auth = create_client(SUPABASE_URL, SUPABASE_KEY, options=ClientOptions(schema="auth"))


def add_blog_post(request):
    if request.method=='POST':
        userid=request.session.get('userid')
        title=request.POST.get('title')
        content=request.POST.get('content')
        tags=request.POST.get('tags')
    
        username=request.session.get('username')

        data={
            'title':title,
            'content':content,
            'user_id':userid,
            'username':username,
            'tags':tags
        }
        try:
            response = supabase.table("blogs").insert(data).execute()
            return redirect('home')
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
        
    return render(request,'blog.html')

def home(request):
    response = supabase.table('blogs').select('title', 'content', 'created_at', 'username', 'Likes', 'id', 'tags').execute()
    blogs = response.data
    for blog in blogs:
        tags_str = blog.get('tags', '')
        blog['tags'] = [tag.strip() for tag in tags_str.split(',')] if tags_str else []

    return render(request, 'home.html', {'response': blogs})


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
          user=supabase.auth.get_user()
          username=user.user.user_metadata.get('display_name')
          request.session['username']=username
          return redirect('home')
          
     return render(request,'signin.html')

def likecount(request,blog_id):
    if request.method=="POST":

        response=supabase.table('blogs').select('Likes').eq('id',blog_id).single().execute()

        if response:
            likecount=response.data.get('Likes')
        else:
            likecount= 0
        supabase.table('blogs').update({'Likes':likecount+1}).eq('id',blog_id).execute()
        return redirect('home')
     
def logout(request):
    supabase.auth.sign_out()
    request.session.flush()
    return redirect('signin')

def show_post(request,blog_id):
    if request.method=='POST':
        response=supabase.table('blogs').select('title','content','created_at','username','Likes','id','tags').eq('id',blog_id).execute()
        blogs=response.data
        for blog in blogs:
            tags_str = blog.get('tags', '')
            blog['tags'] = [tag.strip() for tag in tags_str.split(',')] if tags_str else []

        commentsobject=supabase.table('comments').select('comment','user').eq('blog_id',blog_id).execute()
        return render(request,'comments.html',{'response':blogs,'comments':commentsobject.data,'blog_id':blog_id})
    if request.method=='GET':
        response=supabase.table('blogs').select('title','content','created_at','username','Likes','id','tags').eq('id',blog_id).execute()
        blogs=response.data
        for blog in blogs:
            tags_str = blog.get('tags', '')
            blog['tags'] = [tag.strip() for tag in tags_str.split(',')] if tags_str else []

        commentsobject=supabase.table('comments').select('comment','user').eq('blog_id',blog_id).execute()
        return render(request,'comments.html',{'response':blogs,'comments':commentsobject.data,'blog_id':blog_id})

def add_comment(request,blog_id):
    comment=request.POST.get('comment')
    username=request.session.get('username')
    data={
        'blog_id':blog_id,
        'comment':comment,
        'user':username
    }
    supabase.table('comments').insert(data).execute()
    return redirect('show_post',blog_id)

def profile(request):
    user=supabase.auth.get_user()
    email=user.user.email
    username=request.session.get('username')
    print(username)
    userid=request.session.get('userid')
    info={
        'email':email,
        'username':username
    }

    response=supabase.table('blogs').select('title','content','created_at','Likes','id','tags').eq('user_id',userid).execute()
    blogs=response.data
    for blog in blogs:
        tags_str = blog.get('tags', '')
        blog['tags'] = [tag.strip() for tag in tags_str.split(',')] if tags_str else []
    return render(request,'profile.html',{'info':info,'blogs':blogs})


def bookmark(request,blog_id):
    response=supabase.table('blogs').select('*').eq('id',blog_id).execute()
    responsedata=response.data[0]
    userid=request.session.get('userid')
    data={
        'id':blog_id,
        'user_id':userid,
        'title':responsedata['title'],
        'content':responsedata['content'],
        'created_at':responsedata['created_at'],
        'username':responsedata['username'],
        'Likes':responsedata['Likes'],
        'tags':responsedata['tags']
    }
    supabase.table('bookmark_blogs').insert(data).execute()
    return redirect('show_bookmarks')

def show_bookmarks(request):
    userid=request.session.get('userid')
    response=supabase.table('bookmark_blogs').select('title','content','created_at','Likes','id','tags').eq('user_id',userid).execute()
    blogs=response.data
    for blog in blogs:
        tags_str = blog.get('tags', '')
        blog['tags'] = [tag.strip() for tag in tags_str.split(',')] if tags_str else []
    return render(request,'bookmark.html',{'response':blogs})

def remove_bookmark(request,blog_id):
    supabase.table('bookmark_blogs').delete().eq('id',blog_id).execute()
    return redirect('show_bookmarks')


     
          
          
    
        

