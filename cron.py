import requests,bs4,os,asyncio,sys
from telethon import TelegramClient
from telethon.sessions import StringSession


session = os.environ.get("SESSION")
api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")

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
ig_username = sys.argv[1]
channel_username = sys.argv[2]
async def main():
    x = requests.get(ig+'/u/'+ig_username)
    soup = bs4.BeautifulSoup(x.text)
    post = soup.select('a[class="sized-link"]')[0].get('href')
    print(post)
    with open('post.txt') as myfile:
        if not post in myfile.read():
            print("new post!")
            x = requests.get(ig+post)
            soup = bs4.BeautifulSoup(x.text)
            images = soup.findAll('section',{"class":"images-gallery"})[0].decode_contents()
            soup = bs4.BeautifulSoup(images)
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
                    elif image.name == "img":
                        filename = str(i)+".jpeg"
                        download_file(ig+image.get('src'),filename)
                        async with TelegramClient(StringSession(session), api_id, api_hash) as client:
                            await client.send_file(channel_username, filename, caption="@"+channel_username)
                            os.remove(filename)
                i+=1
    if 'succcexe' in channel_username:
        f = open("post.txt", "w")
        f.write(post)
        f.close()       
                
asyncio.run(main())


