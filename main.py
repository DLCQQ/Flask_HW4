from flask import Flask, request, render_template
import requests
import os
import threading
import time
import multiprocessing
import asyncio

app = Flask(__name__)

def download_image(url, filename, start_time):
    
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)
    print(f"Изображение {filename} загружено за {time.time() - start_time:.2f} секунд.")

async def download_image_async(url, filename, start_time):
    
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)
    print(f"Изображение {filename} загружено за {time.time() - start_time:.2f} секунд.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    start_time = time.time()
    urls = request.form.getlist('url')

    # Подход с использованием многопоточности
    threads = []
    for url in urls:
        filename = os.path.basename(url)
        thread = threading.Thread(target=download_image, args=(url, filename, start_time))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Многопоточность - Общее время: {time.time() - start_time:.2f} секунд.")

    # Подход с использованием многопроцессорности
    start_time = time.time()
    processes = []
    for url in urls:
        filename = os.path.basename(url)
        process = multiprocessing.Process(target=download_image, args=(url, filename, start_time))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print(f"Многопроцессорность - Общее время: {time.time() - start_time:.2f} секунд.")

    # Асинхронный подход
    async def download_images_async():
        tasks = []
        for url in urls:
            filename = os.path.basename(url)
            task = asyncio.create_task(download_image_async(url, filename, start_time))
            tasks.append(task)
        await asyncio.gather(*tasks)

    asyncio.run(download_images_async())

    print(f"Асинхронность - Общее время: {time.time() - start_time:.2f} секунд.")

    return "Изображения успешно загружены!"

if __name__ == '__main__':
    app.run(debug=True)