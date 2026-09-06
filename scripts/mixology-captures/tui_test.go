package main

import (
	"context"
	"io"
	"log/slog"
	"os"
	"path/filepath"
	"testing"

	"github.com/TheFellow/go-modular-monolith/app"
	"github.com/TheFellow/go-modular-monolith/app/domains/ingredients"
	"github.com/TheFellow/go-modular-monolith/pkg/authn"
	pkglog "github.com/TheFellow/go-modular-monolith/pkg/log"
	"github.com/TheFellow/go-modular-monolith/pkg/store"
	"github.com/TheFellow/go-modular-monolith/pkg/testutil"
	"github.com/TheFellow/go-modular-monolith/pkg/testutil/tuitest"
	"github.com/charmbracelet/lipgloss"
	"github.com/muesli/termenv"
)

// Run only in the disposable checkout prepared by capture.sh.
func TestDeckCapture(t *testing.T) {
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
	driver.Resize(140, 36)
	capture := func(name string) {
		t.Helper()
		driver.RequireViewport(140, 36)
		testutil.Ok(t, os.WriteFile(filepath.Join(os.Getenv("MIXOLOGY_RENDER_DIR"), name+".ansi"), []byte(driver.Screen()), 0644))
	}
	driver.RequireText("Dashboard", "Recent Activity")
	capture("tui-dashboard")
	driver.Press("2")
	driver.RequireText("Ingredients")
	items, err := session.Ingredients.List(session.Context(), ingredients.ListRequest{Limit: 100})
	testutil.Ok(t, err)
	found := false
	for _, ingredient := range items.Items {
		if ingredient.Name == "London Dry Gin" {
			found = true
			break
		}
		driver.Press("down")
	}
	testutil.ErrorIf(t, !found, "seed gin missing")
	capture("tui-ingredients")
	driver.Press("e")
	driver.RequireText("Name")
	capture("tui-ingredient-edit")
}
