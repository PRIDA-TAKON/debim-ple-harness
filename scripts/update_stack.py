p = "/opt/benchmark/ple/kit/stack.py"
with open(p, "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace('"NO_PROXY": "",', '"NO_PROXY": "127.0.0.1,localhost,host.docker.internal,egress",')
c = c.replace('"no_proxy": "",', '"no_proxy": "127.0.0.1,localhost,host.docker.internal,egress",')

with open(p, "w", encoding="utf-8") as f:
    f.write(c)

print("SUCCESSFULLY_UPDATED_STACK_PY")
