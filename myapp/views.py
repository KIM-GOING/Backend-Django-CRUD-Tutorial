from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

nextnum = 4
topic = [
    {'id': 1, 'title': 'routing', 'content': 'Routing is ...'},
    {'id': 2, 'title': 'views', 'content': 'Views is ...'},
    {'id': 3, 'title': 'model', 'content': 'Model is ...'}
]

def HTMLTemplate(title, content, id=None) :
    global topic
    contextUI = ''    
    if id != None:
        contextUI =f'''
            <li>
                <form action="/delete/" method="post">
                    <input type="hidden" name="id" value={id}>
                    <input type="submit" value="delete">
                </form>
            </li>
            <li><a href="/update/{id}/">update</a></li>
        '''

    ol = ''
    for i in topic:
        ol += f'<li><a href="/read/{i["id"]}/">{i["title"]}</a></li>'

    return f'''
    <html>
    <body>
        <h1><a href="/">Django Tutorial</a></h1>
        <ol>
            {ol}
        </ol>
        <h2>{title}</h2>
        <div>{content}</div>
        <ul>
            <li><a href="/create/">create</a></li>
            {contextUI}
        </ul>
    </body>
    </html>
    '''

def index(request) :
    return HttpResponse(HTMLTemplate('Welcome', 'Hello, Django'))

@csrf_exempt
def create(request) :
    global nextnum
    if request.method == 'GET':
        t = '''
        <form action="/create/" method="post">
        <input type="text" name="title" placeholder="title"></input>
        '''
        c = '''
        <p><textarea name="content" placeholder="content"></textarea></p>
        <p><input type="submit"></p>
        </form>
        '''
        return HttpResponse(HTMLTemplate(t, c))

    elif  request.method =="POST":
        t = request.POST["title"]
        c = request.POST["content"]
        newTopic = {'id': nextnum, 'title': t, 'content': c}
        topic.append(newTopic)
        nextnum += 1
        url = '/read/' + str(nextnum-1)
        return redirect(url)

@csrf_exempt
def delete(request):
    global topic
    global nextnum
    if request.method == "POST":
        id = request.POST["id"]
        del topic[int(id)-1]
        #newTopic = []
        #for i in topic:
        #    if i['id'] != int(id):
        #        newTopic.append(i)
        #topic = newTopic
        nextnum -= 1
    return redirect('/')

@csrf_exempt
def update(request, id):
    global topic
    if request.method == "GET":
        for i in topic:
            if i["id"] == int(id):
                selectedTopic = {
                    'title': i["title"],
                    'content': i["content"]
                }
        t = f'''
        <form action="/update/{id}/" method="post">
        <input type="text" name="title" placeholder="title" value={selectedTopic["title"]}></input>
        '''
        c = f'''
        <p><textarea name="content" placeholder="content">{selectedTopic["content"]}</textarea></p>
        <p><input type="submit"></p>
        </form>
        '''
        return HttpResponse(HTMLTemplate(t , c))

    elif request.method == "POST":
        t = request.POST["title"]
        c = request.POST["content"]
        topic[int(id)-1]["title"] = t
        topic[int(id)-1]["content"] = c
        return redirect(f"/read/{id}")

def read(request, id) :
    t = topic[int(id)-1]["title"]
    c = topic[int(id)-1]["content"]
    return HttpResponse(HTMLTemplate(t , c, id))