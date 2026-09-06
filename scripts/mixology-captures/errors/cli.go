// This probe runs the injected Internal example through the real CLI exit adapter.
package main

import (
	"github.com/TheFellow/go-modular-monolith/deckcapture"
	"github.com/TheFellow/go-modular-monolith/pkg/errors"
	"github.com/urfave/cli/v3"
)

func main() { cli.HandleExitCoder(errors.ToCLIExit(deckcapture.InternalFailure())) }
