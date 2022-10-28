
# useage

1. python version > 3.8 because the protoletarial bump python lower bound to 3.8 ([0480117](https://github.com/cpcloud/protoletariat/commit/04801176b74747199adcfe101f65c7c880662f07))

2. ./pleasew tools && ./pleasew proto && ./pleasew protol



# run example
1. run server
> PYTHONPATH=$(pwd) python cmd/{grpc|twirp}/server/main.py
2. run client
> PYTHONPATH=$(pwd) python cmd/{grpc|twirp}/client/main.py


# todo
use python_wheel instead of sh_cmd(which protol)

```plz
sh_cmd(
    name = "protoletariat",
    cmd = [
        "$(which protol) \\\\$@"
    ],
)
```