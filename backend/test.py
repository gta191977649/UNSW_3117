import math
import numpy as np

good_6 = [55.33,127.05,106.36,43.93,43.93,43.93,43.93,44.23,44.08,30.21,29.86,31.15,30.49,25.00,27.74,28.54,26.60,19.99,26.38,26.06,21.25,19.62,24.20,24.02,20.34,17.70,22.09,21.86,19.30,18.41,15.31,14.79,14.72,14.71,23.93,43.05,43.34,43.20,41.81,18.31,14.14,14.10,14.12,14.14,14.15,18.33,19.04,19.53,19.87,26.60,43.05,41.67,20.67,19.39,26.11,31.61,32.32,41.81,20.08,19.87,42.35,41.81,41.67,20.28,19.84,19.81,19.93,20.63,41.81,41.54,41.81,41.41,20.63,20.44,20.18,20.24,20.40,21.28,39.16,38.35,38.69,42.49,42.63,42.49,40.75,21.46,18.13,22.09,15.62,14.76,24.95,18.20,14.54,42.63,42.49,42.91,17.32,43.49,43.49,31.76,18.57,43.34,43.63,16.93,15.02,43.20,39.51,15.09,22.67,35.32,40.88,43.34,40.50,19.10,18.31,20.15,43.20,43.34,43.05,37.46,22.35,22.71,41.27,40.88,41.41,41.27,39.51,27.16,22.51,22.09,39.04,40.63,40.88,39.63,30.71,27.33,27.56,37.90,43.34,43.63,43.49,43.78,43.78,43.78,16.53,16.16,16.43,21.75,43.63,43.78,43.93]
alpha = 10
def inv(arr):
    L = len(arr)
    new_arr = []
    for i in range(L):
        if(arr[i] > 50):
            tmp = 43.34
        else:
            tmp = arr[i]
        tmp = 43.34 - tmp
        #new_arr.append(-(tmp-14.14) + (44.23-14.14))
        new_arr.append(tmp)

    return new_arr
    
def up_sinc(x):
    p = math.pi
    if(x < 0.0001 and x > -0.0001):
        y = 1
    else:
        y = math.sin(p*x)/(p*x)
    return y

def up_sampling(arr, up_rate):
    L = len(arr)
    new_L = math.floor(up_rate*L)
    up_arr = []
    for i in range(new_L):
        up_arr.append(0)

    i = 0
    for i in range(new_L):
        #temp = 0.0
        for n in range(L):
            up_arr[i] = up_arr[i] + arr[n]*up_sinc(((i)/up_rate) - (n))
            #temp = temp + arr[n]*up_sinc(i/up_rate - n)
        #print(up_arr)
        #up_arr.append(temp)

    return up_arr

def my_diff(arr,t,delta):
    L = len(arr)
    if(t + delta > L-1):
        y = 0
    else:
        y = (arr[t + delta]-arr[t])/delta
    return y

def rieman_sum(arr,delta):
    L = len(arr)
    out = []
    for i in range(L-1):
        mid = math.floor(delta/2)
        temp = 0
        for j in range(i):
            f_mid = arr[i+mid+1-j]
            temp = temp + f_mid*delta
        out.append(temp)
    return out

def shimmer(arr,start,finish):
    N = finish-start+1
    numera = 0
    epsilon = 0.01
    denom = arr[finish]
    for i in range(start,finish-1):
        numera = abs(arr[i+1]-arr[i]) + numera
        denom = (arr[i]) + denom
    numera = numera/(N-1)
    denom = denom/N
    if(denom < epsilon):
        denom = 1
    out = numera*100/denom
    return out

def two_mean(x,y):
    return (x+y)/2

def find_state(x,m):
    weak = 2
    strong = m
    gap = (strong-weak)/4
    mid_strong = strong-gap
    mid = mid_strong - gap
    mid_weak = weak + gap
    out = 1
    if(x >= two_mean(strong,mid_strong)):
       out = 5
    if((x >= two_mean(mid_strong,mid)) & (x < two_mean(strong,mid_strong))):
       out = 4
    if((x <= two_mean(mid_strong,mid)) & (x > two_mean(mid,mid_weak))):
       out = 3
    if((x <= two_mean(mid,mid_weak)) & (x > two_mean(weak,mid_weak))):
       out = 2

    return out

def init_5_states():
    arr = []
    for i in range(5):
        arr.append(0)

    return arr

def five_states(arr):
    L = len(arr)
    out = [0,0,0,0,0]
    m = max(arr)
    out[find_state(arr[0],m)-1] = 1
    for i in range(L-1):
        if(find_state(arr[i+1],m) - find_state(arr[i],m) != 0):
            index = find_state(arr[i+1],m) - 1
            out[index] = out[index] + 1
    return out

def mid_zeros(arr,top,bottom):
    mid = (top+bottom)/2
    epsilon = 0.001
    L = len(arr)
    num_zeros = 0
    all_zeros = []
    pivot = mid + epsilon
    #print(mid,top,bottom)
    for i in range(L-1):
        if(arr[i+1] > pivot and arr[i] < pivot):
            num_zeros = num_zeros + 1
            all_zeros.append(i)
        if(arr[i+1] < pivot and arr[i] > pivot):
            num_zeros = num_zeros + 1
            all_zeros.append(i)
    return [num_zeros,all_zeros]

def most_zeros(arr):
    state1 = 1
    state2 = 1
    last_nums = [0,0,0]
    top = max(arr)
    but = min(arr)
    while(True):
        mid = two_mean(top,but)
        [num0,zeros0] = mid_zeros(arr,top,but)
        [num_up,zeros_up] = mid_zeros(arr,top,mid)
        [num_bot,zeros_bot] = mid_zeros(arr,mid,but)
        state1 = (num0 >= num_up) and (num0 >= num_bot)  #mid is better
        state2 = max(last_nums) >= max([num0,num_up,num_bot]) #last is better
        last_nums = [num0,num_up,num_bot]
        last_zeros = [zeros0,zeros_up,zeros_bot]
        if(state2 or state1):
            return [last_nums[np.argmax(last_nums)],last_zeros[np.argmax(last_nums)]]
        if(num_up > num_bot):
            but = mid
        else:
            top = mid

def find_freq(arr,up_rate):
    [num_zeros,zero_arr] = most_zeros(arr)
    L = int(num_zeros)
    estimate_time = 0
    if(L == 1):
        return -1
    for i in range(L-1):
        estimate_time = estimate_time + (zero_arr[i+1] - zero_arr[i])
    estimate_time = estimate_time/(2*(L-1)*up_rate)
    return 1/estimate_time

def main0():
    good = inv(good_6)
    L = len(good)
    alpha = 10
    up_good = up_sampling(good,alpha)
    size = math.floor(alpha*L)
    diff = []
    delta = 20
    for i in range(size):
        diff.append(my_diff(up_good,i,delta))
    rie = rieman_sum(diff,1)
    max_rie = max(rie)
    max_sig = max(good)
    len_rie = len(rie)
    pow_coe = 2
    new_rie = []
    for i in range(len_rie):
        temp = (math.pow(rie[i],pow_coe)*max_sig)/math.pow(max_rie,pow_coe)
        new_rie.append(temp)
    
    states = []
    for i in range(len_rie):
        find_a_state = find_state(rie[i],max_rie)
        states.append(find_a_state)
    
    #five_states = []
    #five_states.append(states[0])
    time_segment = 200
    shim_size = math.floor(len_rie / time_segment)
    f_state = five_states(rie)
    #print(f_state)
    #[n1,n2] = mid_zeros(rie,,min(rie))
    #print(n1,"\n",n2)
    [n,arr] = most_zeros(rie)
    print(n,len(arr))
    print(find_freq(arr,alpha))

def diff_sig(up_sig,delta,size):
    diff = []
    for i in range(size):
        diff.append(my_diff(up_sig,i,delta))
    return diff

def gen_process_sig(temp_process_sig,pow_coe,max_sig):
    max_psig = max(temp_process_sig)
    len_process_sig = len(temp_process_sig)
    max_temp = 35
    new_rie = []
    for i in range(len_process_sig):
        if(max_psig < 0.001):
            max_psig = 1
        temp = (math.pow(temp_process_sig[i],pow_coe)*max_temp)/math.pow(max_psig,pow_coe)
        new_rie.append(temp)
    return new_rie

def my_mean(arr,start,end):
    L = len(arr)
    out = 0
    for i in range(int(start),int(end)):
        out = arr[i] + out
    out = out/(end-start)
    return out

def mean_window(arr,leng):
    if(leng % 2 == 0):
        leng = leng - 1
    L = len(arr)
    out = []
    for i in range(L):
        mid = (leng-1)/2
        temp = 0
        if(i < mid):
            #tmp_arr = arr[0:i+mid-1-1]
            temp = my_mean(arr,0,i+mid-1-1)
        if(i >= mid and i < (L-mid-1)):
            #temp = my_mean(arr[i-mid:i+mid-1])
            temp = my_mean(arr,i-mid,i+mid-1)
        if(i >= L-mid-1):
            #temp = my_mean(arr[i-mid:L-1])
            temp = my_mean(arr,i-mid,L-1)
        out.append(temp)

    return out

def main1(sig):
    temp_sig = inv(sig)
    L = len(temp_sig)
    alpha = 10
    up_sig = up_sampling(temp_sig,alpha)
    size = math.floor(alpha*L)
    delta = 20
    diff = diff_sig(up_sig,delta,size)
    temp_process_sig = rieman_sum(diff,1)
    pow_coe = 2
    new_rie = gen_process_sig(temp_process_sig,pow_coe,max(sig))
    #print(temp_process_sig)
    #m_slide = mean_window(new_rie,10)
    #len_rie = len(new_rie)
    time_seg = 7
    #print(new_rie,"temp_up",up_sig)
    #print("rie\n",new_rie,"temp\n",temp_process_sig,"up\n",up_sig,"temp_sig\n",temp_sig)
    #shim = shimmer(sig,len_rie-time_seg*alpha-100,len_rie-100)
    shim = shimmer(sig, len(sig)-1-time_seg,len(sig)-1)
    start = len(new_rie)-1-20*alpha
    end = len(new_rie)-1
    #print(new_rie[start:end])
    freq = find_freq(new_rie[start:end],alpha)
    all_states = five_states(new_rie[start:end])

    steep = (1/2)*((sig[L-1]-sig[L-2]) + (sig[L-2]-sig[L-3]))
    return [shim,freq,all_states,steep]

sig_ = []
max_siglen = 200
threshold = 15

def update_sig(x):
    L = len(sig_)
    if(L < max_siglen):
        sig_.append(x)
    if(L == max_siglen):
        for i in range(max_siglen-1):
            sig_[i] = sig_[i+1]
        sig_[max_siglen-1] = x

def is_sleep_apnea():
    if(len(sig_) > threshold+2):
        [shim,freq,all_states,steep] = main1(sig_)
        return [shim,freq,all_states,steep]
        #print(shim)
        #print("sleep apnea",test)
    return 0
    #print("no sleep apnea",len(sig))

'''
def main2():
    test = []
    
    len = 140
    for i in range(len):
        test.append(44)
    
    test = inv(good_6)
    [num,zeros] = most_zeros(test)
    print(num,"\n",zeros)
    #up_test = up_sampling(test,10)
    #mean_out = mean_window(up_test,1)
    #print(up_test)
'''