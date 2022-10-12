
sh_cmd(
    name = "proto",
    cmd = [
        "$(out_exe ///pleasings2//tools/proto:buf) generate",
    ],
    deps = [
        "///pleasings2//tools/proto:buf",
    ]
)

sh_cmd(
    name = "protol",
    cmd = [
        f"$(out_exe :proto) && $(out_exe :protoletariat) --create-package --in-place --python-out api/gen/pb --exclude-google-imports --exclude-imports-glob 'google/*' buf",
    ],
    deps = [
        ":proto",
        ":protoletariat"
    ]
)

sh_cmd(
    name = "plz-tools",
    cmd = [
        "set -eux; cd tools && pip install --upgrade pip && pwd && pip install -r requirements.txt && go get -u github.com/verloop/twirpy/protoc-gen-twirpy"
    ]
)

remote_file(
    name = "protoletariat",
    binary = True,
    exported_files = ["protoletariat"],
    extract = False,
    url = f"file:////usr/local/bin/protol",
)