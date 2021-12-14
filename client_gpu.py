import time, requests, threading

text_file = open("sample.txt", "w")

def html_post(thread_time):
    thread_time.start = time.time()
    for i in range(NUM_REQUESTS):
        files = {'image': open('test.png', 'rb')}
        res = requests.post(url, files=files)
        # ********* For Debug purpose only ********* # 
        print(f"res->{res}")
        # res_test = requests.get(url)
        # print(f"res_test->{res_test}")
        # ********* For Debug purpose only ********* # 
    thread_time.end = time.time()
    thread_time.total = thread_time.end - thread_time.start
    target_string = f"{thread_time.total} seconds from thread {threading.current_thread().ident}.\n"
    print(target_string)
    with threading.Lock():
        text_file.write(target_string)

threads_lst = []
NUM_THREADS = 100
NUM_REQUESTS = 4000
# url = 'http://6d236c86-us-east.lb.appdomain.cloud:5000/inference'
# url = 'http://172.21.1.77:5000/inference'
# url = 'http://10.27.25.193:5000/inference'
url = 'http://10.32.35.163:5000/inference'
# files = {'image': open('test.png', 'rb')}
thread_time = threading.local()

for i in range(NUM_THREADS):
    t = threading.Thread(target=html_post, args=(thread_time,))
    t.start()
    threads_lst.append(t)

for t_ind in threads_lst:
    t_ind.join()

text_file.close()

# import time, requests, threading

# threads_lst = []
# NUM_REQUESTS = 10
# url = 'http://6d236c86-us-east.lb.appdomain.cloud:5000/inference'
# files = {'image': open('test.png', 'rb')}

# def html_post():
#     start_time = time.time()
#     res = requests.post(url, files=files)
#     end_time = time.time()
#     #elapsed_time = threading.local()
#     elapsed_time = end_time - start_time
#     print(f"{elapsed_time} seconds from thread {threading.current_thread().ident}.")

# for i in range(NUM_REQUESTS):
#     elapsed_time = threading.local()
#     t = threading.Thread(target=html_post, name='html_post_threads')
#     t.start()
#     threads_lst.append(t)

# # Wait all threads to finish.
# for t_ind in threads_lst:
#     t_ind.join()



