package main

import (
	"context"
	"io"
	"log/slog"
	"os"
	"path/filepath"
	"testing"

	"github.com/TheFellow/go-modular-monolith/app"
	"github.com/TheFellow/go-modular-monolith/deckcapture"
	"github.com/TheFellow/go-modular-monolith/main/tui/routes"
	"github.com/TheFellow/go-modular-monolith/pkg/authn"
	"github.com/TheFellow/go-modular-monolith/pkg/errors"
	pkglog "github.com/TheFellow/go-modular-monolith/pkg/log"
	"github.com/TheFellow/go-modular-monolith/pkg/store"
	"github.com/TheFellow/go-modular-monolith/pkg/testutil"
	"github.com/TheFellow/go-modular-monolith/pkg/testutil/tuitest"
	"github.com/charmbracelet/lipgloss"
	"github.com/muesli/termenv"
	"github.com/urfave/cli/v3"
)

func TestDeckCaptureErrors(t *testing.T) {
	lipgloss.SetColorProfile(termenv.TrueColor)
	lipgloss.SetHasDarkBackground(true)
	ctx := authn.ToContext(context.Background(), authn.Owner())
	ctx = pkglog.ToContext(ctx, slog.New(slog.NewTextHandler(io.Discard, nil)))
	database, err := store.Open(ctx, os.Getenv("MIXOLOGY_DB"))
	testutil.Ok(t, err)
	application := app.New(ctx, app.Config{Store: database})
	t.Cleanup(func() { testutil.Ok(t, application.Close()) })
	session := app.NewSession(ctx, application)
	driver := tuitest.NewDriver(t, NewApp(session))
	driver.Resize(120, 34)
	driver.Press("2")
	for _, example := range deckcapture.Cases(session) {
		if example.Name == "internal" {
			driver.Press("4")
		}
		var payload *errors.Error
		testutil.ErrorIf(t, !errors.As(example.Err, &payload), "unclassified %s error: %v", example.Name, example.Err)
		testutil.Equals(t, payload.Kind(), example.Kind)
		terminal := errors.ToTUIError(example.Err)
		testutil.Equals(t, terminal.Style, example.Style)
		var exit cli.ExitCoder
		testutil.ErrorIf(t, !errors.As(errors.ToCLIExit(example.Err), &exit), "missing CLI exit")
		testutil.Equals(t, exit.ExitCode(), example.Exit)
		testutil.Equals(t, exit.Error(), terminal.Message)
		// Deliver the error at the root status-bar boundary, independently of a form.
		driver.Send(routes.ErrorMsg{Err: example.Err})
		driver.RequireText(terminal.Message)
		driver.RequireNoText("database is locked", "load readiness:", "condition 0:")
		testutil.Ok(t, os.WriteFile(filepath.Join(os.Getenv("MIXOLOGY_RENDER_DIR"), "tui-error-"+example.Name+".ansi"), []byte(driver.Screen()), 0644))
	}
}
