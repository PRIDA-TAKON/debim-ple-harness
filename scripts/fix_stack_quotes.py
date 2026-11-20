p = "/opt/benchmark/ple/kit/stack.py"
with open(p, "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace("*LOG_OPTS, --add-host, host.docker.internal:host-gateway,", '*LOG_OPTS, "--add-host", "host.docker.internal:host-gateway",')

with open(p, "w", encoding="utf-8") as f:
    f.write(c)

print("FIXED_STACK_QUOTES_SUCCESS")
