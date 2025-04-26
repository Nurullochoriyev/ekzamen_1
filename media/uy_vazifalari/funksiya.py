import time
def data_count(data):
    def qweer(*args,**kwargs):
        boshlangan_vaqt=time.time()
        print(f"boshlangan vaqt{boshlangan_vaqt}")
        natija=data(*args,**kwargs)
        tugagan_vaqt=time.time()
        print(f"tugagan vaqt {tugagan_vaqt}")
        utgan_vaqt=tugagan_vaqt-boshlangan_vaqt
        print(f"sarflangan vaqt {utgan_vaqt:.5f}")
        print(f"natija {natija}")
        return natija
    return qweer

@data_count
def add(a):
    b=0
    for i in range(a):
        b+=i
    return b+2
add(a=35478587)