package(default_visibility = ["PUBLIC"])


sh_cmd(
    # https://github.com/cpcloud/protoletariat
    name = "install-deps",
    cmd = [
        "set -eux; rootPath=\\\\$(pwd) && cd tools && pip3 install --upgrade pip && pwd && pip3 install -r requirements.txt",
        "cd \\\\$rootPath && $(out_exe ///pleasings2//tools/proto:buf) -v generate buf.build/envoyproxy/protoc-gen-validate"
    ],
    deps = [
        "///pleasings2//tools/proto:buf",
    ]
)


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
        f"$(out_exe :protoletariat) --create-package --in-place --python-out api/gen/pb --exclude-google-imports --exclude-imports-glob 'google/*' buf --buf-path=$(out_exe ///pleasings2//tools/proto:buf)",
    ],
    deps = [
        ":protoletariat",
        "///pleasings2//tools/proto:buf"
    ]
)

sh_cmd(
    name = "protoletariat",
    cmd = [
        "$(which protol) \\\\$@"
    ],
)

# remote_file(
#     name = "protoletariat",
#     binary = True,
#     exported_files = ["protoletariat"],
#     extract = False,
#     url = f"file:///opt/homebrew/bin/protol",
# )

# python_wheel(
#     name = "protoletariat",
#     package_name = "protoletariat",
#     version = "1.0.1-py3-none-any",
#     # entry_points = {"protoletariat": "protoletariat.__main__:main"}
# )