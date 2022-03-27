import requests,bs4,os,asyncio,sys
from telethon import TelegramClient
from telethon.sessions import StringSession


session = sys.argv[1]
api_id = sys.argv[2]
api_hash = sys.argv[3]

def download_file(url, local_filename):
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return local_filename


ig = "https://ig.tokhmi.xyz"
ig_username = "succc.exe"
channel_username = "succcexe"
async def main():
    x = requests.get(ig+'/u/'+ig_username)
    soup = bs4.BeautifulSoup(x.text,features="lxml")
    post = soup.select('a[class="sized-link"]')[0].get('href')
    print(post)
    with open('post.txt') as myfile:
        if not post in myfile.read():
            print("new post!")
            x = requests.get(ig+post)
            soup = bs4.BeautifulSoup(x.text,features="lxml")
            images = soup.findAll('section',{"class":"images-gallery"})[0].decode_contents()
            soup = bs4.BeautifulSoup(images,features="lxml")
            imageArray = soup.find_all()
            i=1
            for image in imageArray:
                if image.get('src'):
                    if image.name == "video":
                        filename = str(i)+".mp4"
                        download_file(ig+image.get('src'),filename)
                        async with TelegramClient(StringSession(session), api_id, api_hash) as client:
                            await client.send_file(channel_username, filename, caption="@"+channel_username)
                            os.remove(filename)
                    elif image.name == "image":
                        filename = str(i)+".jpeg"
                        download_file(ig+image.get('src'),filename)
                        async with TelegramClient(StringSession(session), api_id, api_hash) as client:
                            await client.send_file(channel_username, filename, caption="@"+channel_username)
                            os.remove(filename)
                i+=1
    f = open("post.txt", "w")
    f.write(post)
    f.close()       
                
asyncio.run(main())


