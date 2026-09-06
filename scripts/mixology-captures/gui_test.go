package main

import (
	"context"
	"os"
	"testing"

	framework "fyne.io/fyne/v2"
	"fyne.io/fyne/v2/test"
	"fyne.io/fyne/v2/theme"
	ingredientsgui "github.com/TheFellow/go-modular-monolith/app/domains/ingredients/surfaces/gui"
	menusgui "github.com/TheFellow/go-modular-monolith/app/domains/menus/surfaces/gui"
	ordersmodels "github.com/TheFellow/go-modular-monolith/app/domains/orders/models"
	ordersgui "github.com/TheFellow/go-modular-monolith/app/domains/orders/surfaces/gui"
	"github.com/TheFellow/go-modular-monolith/pkg/testutil"
)

func TestDeckCapture(t *testing.T) {
	gui := test.NewApp()
	t.Cleanup(gui.Quit)
	gui.Settings().SetTheme(theme.DarkTheme())
	desktop, err := openDesktopWithDependencies(context.Background(), gui, desktopConfig{
		dataDirectory: t.TempDir(), databasePath: os.Getenv("MIXOLOGY_DB"), actor: "owner",
	}, deterministicDesktopDependencies(nil))
	testutil.Ok(t, err)
	t.Cleanup(func() { testutil.Ok(t, desktop.Close()) })
	desktop.window.Resize(framework.NewSize(1100, 720))
	capture := func(name string) { captureReview(t, desktop, os.Getenv("MIXOLOGY_RENDER_DIR"), name+".png") }
	testutil.Ok(t, desktop.shell.Navigate("ingredients"))
	ingredients := desktop.presenters["ingredients"].(*ingredientsgui.Presenter)
	testutil.ErrorIf(t, len(ingredients.Snapshot().Items) == 0, "seed ingredients missing")
	capture("gui-ingredients")
	found := false
	for _, ingredient := range ingredients.Snapshot().Items {
		if ingredient.Name == "London Dry Gin" {
			ingredients.Select(ingredient.ID)
			found = true
			break
		}
	}
	testutil.ErrorIf(t, !found, "seed gin missing")
	ingredients.StartEdit()
	capture("gui-ingredient-edit")
	ingredients.Cancel()
	testutil.Ok(t, desktop.shell.Navigate("menus"))
	menus := desktop.presenters["menus"].(*menusgui.Presenter)
	testutil.ErrorIf(t, len(menus.State().Items) == 0, "seed menu missing")
	menus.Select(0)
	test.Scroll(desktop.window.Canvas(), framework.NewPos(650, 450), 0, -520)
	capture("gui-menu")
	menu := menus.State().Selected
	order, err := desktop.session.Orders.Place(desktop.session.Context(), &ordersmodels.Order{
		MenuID: menu.ID, Items: []ordersmodels.OrderItem{{DrinkID: menu.Items[0].DrinkID, Quantity: 2}}, Notes: "Bar seat four",
	})
	testutil.Ok(t, err)
	testutil.Ok(t, desktop.shell.Navigate("orders"))
	orders := desktop.presenters["orders"].(*ordersgui.Presenter)
	for i, row := range orders.State().Rows {
		if row.Order.ID == order.ID {
			orders.Select(i)
			test.Scroll(desktop.window.Canvas(), framework.NewPos(650, 450), 0, -620)
			capture("gui-order")
			return
		}
	}
	t.Fatal("placed order missing")
}
