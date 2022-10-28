//go:build tools
// +build tools

package tools

// see https://github.com/golang/go/wiki/Modules#how-can-i-track-tool-dependencies-for-a-module
import (
	_ "github.com/envoyproxy/protoc-gen-validate"
	_ "github.com/verloop/twirpy/protoc-gen-twirpy"
)

//go:generate go install github.com/envoyproxy/protoc-gen-validate
//go:generate go install github.com/verloop/twirpy/protoc-gen-twirpy
