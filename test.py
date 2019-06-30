import requests


def test_get():
    for i in range(100):
        r = requests.get(f"http://httpbin.org/range/{i}")
        print(r.status_code)
        print(r.text)
    print("done")

test_get()