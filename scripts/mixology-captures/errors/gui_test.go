package main

import (
	"context"
	"os"
	"testing"

	framework "fyne.io/fyne/v2"
	"fyne.io/fyne/v2/test"
	"fyne.io/fyne/v2/theme"
	ingredientsgui "github.com/TheFellow/go-modular-monolith/app/domains/ingredients/surfaces/gui"
	"github.com/TheFellow/go-modular-monolith/deckcapture"
	"github.com/TheFellow/go-modular-monolith/pkg/errors"
	"github.com/TheFellow/go-modular-monolith/pkg/testutil"
	toolkit "github.com/TheFellow/go-modular-monolith/pkg/toolkits/gui"
)

func TestDeckCaptureErrors(t *testing.T) {
	for _, name := range []string{"invalid", "conflict", "internal"} {
		t.Run(name, func(t *testing.T) {
			gui := test.NewApp()
			t.Cleanup(gui.Quit)
			gui.Settings().SetTheme(theme.DarkTheme())
			desktop, err := openDesktopWithDependencies(context.Background(), gui, desktopConfig{
				dataDirectory: t.TempDir(), databasePath: os.Getenv("MIXOLOGY_DB"), actor: "owner",
			}, deterministicDesktopDependencies(nil))
			testutil.Ok(t, err)
			t.Cleanup(func() { testutil.Ok(t, desktop.Close()) })
			desktop.window.Resize(framework.NewSize(1100, 720))
			testutil.Ok(t, desktop.shell.Navigate("ingredients"))
			presenter := desktop.presenters["ingredients"].(*ingredientsgui.Presenter)
			var failure error
			var severity toolkit.ErrorSeverity
			switch name {
			case "invalid":
				presenter.StartCreate()
				input := deckcapture.MissingNameIngredient()
				presenter.Submit(ingredientsgui.Form{Name: input.Name, Category: input.Category, Unit: input.Unit, Description: "Keep this correction"})
				failure = presenter.Snapshot().Err
				testutil.ErrorIsInvalid(t, failure)
				severity = toolkit.ErrorSeverityInline
			case "conflict":
				presenter.StartCreate()
				duplicate := deckcapture.DuplicateIngredient()
				form := ingredientsgui.Form{Name: duplicate.Name, Category: duplicate.Category, Unit: duplicate.Unit, Description: "Keep this correction"}
				testutil.ErrorIf(t, !presenter.Submit(form), "duplicate create not submitted")
				failure = presenter.Snapshot().Err
				testutil.ErrorIsConflict(t, failure)
				testutil.Equals(t, presenter.Snapshot().Form.Description, form.Description)
				severity = toolkit.ErrorSeverityWarning
			case "internal":
				testutil.Ok(t, desktop.shell.Navigate("menus"))
				failure = deckcapture.InternalFailure()
				testutil.ErrorIsInternal(t, failure)
				toolkit.ShowPresentation(toolkit.WindowDialogs{Window: desktop.window}, failure)
				severity = toolkit.ErrorSeverityError
			}
			var presentation toolkit.ErrorPresentation
			testutil.ErrorIf(t, !errors.As(toolkit.PresentError(failure), &presentation), "missing presentation")
			testutil.Equals(t, presentation.Severity, severity)
			testutil.Equals(t, presentation.Message, errors.ToTUIError(failure).Message)
			captureReview(t, desktop, os.Getenv("MIXOLOGY_RENDER_DIR"), "gui-error-"+name+".png")
		})
	}
}
